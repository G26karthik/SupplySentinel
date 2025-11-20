"""
SupplySentinel Logging Configuration
Professional-grade structured logging for all agents
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from collections import deque

# Log format with timestamp, level, agent name, and message
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] — %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Ensure logs directory exists
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# In-memory log storage for Streamlit UI (last 500 logs)
_log_buffer = deque(maxlen=500)

class StreamlitLogHandler(logging.Handler):
    """Custom handler to capture logs for Streamlit UI display"""
    def emit(self, record):
        log_entry = self.format(record)
        _log_buffer.append({
            'timestamp': datetime.fromtimestamp(record.created),
            'level': record.levelname,
            'agent': record.name.replace('Agent.', ''),
            'message': record.getMessage(),
            'full_text': log_entry
        })

def get_recent_logs(limit=100):
    """Get recent logs for UI display"""
    return list(_log_buffer)[-limit:]

def clear_log_buffer():
    """Clear in-memory log buffer"""
    _log_buffer.clear()

def setup_logging(environment="streamlit"):
    """
    Configure logging for SupplySentinel
    
    Args:
        environment: "streamlit" for Cloud Run (stdout only) or "cli" for file-based logging
    """
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler (stdout) - always enabled
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Streamlit UI handler (in-memory buffer for web display)
    if environment == "streamlit":
        streamlit_handler = StreamlitLogHandler()
        streamlit_handler.setLevel(logging.DEBUG)
        streamlit_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        streamlit_handler.setFormatter(streamlit_formatter)
        root_logger.addHandler(streamlit_handler)
    
    # File handler for CLI mode only
    if environment == "cli":
        file_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, "supplysentinel.log"),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

def get_agent_logger(agent_name):
    """
    Get a logger for a specific agent
    
    Args:
        agent_name: Name of the agent (Config, Watchman, Analyst, Dispatcher)
    
    Returns:
        Logger instance configured for the agent
    """
    return logging.getLogger(f"Agent.{agent_name}")

# Create loggers for each agent
config_logger = get_agent_logger("Config")
watchman_logger = get_agent_logger("Watchman")
analyst_logger = get_agent_logger("Analyst")
dispatcher_logger = get_agent_logger("Dispatcher")
