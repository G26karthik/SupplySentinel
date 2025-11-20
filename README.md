# 🛡️ SupplySentinel: Multi-Agent Supply Chain Protection

> **Google x Kaggle Agents Intensive Capstone**  
> **Track:** Enterprise Agents  
> **Focus:** Autonomous supply chain risk monitoring with real-time alerting

SupplySentinel is a **premium multi-agent AI system** that protects your supply chain from global disruptions. Using Google's Gemini 2.5 Flash with native search grounding, it automatically maps dependencies, monitors risks, and dispatches critical alerts—all through an intuitive one-click interface.

## 🎯 Key Highlights

- **🚀 One-Click Workflow**: Enter your business → Complete analysis in seconds
- **🤖 4-Agent Architecture**: Config → Watchman → Analyst → Dispatcher
- **🔍 Real-Time Intelligence**: Native Google Search integration for live data
- **💎 Premium UI**: Modern, enterprise-grade Streamlit interface
- **⚡ Instant Setup**: Zero configuration, AI-powered dependency mapping
- **🎯 Smart Filtering**: Alerts only on critical risks (score ≥7/10)

## 🏗️ Multi-Agent Architecture

### **Agent 1: Configuration Agent** 
- **Role**: Supply Chain Mapper
- **Input**: Business description (natural language)
- **Output**: Structured dependency map (materials + locations)
- **Tech**: Gemini AI reasoning

### **Agent 2: Watchman Agent** 🔍
- **Role**: Global Risk Scanner
- **Input**: Material + Location pairs
- **Output**: Real-time news about logistics, weather, politics
- **Tech**: Gemini AI + **Google Search Grounding**

### **Agent 3: Analyst Agent** 📊
- **Role**: Risk Evaluator
- **Input**: News data from Watchman
- **Output**: Risk score (0-10) + reason
- **Tech**: Gemini AI analysis

### **Agent 4: Dispatcher Agent** ✉️
- **Role**: Alert Manager
- **Input**: Risk scores from Analyst
- **Output**: Critical alerts (if score ≥7)
- **Tech**: Logic + persistent memory

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd SupplySentinel-main

# Install dependencies
pip install -r requirements.txt

# Set your API key
# Windows PowerShell:
$env:GEMINI_API_KEY="your_api_key_here"

# Linux/Mac:
export GEMINI_API_KEY="your_api_key_here"

# Or create a .env file:
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### Run the Premium Web Interface (Recommended)

```bash
streamlit run app.py
```

Then:
1. **Enter your API key** in the sidebar (if not in .env)
2. **Describe your business**: "I manufacture solar panels in Arizona"
3. **Click "Analyze & Monitor Supply Chain"**
4. **Watch the multi-agent system work** automatically!

### Run Command-Line Version (Alternative)

```bash
# Step 1: Configure your supply chain
python config_agent.py

# Step 2: Start continuous monitoring
python supply_sentinel.py
```

## 💎 Premium Web Interface

The Streamlit app provides an enterprise-grade experience:

### ✨ Features
- **Single-Page Flow**: Complete analysis in one click
- **Real-Time Metrics**: Live updating dashboards
- **Visual Supply Chain Map**: See your dependencies at a glance
- **Color-Coded Alerts**: Critical (red), Safe (green), Info (blue)
- **Progressive Disclosure**: Watch agents work step-by-step
- **Responsive Design**: Works on desktop and mobile
- **Dark Theme**: Premium glassmorphism UI

### 🎨 UI Components
- Premium card layouts with hover effects
- Animated metric displays
- Status cards with left-border accents
- Gradient buttons with lift animations
- Real-time progress tracking
- Final summary dashboard

## 📁 Project Structure

```
SupplySentinel-main/
├── app.py                    # Premium Streamlit web interface (MAIN)
├── supply_sentinel.py        # CLI monitoring loop (alternative)
├── config_agent.py          # CLI configuration tool (alternative)
├── requirements.txt         # Python dependencies
├── .env                     # API key storage (create this)
├── suppliers.json           # Auto-generated supply chain map
├── alert_history.json       # Agent memory for deduplication
├── README.md               # This file
└── README_DEPLOY.md        # Cloud deployment guide
```

## 🔄 How It Works

### Single-Click Workflow (Web UI)

```
User Input
   ↓
[Config Agent] → Analyzes business → Generates suppliers.json
   ↓
[Supply Chain Map Display] → Visual representation
   ↓
For each dependency:
   [Watchman Agent] → Scans Google Search → Returns news
        ↓
   [Analyst Agent] → Evaluates risk → Returns score (0-10)
        ↓
   [Dispatcher Agent] → If score ≥7 → CRITICAL ALERT
                      → If score <7 → Safe status
   ↓
[Final Summary] → Total scanned, Safe count, Critical count
```

### Multi-Agent Handoffs

1. **Config Agent** passes `suppliers.json` to monitoring phase
2. **Watchman Agent** passes `search_results` to Analyst
3. **Analyst Agent** passes `risk_data` to Dispatcher
4. **Dispatcher Agent** checks memory and sends alerts

## 🧠 Agentic Concepts Implemented

### 1. **Tool Usage** (Google Search Grounding)
```python
self.search_tool = types.Tool(
    google_search=types.GoogleSearch()
)
```
Watchman Agent uses native Google Search to find real-time supply chain news.

### 2. **Memory/State Persistence**
```python
self.alert_history = self._load_history()  # From alert_history.json
```
Prevents duplicate alerts using persistent file-based memory.

### 3. **Multi-Agent Handshakes**
```python
news = watchman_agent(material, location)
risk_data = analyst_agent(material, location, news)
dispatcher_agent(material, location, risk_data)
```
Agents pass context to each other in a pipeline.

### 4. **Autonomous Decision Making**
```python
if score >= 7:  # Dispatcher's autonomous threshold
    send_critical_alert()
```
Agents make decisions without human intervention.

### 5. **Long-Running Operations**
The system can run continuously in debug mode (single cycle) or 24/7 production mode.

## 📊 Example Output

### Web Interface Flow

```
🛡️ SupplySentinel
AI-Powered Multi-Agent Risk Monitoring

📝 Business Description
[Input: "I manufacture electric vehicles in California"]

[🎯 Analyze & Monitor Supply Chain]

🤖 Phase 1: Configuration Agent
✓ Supply Chain Mapped!
  Identified 3 critical dependencies

📊 Supply Chain Map
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ 📦 Lithium  │  │ 📦 Steel    │  │ 📦 Rubber   │
│ 📍 Chile    │  │ 📍 China    │  │ 📍 Thailand │
└─────────────┘  └─────────────┘  └─────────────┘

👁️ Phase 2: Watchman → Analyst → Dispatcher

📈 Real-Time Metrics
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Scanned │ │ ✓ Safe  │ │ ⚠ Crit  │ │Progress │
│    3    │ │    2    │ │    1    │ │  100%   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘

🔍 Risk Analysis Results

🚨 CRITICAL: Lithium
📍 Location:   Chile
⚠️ Risk Score: 8/10
📋 Reason:     Mining strikes affecting production
✉️ Dispatcher: Alert sent to procurement

✓ Steel from China
  Risk: 2/10 • No significant risks detected

✓ Rubber from Thailand
  Risk: 3/10 • Normal operations

✅ Multi-Agent Analysis Complete
   3 Dependencies Mapped  |  2 Safe  |  1 Critical
```

### Command-Line Output

```bash
$ python supply_sentinel.py

🟢 SupplySentinel Active. Monitoring Global Chains...

🔍 Watchman scanning: Lithium in Chile...
📊 Analyst evaluating risk...

🚨 🚨 CRITICAL ALERT: Lithium Supply Chain Risk!
   -> Location: Chile
   -> Score: 8/10
   -> Reason: Mining strikes affecting lithium production
   -> [Sent Email to Procurement Team]

💤 Cycle complete. Sleeping for 24 hours...
```

## 🎓 Technical Details

### Technology Stack
- **AI Model**: Google Gemini 2.5 Flash
- **SDK**: `google-genai` v1.0+
- **Search**: Native Google Search Grounding
- **UI**: Streamlit with custom CSS
- **Backend**: Python 3.9+
- **State**: JSON file-based persistence

### API Configuration
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)
model_id = "gemini-2.5-flash"

# Enable Google Search
search_tool = types.Tool(
    google_search=types.GoogleSearch()
)
```

### Agent Prompts

**Config Agent:**
```
Based on: "I manufacture solar panels in Arizona", 
identify the top 3 likely supply chain dependencies.
Return as JSON: [{"material": "...", "location": "..."}]
```

**Watchman Agent:**
```
Find recent logistics, weather, or political news 
affecting {material} supply from {location}.
Focus on strikes, shortages, or natural disasters.
```

**Analyst Agent:**
```
CONTEXT: You are a Supply Chain Risk Officer.
INPUT DATA: {search_results}
TASK: Analyze risk for {material} from {location}.
OUTPUT: risk_score (0-10), reason (1 sentence), action_needed
```

## ☁️ Cloud Deployment

Deploy to Google Cloud Run with one command:

```bash
# Build and deploy
gcloud run deploy supplysent --source . --allow-unauthenticated
```

See [README_DEPLOY.md](README_DEPLOY.md) for complete instructions.

**Benefits:**
- Serverless scaling
- HTTPS by default
- No infrastructure management
- Pay-per-use pricing
- Global availability

## 🏆 Competition Compliance

### ✅ Required Features
- [x] **Google Search Tool Integration**: Native `GoogleSearch()` in Watchman Agent
- [x] **Multi-Agent Architecture**: 4 specialized agents with handoffs
- [x] **Persistent Memory**: `alert_history.json` for deduplication
- [x] **Autonomous Decision Making**: Risk threshold filtering
- [x] **Long-Running Operation**: Continuous monitoring loop
- [x] **Gemini 2.5 Flash**: Latest stable model

### 🎁 Bonus Features
- [x] **Premium Web Interface**: Enterprise-grade Streamlit UI
- [x] **One-Click Workflow**: Complete flow in single interaction
- [x] **Real-Time Dashboards**: Live metrics and progress
- [x] **Cloud Deployment Ready**: Production-ready with Docker
- [x] **Visual Supply Chain Maps**: Intuitive dependency display
- [x] **Responsive Design**: Mobile and desktop support

## 📝 Configuration Files

### suppliers.json (Auto-generated)
```json
[
  {
    "material": "Lithium",
    "location": "Chile"
  },
  {
    "material": "Steel",
    "location": "China"
  },
  {
    "material": "Rubber",
    "location": "Thailand"
  }
]
```

### alert_history.json (Agent Memory)
```json
[
  "Lithium-Chile-2025-11-21",
  "Steel-China-2025-11-20"
]
```

### .env (API Key Storage)
```
GEMINI_API_KEY=your_api_key_here
```

## 🐛 Troubleshooting

**Issue**: "API Key not found"
```bash
# Solution: Set environment variable or create .env file
echo "GEMINI_API_KEY=your_key" > .env
```

**Issue**: "No module named 'google.genai'"
```bash
# Solution: Install latest google-genai SDK
pip install google-genai>=1.0.0
```

**Issue**: "Search tool not working"
```bash
# Solution: Ensure you're using gemini-2.5-flash (not 1.5)
# Check in code: model_id = "gemini-2.5-flash"
```

**Issue**: Streamlit not starting
```bash
# Solution: Install streamlit
pip install streamlit
streamlit run app.py
```

## 📚 Resources

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Google Search Grounding Guide](https://ai.google.dev/docs/grounding)
- [Deployment Guide](README_DEPLOY.md)

## 📄 License

MIT License - Feel free to use for your supply chain protection needs!

## 🙏 Acknowledgments

Built for the **Google x Kaggle Agents Intensive Capstone Project**  
Enterprise Track - November 2025

---

**⭐ Ready to protect your supply chain? Run `streamlit run app.py` and experience the future of autonomous risk monitoring!**
