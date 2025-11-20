import os
import time
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    def watchman_agent(self, material, location):
        """
        Role: The Hunter. Finds raw signals.
        """
        logging.info(f"🔍 Watchman scanning: {material} in {location}...")
        
        prompt = f"""
        Find recent logistics, weather, or political news that could affect the supply of {material} from {location}.
        Focus on strikes, shortages, or natural disasters in the last 7 days.
        """
        
        try:
            # Using the Search Tool explicitly
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[self.search_tool],
                    response_mime_type="text/plain" 
                )
            )
            return response.text
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return None

    def analyst_agent(self, material, location, search_data):
        """
        Role: The Brain. Scores the risk.
        """
        if not search_data:
            return None

        # AGENTIC CONCEPT 3: HANDSHAKE & CONTEXT ENGINEERING
        prompt = f"""
        CONTEXT: You are a Supply Chain Risk Officer.
        INPUT DATA: {search_data}
        
        TASK: Analyze the risk for {material} from {location}.
        
        OUTPUT: JSON with:
        - risk_score (0-10, where 10 is factory shutdown)
        - reason (1 sentence)
        - action_needed (boolean)
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            return None

    def dispatcher_agent(self, material, location, risk_data):
        """
        Role: The Action. Filters noise and alerts user.
        """
        if not risk_data:
            return

        score = risk_data.get('risk_score', 0)
        alert_id = f"{material}-{location}-{datetime.now().strftime('%Y-%m-%d')}"

        # CHECK MEMORY (Deduplication)
        if alert_id in self.alert_history:
            logging.info(f"   -> [SKIPPED] Alert already sent today for {material}.")
            return

        # CHECK THRESHOLD (Logic)
        if score >= 7:
            print(f"\n🚨 🚨 CRITICAL ALERT: {material} Supply Chain Risk!")
            print(f"   -> Location: {location}")
            print(f"   -> Score: {score}/10")
            print(f"   -> Reason: {risk_data.get('reason')}")
            print(f"   -> [Sent Email to Procurement Team]\n")
            
            # UPDATE MEMORY
            self.alert_history.add(alert_id)
            self._save_history()
        else:
            logging.info(f"   -> [SAFE] Risk score {score}/10 is below threshold.")

    def run_loop(self, debug_mode=False):
        """AGENTIC CONCEPT 4: LONG-RUNNING OPERATION"""
        print("🟢 SupplySentinel Active. Monitoring Global Chains...")
        
        # Load configuration
        try:
            with open("suppliers.json", "r") as f:
                suppliers = json.load(f)
        except FileNotFoundError:
            print("❌ Error: suppliers.json not found. Run config_agent.py first.")
            return

        while True:
            for item in suppliers:
                # 1. Watchman scans
                news = self.watchman_agent(item['material'], item['location'])
                
                # 2. Analyst scores
                risk_analysis = self.analyst_agent(item['material'], item['location'], news)
                
                # 3. Dispatcher acts
                self.dispatcher_agent(item['material'], item['location'], risk_analysis)
                
                time.sleep(2) # Graceful spacing between agents

            if debug_mode:
                print("🟡 Debug Mode: Stopping after one cycle.")
                break
            
            print("💤 Cycle complete. Sleeping for 24 hours...")
            time.sleep(86400)

if __name__ == "__main__":
    sentinel = SupplySentinel()
    # Set debug_mode=True for the video demo!
    sentinel.run_loop(debug_mode=True)
