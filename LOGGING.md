# SupplySentinel Logging Documentation

## Overview

SupplySentinel includes professional-grade structured logging across all four agents (Config, Watchman, Analyst, Dispatcher) to provide comprehensive observability for both development and production environments.

## Log Format

All logs follow a consistent structured format:

```
YYYY-MM-DD HH:MM:SS [LEVEL] [Agent.AgentName] — Message
```

**Example:**
```
2024-01-15 14:32:45 [INFO] [Agent.Config] — Dependency mapping complete — 3 dependencies extracted
2024-01-15 14:32:47 [CRITICAL] [Agent.Analyst] — Risk score computed: 9/10 — CRITICAL threat level for Steel in China
```

## Log Levels

### DEBUG
Low-level diagnostic information, useful for troubleshooting specific issues.

**Examples:**
- `Dependency mapping initiated`
- `Initiating search for Steel in China`
- `Risk analysis initiated for Steel in China`
- `Duplicate alert suppressed: Steel-China-2024-01-15`

### INFO
General informational messages about normal operations.

**Examples:**
- `Dependency mapping complete — 3 dependencies extracted`
- `Search returned 12 data points for Steel in China`
- `Risk score computed: 3/10 — NORMAL threat level for Steel in China`
- `Cycle complete — Scanned: 3 | Safe: 2 | Critical: 1 | Skipped: 0`

### WARNING
Potentially problematic situations that don't prevent operation.

**Examples:**
- `Insufficient data for analysis: Steel in China`
- `Risk score computed: 6/10 — ELEVATED threat level for Steel in China`

### ERROR
Error events that might still allow operation to continue.

**Examples:**
- `Error generating suppliers: Connection timeout`
- `Search failed for Steel in China: API rate limit exceeded`
- `Analysis failed for Steel in China: Invalid JSON response`

### CRITICAL
Very severe error events that require immediate attention.

**Examples:**
- `Risk score computed: 9/10 — CRITICAL threat level for Steel in China`
- `Critical alert sent — Steel-China — Score: 9/10 — Reason: Factory shutdown due to earthquake`

## Agent-Specific Logging

### Config Agent
Logs dependency mapping and configuration activities.

**Key Messages:**
- `Dependency mapping initiated` (DEBUG)
- `Dependency mapping complete — X dependencies extracted` (INFO)
- `Error generating suppliers: <error>` (ERROR)
- `Successfully saved X suppliers to suppliers.json` (INFO)

### Watchman Agent
Logs search operations and data collection activities.

**Key Messages:**
- `Initiating search for {material} in {location}` (DEBUG)
- `Search returned X data points for {material} in {location}` (INFO)
- `Search failed for {material} in {location}: <error>` (ERROR)

### Analyst Agent
Logs risk analysis and scoring operations.

**Key Messages:**
- `Risk analysis initiated for {material} in {location}` (DEBUG)
- `Risk score computed: X/10 — NORMAL threat level` (INFO, score < 5)
- `Risk score computed: X/10 — ELEVATED threat level` (WARNING, 5 ≤ score < 7)
- `Risk score computed: X/10 — CRITICAL threat level` (CRITICAL, score ≥ 7)
- `Insufficient data for analysis: {material} in {location}` (WARNING)
- `Analysis failed for {material} in {location}: <error>` (ERROR)

### Dispatcher Agent
Logs alert decisions and deduplication activities.

**Key Messages:**
- `Critical alert sent — {material}-{location} — Score: X/10 — Reason: <reason>` (CRITICAL)
- `Risk monitored (non-critical) — {material}-{location} — Score: X/10` (INFO)
- `Duplicate alert suppressed: {alert_id}` (DEBUG)
- `No significant risks detected for {material} in {location}` (INFO)
- `Cycle complete — Scanned: X | Safe: Y | Critical: Z | Skipped: W` (INFO)

## Deployment Modes

### Streamlit/Cloud Run (Web Interface)

Logs are sent to **stdout** for Cloud Run to capture:

```python
from logging_config import setup_logging
setup_logging(environment="streamlit")
```

**Viewing Logs on Cloud Run:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=supply-sentinel" --limit 50 --format json
```

### CLI Mode (Continuous Monitoring)

Logs are written to both **stdout** and **rotating log files**:

```python
from logging_config import setup_logging
setup_logging(environment="cli")
```

**Log File Location:** `logs/supplysentinel.log`

**Rotation Settings:**
- Max file size: 10 MB
- Backup count: 5 files
- Total max storage: ~50 MB

**Viewing Logs:**
```bash
# View latest logs
tail -f logs/supplysentinel.log

# Search for critical alerts
grep "CRITICAL" logs/supplysentinel.log

# View errors only
grep "ERROR" logs/supplysentinel.log

# Count alerts by severity
grep -c "INFO" logs/supplysentinel.log
grep -c "WARNING" logs/supplysentinel.log
grep -c "ERROR" logs/supplysentinel.log
grep -c "CRITICAL" logs/supplysentinel.log
```

## Monitoring & Analysis

### Real-Time Monitoring

**Watch for critical alerts:**
```bash
tail -f logs/supplysentinel.log | grep "CRITICAL"
```

**Monitor cycle completions:**
```bash
tail -f logs/supplysentinel.log | grep "Cycle complete"
```

### Historical Analysis

**Find all alerts for a specific material:**
```bash
grep "Steel" logs/supplysentinel.log | grep "CRITICAL"
```

**Count total alerts in last 24 hours:**
```bash
grep "Critical alert sent" logs/supplysentinel.log | grep "$(date +%Y-%m-%d)"
```

**View error patterns:**
```bash
grep "ERROR" logs/supplysentinel.log | cut -d']' -f3 | sort | uniq -c
```

## Integration Examples

### Custom Monitoring Script

```python
import re
from datetime import datetime

def count_alerts_today():
    today = datetime.now().strftime('%Y-%m-%d')
    critical_count = 0
    
    with open('logs/supplysentinel.log', 'r') as f:
        for line in f:
            if today in line and '[CRITICAL]' in line and 'Critical alert sent' in line:
                critical_count += 1
    
    return critical_count

if __name__ == "__main__":
    alerts = count_alerts_today()
    print(f"Critical alerts today: {alerts}")
```

### Log Analysis with pandas

```python
import pandas as pd
import re
from datetime import datetime

def parse_log_file(filepath):
    records = []
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] \[Agent\.(\w+)\] — (.+)'
    
    with open(filepath, 'r') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                timestamp, level, agent, message = match.groups()
                records.append({
                    'timestamp': datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
                    'level': level,
                    'agent': agent,
                    'message': message
                })
    
    return pd.DataFrame(records)

# Usage
df = parse_log_file('logs/supplysentinel.log')
print(df.groupby(['agent', 'level']).size())
```

## Best Practices

1. **Set appropriate log levels**: Use DEBUG for development, INFO for production
2. **Monitor disk usage**: Log rotation prevents disk space issues
3. **Archive old logs**: Backup log files before they're rotated out
4. **Alert on critical logs**: Set up monitoring to notify on CRITICAL level messages
5. **Regular review**: Check logs weekly for patterns or recurring errors
6. **Keep logs secure**: Logs may contain sensitive supply chain information

## Troubleshooting

### No logs appearing

**Check logging configuration:**
```python
import logging
print(logging.getLogger().level)  # Should show 10 (DEBUG) or 20 (INFO)
print(logging.getLogger().handlers)  # Should show console and/or file handlers
```

### Log file not created

**Ensure logs directory exists:**
```bash
mkdir -p logs
```

**Check file permissions:**
```bash
ls -la logs/
```

### Excessive log volume

**Increase log level to WARNING:**
```python
import logging
logging.getLogger().setLevel(logging.WARNING)
```

## Configuration Reference

**Default Configuration** (`logging_config.py`):

```python
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] — %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGS_DIR = "logs"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5
```

**Adjust settings:**
```python
from logging_config import setup_logging
import logging

# Custom setup with different log level
setup_logging(environment="cli")
logging.getLogger().setLevel(logging.WARNING)  # Only show warnings and above
```
