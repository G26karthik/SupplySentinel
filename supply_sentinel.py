import os
import time
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import logging configuration
from logging_config import setup_logging, config_logger, watchman_logger, analyst_logger, dispatcher_logger

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure logging for CLI with file output
setup_logging(environment="cli")

class SupplySentinel:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.history_file = "alert_history.json"
        self.alert_history = self._load_history()
        
        # Configuration for Gemini 2.5 Flash
        self.model_id = "gemini-2.5-flash"
        
        # AGENTIC CONCEPT 1: TOOLS (Native Google Search Grounding)
        self.search_tool = types.Tool(
            google_search=types.GoogleSearch() 
        )

    def _load_history(self):
        """AGENTIC CONCEPT 2: STATE/MEMORY (Persistence)"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return set(json.load(f))
            except:
                return set()
        return set()

    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(list(self.alert_history), f)

    def watchman_agent(self, material, location, retry_without_location=False):
        """
        Role: The Hunter. Finds raw signals.
        """
        if retry_without_location:
            prompt = f"""
            Find recent logistics, weather, or political news affecting {material} supply globally.
            Focus on strikes, shortages, or natural disasters in the last 7 days.
            """
            watchman_logger.info(f"Retrying search with broader query (material-only): {material}")
        else:
            prompt = f"""
            Find recent logistics, weather, or political news that could affect the supply of {material} from {location}.
            Focus on strikes, shortages, or natural disasters in the last 7 days.
            """
            watchman_logger.debug(f"Initiating search for {material} in {location}")
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[self.search_tool],
                    response_mime_type="text/plain" 
                )
            )
            result = response.text
            article_count = len([line for line in result.split('\n') if line.strip()])
            
            if retry_without_location:
                watchman_logger.info(f"Retry search returned {article_count} data points for {material}")
            else:
                watchman_logger.info(f"Search returned {article_count} data points for {material} in {location}")
            
            return result
        except Exception as e:
            watchman_logger.error(f"Search failed for {material} in {location}: {str(e)}", exc_info=True)
            return None

    def analyst_agent(self, material, location, search_data):
        """
        Role: The Brain. Scores the risk.
        """
        if not search_data:
            analyst_logger.warning(f"Insufficient data for analysis: {material} in {location}")
            return None

        # AGENTIC CONCEPT 3: HANDSHAKE & CONTEXT ENGINEERING
        prompt = f"""
        CONTEXT: You are a Supply Chain Risk Officer.
        INPUT DATA: {search_data}
        
        TASK: Analyze the risk for {material} from {location}.
        
        OUTPUT: JSON with:
        - risk_score (0-10, where 10 is factory shutdown, 0 means no relevant information found)
        - reason (1 sentence)
        - action_needed (boolean)
        - retry_search (boolean - true if score is 0 and a broader search might help)
        """

        try:
            analyst_logger.debug(f"Risk analysis initiated for {material} in {location}")
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            risk_data = json.loads(response.text)
            score = risk_data.get('risk_score', 0)
            
            # Log based on severity
            if score == 0:
                analyst_logger.warning(f"No relevant data found for {material} in {location} — Agent recommends retry")
            elif score >= 7:
                analyst_logger.critical(f"Risk score computed: {score}/10 — CRITICAL threat level for {material} in {location}")
            elif score >= 5:
                analyst_logger.warning(f"Risk score computed: {score}/10 — ELEVATED threat level for {material} in {location}")
            else:
                analyst_logger.info(f"Risk score computed: {score}/10 — NORMAL threat level for {material} in {location}")
            
            return risk_data
        except Exception as e:
            analyst_logger.error(f"Analysis failed for {material} in {location}: {str(e)}", exc_info=True)
            return None

    def dispatcher_agent(self, material, location, risk_data):
        """
        Role: The Action. Filters noise and alerts user.
        """
        if not risk_data:
            dispatcher_logger.info(f"No significant risks detected for {material} in {location}")
            return

        score = risk_data.get('risk_score', 0)
        reason = risk_data.get('reason', 'Unknown')
        alert_id = f"{material}-{location}-{datetime.now().strftime('%Y-%m-%d')}"

        # CHECK MEMORY (Deduplication)
        if alert_id in self.alert_history:
            dispatcher_logger.debug(f"Duplicate alert suppressed: {alert_id}")
            return

        # CHECK THRESHOLD (Logic)
        if score >= 7:
            print(f"\n🚨 🚨 CRITICAL ALERT: {material} Supply Chain Risk!")
            print(f"   -> Location: {location}")
            print(f"   -> Score: {score}/10")
            print(f"   -> Reason: {reason}")
            print(f"   -> [Sent Email to Procurement Team]\n")
            
            dispatcher_logger.critical(f"Critical alert sent — {material}-{location} — Score: {score}/10 — Reason: {reason}")
            
            # UPDATE MEMORY
            self.alert_history.add(alert_id)
            self._save_history()
        else:
            dispatcher_logger.info(f"Risk monitored (non-critical) — {material}-{location} — Score: {score}/10")

    def run_loop(self, debug_mode=False):
        """AGENTIC CONCEPT 4: LONG-RUNNING OPERATION"""
        print("🟢 SupplySentinel Active. Monitoring Global Chains...")
        dispatcher_logger.info("Monitoring loop started")
        
        # Load configuration
        try:
            with open("suppliers.json", "r") as f:
                suppliers = json.load(f)
                config_logger.info(f"Loaded {len(suppliers)} suppliers from configuration")
        except FileNotFoundError:
            config_logger.error("suppliers.json not found. Run config_agent.py first.")
            print("❌ Error: suppliers.json not found. Run config_agent.py first.")
            return

        cycle_number = 0
        while True:
            cycle_number += 1
            dispatcher_logger.info(f"Starting monitoring cycle #{cycle_number}")
            
            safe_count = 0
            critical_count = 0
            skipped_count = 0
            
            for item in suppliers:
                # 1. Watchman scans
                news = self.watchman_agent(item['material'], item['location'])
                
                # 2. Analyst scores
                risk_analysis = self.analyst_agent(item['material'], item['location'], news)
                
                # 3. Dispatcher acts
                self.dispatcher_agent(item['material'], item['location'], risk_analysis)
                
                # Track statistics
                if risk_analysis:
                    score = risk_analysis.get('risk_score', 0)
                    if score >= 7:
                        critical_count += 1
                    else:
                        safe_count += 1
                else:
                    skipped_count += 1
                
                time.sleep(2) # Graceful spacing between agents
            
            # Log cycle completion statistics
            dispatcher_logger.info(f"Cycle #{cycle_number} complete — Scanned: {len(suppliers)} | Safe: {safe_count} | Critical: {critical_count} | Skipped: {skipped_count}")

            if debug_mode:
                print("🟡 Debug Mode: Stopping after one cycle.")
                break
            
            print("💤 Cycle complete. Sleeping for 24 hours...")
            time.sleep(86400)

if __name__ == "__main__":
    sentinel = SupplySentinel()
    # Set debug_mode=True for the video demo!
    sentinel.run_loop(debug_mode=True)
