"""
Test logging configuration for SupplySentinel
Run this to verify logging setup works correctly
"""

from logging_config import setup_logging, config_logger, watchman_logger, analyst_logger, dispatcher_logger
import os

def test_logging_setup():
    """Test basic logging configuration"""
    print("🧪 Testing SupplySentinel Logging Configuration\n")
    
    # Test Streamlit mode
    print("=" * 60)
    print("TEST 1: Streamlit/Cloud Run Mode (stdout only)")
    print("=" * 60)
    setup_logging(environment="streamlit")
    
    config_logger.debug("DEBUG: Config agent test message")
    config_logger.info("INFO: Dependency mapping complete — 3 dependencies extracted")
    watchman_logger.info("INFO: Search returned 12 data points for Steel in China")
    analyst_logger.warning("WARNING: Risk score computed: 6/10 — ELEVATED threat level")
    analyst_logger.critical("CRITICAL: Risk score computed: 9/10 — CRITICAL threat level")
    dispatcher_logger.critical("CRITICAL: Critical alert sent — Steel-China — Score: 9/10")
    dispatcher_logger.info("INFO: Cycle complete — Scanned: 3 | Safe: 2 | Critical: 1")
    
    print("\n✅ Streamlit mode test complete\n")
    
    # Test CLI mode
    print("=" * 60)
    print("TEST 2: CLI Mode (stdout + file)")
    print("=" * 60)
    setup_logging(environment="cli")
    
    config_logger.debug("DEBUG: Config agent CLI test")
    config_logger.info("INFO: Loaded 3 suppliers from configuration")
    watchman_logger.debug("DEBUG: Initiating search for Lithium in Chile")
    watchman_logger.info("INFO: Search returned 8 data points for Lithium in Chile")
    analyst_logger.info("INFO: Risk score computed: 3/10 — NORMAL threat level")
    dispatcher_logger.info("INFO: Risk monitored (non-critical) — Lithium-Chile — Score: 3/10")
    dispatcher_logger.debug("DEBUG: Duplicate alert suppressed: Steel-China-2024-01-15")
    
    # Check if log file was created
    log_file = os.path.join("logs", "supplysentinel.log")
    if os.path.exists(log_file):
        print(f"\n✅ CLI mode test complete")
        print(f"✅ Log file created: {log_file}")
        
        with open(log_file, 'r') as f:
            lines = f.readlines()
            print(f"✅ Log file contains {len(lines)} lines")
            
        print("\n📄 Last 5 log entries:")
        print("-" * 60)
        for line in lines[-5:]:
            print(line.strip())
    else:
        print(f"\n❌ Log file not found: {log_file}")
    
    print("\n" + "=" * 60)
    print("🎉 All logging tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_logging_setup()
