import streamlit as st
import json
import os
import time
import logging
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Page
st.set_page_config(
    page_title="SupplySentinel: Multi-Agent Risk Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Premium Custom CSS
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --primary-color: #3B82F6;
        --primary-dark: #2563EB;
        --success-color: #10B981;
        --warning-color: #F59E0B;
        --danger-color: #EF4444;
        --bg-dark: #0F172A;
        --bg-card: #1E293B;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --border-color: #334155;
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    h1 {
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 1.25rem !important;
    }
    
    .subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        color: #3B82F6;
    }
    
    .premium-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(30, 41, 59, 0.4) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid var(--border-color);
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    .status-card {
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .status-card:hover {
        transform: translateX(4px);
    }
    
    .status-card.critical {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, transparent 100%);
        border-left-color: var(--danger-color);
    }
    
    .status-card.safe {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, transparent 100%);
        border-left-color: var(--success-color);
    }
    
    .status-card.info {
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%);
        border-left-color: var(--primary-color);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }
    
    .stTextInput > div > div > input {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        color: var(--text-primary);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border-right: 1px solid var(--border-color);
    }
    
    .success-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 0.75rem;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        h1 {
            font-size: 2rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

class StreamlitConfigAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"

    def generate_suppliers(self, business_context: str):
        system_instruction = "You are a Global Supply Chain Expert. Identify the top 3 most critical supply chain dependencies (materials and their likely country of origin) for a given business. Be precise and realistic."
        
        prompt = f"""
        Based on: "{business_context}", identify the top 3 likely supply chain dependencies.
        For each dependency, specify the 'material' and the likely 'location' (Country) of origin.
        
        Return as a JSON list of objects with "material" and "location" keys.
        Example: [{{"material": "Steel", "location": "China"}}, {{"material": "Rubber", "location": "Thailand"}}]
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            st.error(f"Error generating suppliers: {e}")
            return []

class StreamlitSentinel:
    def __init__(self, api_key, debug_mode=True):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"
        self.debug_mode = debug_mode
        self.history_file = "alert_history.json"
        self.alert_history = self._load_history()
        
        self.search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

    def _load_history(self):
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
        prompt = f"""
        Find recent logistics, weather, or political news affecting {material} supply from {location}.
        Focus on strikes, shortages, or natural disasters in the last 7 days.
        """
        
        try:
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
            return f"Search error: {str(e)}"

    def analyst_agent(self, material, location, search_data):
        if not search_data or "error" in search_data.lower():
            return None

        prompt = f"""
        CONTEXT: You are a Supply Chain Risk Officer.
        INPUT DATA: {search_data}
        TASK: Analyze risk for {material} from {location}.
        
        OUTPUT JSON:
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
            return None

    def check_item(self, material, location):
        alert_id = f"{material}-{location}-{datetime.now().strftime('%Y-%m-%d')}"
        
        if alert_id in self.alert_history:
            return {
                "material": material,
                "location": location,
                "status": "skipped",
                "message": "Already assessed today"
            }
        
        with st.spinner(f"🔍 Watchman scanning: {material} in {location}..."):
            news = self.watchman_agent(material, location)
        
        with st.spinner(f"📊 Analyst evaluating risk..."):
            risk_data = self.analyst_agent(material, location, news)
        
        if not risk_data:
            return {
                "material": material,
                "location": location,
                "status": "safe",
                "score": 0,
                "message": "No significant risks detected"
            }
        
        score = risk_data.get('risk_score', 0)
        reason = risk_data.get('reason', 'Unknown')
        
        if score >= 7:
            self.alert_history.add(alert_id)
            self._save_history()
            return {
                "material": material,
                "location": location,
                "status": "critical",
                "score": score,
                "reason": reason
            }
        else:
            return {
                "material": material,
                "location": location,
                "status": "safe",
                "score": score,
                "reason": reason
            }

def main():
    load_custom_css()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        api_key = st.text_input(
            "GEMINI_API_KEY", 
            type="password", 
            value=os.getenv("GEMINI_API_KEY", ""),
            help="Enter your Google Gemini API key"
        )
        
        debug_mode = st.toggle(
            "⚡ Debug Mode", 
            value=True,
            help="Run single cycle for testing"
        )
        
        st.markdown("---")
        
        st.markdown("### ✨ Multi-Agent System")
        st.markdown("""
        <div style='font-size: 0.9rem; line-height: 1.8;'>
        <b>1. Config Agent</b><br/>
        &nbsp;&nbsp;Maps supply chain<br/>
        <b>2. Watchman Agent</b><br/>
        &nbsp;&nbsp;Scans global news<br/>
        <b>3. Analyst Agent</b><br/>
        &nbsp;&nbsp;Scores risk levels<br/>
        <b>4. Dispatcher Agent</b><br/>
        &nbsp;&nbsp;Sends critical alerts
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📚 About")
        st.markdown("""
        <div style='font-size: 0.85rem; color: #94A3B8; line-height: 1.6;'>
        <b>SupplySentinel</b> - Multi-agent AI system for supply chain protection.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if api_key:
            st.markdown("""
            <div style='display: flex; align-items: center; gap: 0.5rem; color: #10B981;'>
                <span style='font-size: 1.5rem;'>●</span>
                <span style='font-size: 0.85rem; font-weight: 600;'>System Ready</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='display: flex; align-items: center; gap: 0.5rem; color: #F59E0B;'>
                <span style='font-size: 1.5rem;'>●</span>
                <span style='font-size: 0.85rem; font-weight: 600;'>Awaiting API Key</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Hero
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🛡️</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("SupplySentinel")
    st.markdown("""
    <div class='subtitle'>
        <span>AI-Powered Multi-Agent Risk Monitoring</span>
        <span class='badge'>One-Click</span>
        <span class='badge'>Real-Time</span>
    </div>
    """, unsafe_allow_html=True)
    
    if not api_key:
        st.markdown("""
        <div class='premium-card' style='text-align: center; padding: 3rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🔑</div>
            <h3 style='margin-bottom: 1rem;'>API Key Required</h3>
            <p style='color: #94A3B8;'>Enter your GEMINI_API_KEY in the sidebar.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Main Interface
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='premium-card'>
        <div style='display: flex; align-items: start; gap: 1.5rem;'>
            <div style='font-size: 3rem; line-height: 1;'>🚀</div>
            <div>
                <h2 style='margin: 0 0 0.5rem 0 !important;'>One-Click Supply Chain Protection</h2>
                <p style='color: #94A3B8; margin: 0; font-size: 1rem; line-height: 1.6;'>
                    Describe your business and watch our multi-agent system automatically map dependencies, 
                    monitor risks, and deliver alerts—all in one seamless flow.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 📝 Business Description")
    business_input = st.text_input(
        "What does your business do?",
        placeholder="e.g., I manufacture solar panels in Arizona",
        key="business_input",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_btn = st.button(
            "🎯 Analyze & Monitor Supply Chain", 
            type="primary", 
            use_container_width=True,
            help="Complete workflow: Map → Monitor → Alert"
        )
    
    if analyze_btn and business_input:
        config_agent = StreamlitConfigAgent(api_key)
        sentinel = StreamlitSentinel(api_key, debug_mode)
        
        # PHASE 1: Config Agent
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 🤖 Phase 1: Configuration Agent")
        
        with st.spinner("🔍 Analyzing business & mapping supply chain..."):
            suppliers = config_agent.generate_suppliers(business_input)
            time.sleep(1)
        
        if not suppliers:
            st.error("❌ Failed to analyze. Please try again.")
            return
        
        st.markdown(f"""
        <div class='success-banner'>
            <span style='font-size: 2rem;'>✓</span>
            <div>
                <div style='font-weight: 600; color: #10B981; font-size: 1.1rem;'>Supply Chain Mapped!</div>
                <div style='color: #94A3B8; font-size: 0.9rem;'>Identified {len(suppliers)} critical dependencies</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display map
        st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-top: 0;'>📊 Supply Chain Map</h3>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(len(suppliers))
        for idx, item in enumerate(suppliers):
            with cols[idx]:
                st.markdown(f"""
                <div class='metric-card' style='text-align: left; padding: 1rem;'>
                    <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>📦</div>
                    <div style='font-weight: 600; color: #3B82F6; margin-bottom: 0.25rem;'>{item['material']}</div>
                    <div style='color: #94A3B8; font-size: 0.85rem;'>📍 {item['location']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # PHASE 2: Monitoring
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 👁️ Phase 2: Watchman → Analyst → Dispatcher")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("#### 📈 Real-Time Metrics")
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            total_metric = st.empty()
        with metric_cols[1]:
            safe_metric = st.empty()
        with metric_cols[2]:
            critical_metric = st.empty()
        with metric_cols[3]:
            progress_metric = st.empty()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("#### 🔍 Risk Analysis Results")
        st.markdown("<br>", unsafe_allow_html=True)
        
        results = st.container()
        
        safe_count = 0
        critical_count = 0
        
        for idx, item in enumerate(suppliers):
            material = item.get('material')
            location = item.get('location')
            
            result = sentinel.check_item(material, location)
            
            with results:
                if result['status'] == 'critical':
                    st.markdown(f"""
                    <div class='status-card critical'>
                        <div style='display: flex; align-items: start; gap: 1rem;'>
                            <div style='font-size: 2rem; line-height: 1;'>🚨</div>
                            <div style='flex: 1;'>
                                <h3 style='margin: 0 0 0.5rem 0; color: #EF4444;'>CRITICAL: {material}</h3>
                                <div style='display: grid; grid-template-columns: auto 1fr; gap: 0.5rem 1rem; font-size: 0.95rem;'>
                                    <span style='color: #94A3B8;'>📍 Location:</span>
                                    <span style='color: #F1F5F9; font-weight: 500;'>{location}</span>
                                    <span style='color: #94A3B8;'>⚠️ Risk Score:</span>
                                    <span style='color: #EF4444; font-weight: 700;'>{result['score']}/10</span>
                                    <span style='color: #94A3B8;'>📋 Reason:</span>
                                    <span style='color: #F1F5F9;'>{result['reason']}</span>
                                    <span style='color: #94A3B8;'>✉️ Dispatcher:</span>
                                    <span style='color: #10B981; font-weight: 500;'>Alert sent to procurement</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    critical_count += 1
                elif result['status'] == 'safe':
                    st.markdown(f"""
                    <div class='status-card safe'>
                        <div style='display: flex; align-items: center; gap: 1rem;'>
                            <div style='font-size: 1.5rem;'>✓</div>
                            <div style='flex: 1;'>
                                <span style='font-weight: 600; color: #F1F5F9;'>{material}</span>
                                <span style='color: #94A3B8;'> from </span>
                                <span style='color: #10B981; font-weight: 500;'>{location}</span>
                                <div style='color: #94A3B8; font-size: 0.9rem; margin-top: 0.25rem;'>
                                    Risk: {result['score']}/10 • {result.get('reason', 'No risks')}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    safe_count += 1
                else:
                    st.markdown(f"""
                    <div class='status-card info'>
                        <div style='display: flex; align-items: center; gap: 1rem;'>
                            <div style='font-size: 1.5rem;'>ℹ️</div>
                            <div>
                                <span style='font-weight: 600; color: #F1F5F9;'>{material}</span>
                                <span style='color: #94A3B8;'> from {location} • {result['message']}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Update metrics
            total_metric.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Scanned</div>
                <div class='metric-value'>{idx + 1}</div>
            </div>
            """, unsafe_allow_html=True)
            
            safe_metric.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>✓ Safe</div>
                <div class='metric-value' style='color: #10B981;'>{safe_count}</div>
            </div>
            """, unsafe_allow_html=True)
            
            critical_metric.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>⚠️ Critical</div>
                <div class='metric-value' style='color: #EF4444;'>{critical_count}</div>
            </div>
            """, unsafe_allow_html=True)
            
            progress_pct = int(((idx + 1) / len(suppliers)) * 100)
            progress_metric.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Progress</div>
                <div class='metric-value' style='font-size: 2rem;'>{progress_pct}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1)
        
        # Summary
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='premium-card' style='text-align: center; padding: 2.5rem;'>
            <div style='font-size: 3.5rem; margin-bottom: 1rem;'>✅</div>
            <h2 style='margin-bottom: 1rem; color: #10B981;'>Multi-Agent Analysis Complete</h2>
            <p style='color: #94A3B8; margin-bottom: 2rem;'>All agents completed their tasks successfully</p>
            <div style='display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;'>
                <div>
                    <div style='font-size: 2.5rem; font-weight: 700; color: #3B82F6;'>{len(suppliers)}</div>
                    <div style='color: #94A3B8; font-size: 0.95rem;'>Dependencies Mapped</div>
                </div>
                <div>
                    <div style='font-size: 2.5rem; font-weight: 700; color: #10B981;'>{safe_count}</div>
                    <div style='color: #94A3B8; font-size: 0.95rem;'>Safe Operations</div>
                </div>
                <div>
                    <div style='font-size: 2.5rem; font-weight: 700; color: #EF4444;'>{critical_count}</div>
                    <div style='color: #94A3B8; font-size: 0.95rem;'>Critical Alerts</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Save
        with open("suppliers.json", "w") as f:
            json.dump(suppliers, f, indent=4)
        
        if debug_mode:
            st.info("🔧 Debug mode: Single cycle complete. Disable for 24/7 monitoring.")

if __name__ == "__main__":
    main()
