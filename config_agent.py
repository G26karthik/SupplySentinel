import os
import json
from typing import List, Dict
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class ConfigurationAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY environment variable not set.")
            sys.exit(1)
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"

    def run_interview(self) -> List[Dict[str, str]]:
        """
        Conducts a simple interview with the user to understand their business.
        """
        print("\n--- SupplySentinel Configuration ---")
        print("To protect your supply chain, I need to understand your business.")
        business_description = input("What is your business and where are you located? (e.g., 'I make electric bikes in Texas'): ").strip()
        
        if not business_description:
            print("Input cannot be empty. Please try again.")
            return self.run_interview()
            
        return self.generate_suppliers(business_description)

    def generate_suppliers(self, business_context: str) -> List[Dict[str, str]]:
        """
        Generates a list of suppliers based on the business context.
        """
        print(f"\nAnalyzing supply chain for: '{business_context}'...")
        
        prompt = f"""
        Based on the following business description: "{business_context}", 
        identify the top 3 likely supply chain dependencies.
        For each dependency, specify the 'material' and the likely 'location' (Country) of origin.
        
        Return the result as a JSON list of objects, where each object has "material" and "location" keys.
        Example:
        [
            {{"material": "Coffee Beans", "location": "Brazil"}},
            {{"material": "Paper Cups", "location": "China"}}
        ]
        """
        
        system_instruction = "You are a Global Supply Chain Expert. Your goal is to identify the top 3 most critical supply chain dependencies (materials and their likely country of origin) for a given business. You must be precise and realistic."
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json"
                )
            )
            
            suppliers = json.loads(response.text)
            return suppliers
            
        except Exception as e:
            print(f"Error generating suppliers: {e}")
            return []

    def save_suppliers(self, suppliers: List[Dict[str, str]], filepath: str = "suppliers.json"):
        """
        Saves the generated suppliers to a JSON file.
        """
        try:
            with open(filepath, "w") as f:
                json.dump(suppliers, f, indent=4)
            print(f"\nSuccessfully saved {len(suppliers)} suppliers to {filepath}.")
        except Exception as e:
            print(f"Error saving suppliers: {e}")

if __name__ == "__main__":
    agent = ConfigurationAgent()
    suppliers = agent.run_interview()
    
    if suppliers:
        print("\nGenerated Supply Chain Map:")
        print(json.dumps(suppliers, indent=2))
        
        confirm = input("\nPress Enter to confirm and save, or type 'retry' to try again: ").strip().lower()
        
        if confirm == 'retry':
            print("Restarting configuration...")
            suppliers = agent.run_interview()
        
        agent.save_suppliers(suppliers)
        print("Configuration complete. You can now run 'supply_sentinel.py'.")
