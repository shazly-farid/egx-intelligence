# EGX Intelligence System

A comprehensive Python-based intelligence system for monitoring, analyzing, and reporting on the Egyptian Exchange (EGX) market, with real-time data fetching from multiple sources including EGX announcements, FRA regulatory updates, and financial news.

## Overview

The EGX Intelligence System provides automated daily intelligence reports combining:

- **EGX Announcements**: Listed company announcements and market data
- **FRA Regulatory Updates**: Financial Regulatory Authority compliance and regulatory announcements
- **Financial News**: Real-time financial news from Egyptian and Arab financial sources
- **Signal Analysis**: Automated sentiment analysis and trading signal generation
- **Daily Reports**: Professional markdown reports with actionable trading signals

## Features

✨ **Key Features:**

- 🔄 **Multi-Source Data Aggregation** - Fetch from EGX, FRA, and 4+ financial news sources
- 📊 **Automated Signal Analysis** - Sentiment analysis and trading signal generation
- 📈 **Trend Comparison** - Day-over-day analysis comparing signals and market movements
- 📋 **Professional Reports** - Daily markdown reports with statistics and recommendations
- 🔗 **Modular Architecture** - Separate scripts for each data source and analysis function
- 🎯 **Configurable Pipeline** - Customize data sources, analysis parameters, and report generation
- 📧 **Extensible** - Easy to add new sources, analysis methods, or reporting formats

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   run_pipeline.py (Orchestrator)             │
│              Coordinates all pipeline steps                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐        ┌─────────┐       ┌──────────┐
   │ EGX     │        │ FRA     │       │ Financial│
   │ Data    │        │ Data    │       │ News     │
   │ Fetcher │        │ Fetcher │       │ Fetcher  │
   └────┬────┘        └────┬────┘       └────┬─────┘
        │                  │                 │
        └──────────────────┼────────────────┘
                           │
                   ┌───────▼────────┐
                   │ Signal         │
                   │ Analyzer       │
                   └───────┬────────┘
                           │
                   ┌───────▼────────┐
                   │ Report         │
                   │ Generator      │
                   └────────────────┘
```

## Scripts

### 1. `fetch_egx_announcements.py`
Fetches announcements from the Egyptian Exchange.

```bash
python3 scripts/fetch_egx_announcements.py --output data/egx_announcements.json
```

**Output**: JSON file with EGX announcements including:
- Title and summary
- Announcement date
- Listed company information
- Link to full announcement

### 2. `fetch_fra_announcements.py`
Fetches regulatory announcements from the Financial Regulatory Authority.

```bash
python3 scripts/fetch_fra_announcements.py --output data/fra_announcements.json
```

**Output**: JSON file with FRA announcements including:
- Regulatory changes and compliance requirements
- Market measures and trading halts
- Effective dates and compliance deadlines

### 3. `fetch_financial_news.py`
Aggregates financial news from multiple Egyptian and Arab sources.

```bash
python3 scripts/fetch_financial_news.py \
  --sources mubasher,arab-finance,al-borsa,hapi \
  --output data/financial_news.json
```

**Supported Sources**:
- **Mubasher**: Bloomberg Arabic market data and news
- **Arab Finance**: Middle East financial news and analysis
- **Al-Borsa**: Egyptian financial newspaper
- **HAPI**: Egyptian financial data provider

### 4. `analyze_signals.py`
Analyzes fetched data to generate trading signals and market insights.

```bash
python3 scripts/analyze_signals.py \
  --egx-data data/egx_announcements.json \
  --fra-data data/fra_announcements.json \
  --news-data data/financial_news.json \
  --output data/analysis.json \
  --previous-report reports/report_2026-07-27.md
```

**Output**: JSON file containing:
- Bullish/Bearish/Neutral signals
- Regulatory impact analysis
- News sentiment analysis
- Trading recommendations (BUY/SELL/HOLD)
- Day-over-day trend comparison

### 5. `generate_report.py`
Generates professional daily intelligence reports in Markdown format.

```bash
python3 scripts/generate_report.py \
  --analysis data/analysis.json \
  --date 2026-07-28 \
  --output reports/report_2026-07-28.md
```

**Report Sections**:
- Executive Summary
- Trading Signals with confidence levels
- EGX Market Signals (Bullish/Bearish/Neutral breakdown)
- Regulatory Updates from FRA
- Financial News Impact Analysis
- Day-over-Day Comparison
- Statistical Summary
- Disclaimer

### 6. `run_pipeline.py`
Main orchestration script that coordinates all steps of the pipeline.

```bash
# Run complete pipeline
python3 scripts/run_pipeline.py

# Run specific steps
python3 scripts/run_pipeline.py --steps fetch_egx,fetch_fra,analyze,report

# Use custom directories
python3 scripts/run_pipeline.py --data-dir /data --reports-dir /reports
```

**Pipeline Steps** (in order):
1. `fetch_egx` - Fetch EGX announcements
2. `fetch_fra` - Fetch FRA announcements
3. `fetch_news` - Fetch financial news
4. `analyze` - Analyze signals
5. `report` - Generate report
6. `summary` - Create execution summary

## Installation

### Requirements

- Python 3.7+
- Required packages:
  - `requests` - HTTP requests for web scraping
  - `beautifulsoup4` - HTML parsing
  - `lxml` - XML/HTML processing

### Setup

```bash
# Clone the repository
git clone https://github.com/shazly-farid/egx-intelligence.git
cd egx-intelligence

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data reports logs
```

## Usage

### Basic Usage - Run Complete Pipeline

```bash
python3 scripts/run_pipeline.py
```

This will:
1. Fetch data from all sources
2. Analyze signals
3. Generate daily report
4. Create execution summary

### Daily Scheduled Execution

Set up a cron job to run daily at 8:00 AM Cairo time:

```bash
# Open crontab editor
crontab -e

# Add this line (runs at 8:00 AM Egypt timezone)
0 8 * * * cd /path/to/egx-intelligence && python3 scripts/run_pipeline.py >> logs/pipeline.log 2>&1
```

### Using Configuration

Customize behavior via `config.ini`:

```ini
[analysis]
bullish_threshold = 0.6
bearish_threshold = 0.4

[email]
enabled = true
recipients = investor@example.com
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "scripts/run_pipeline.py"]
```

## Output Structure

```
project/
├── data/
│   ├── egx_announcements_2026-07-28.json
│   ├── fra_announcements_2026-07-28.json
│   ├── financial_news_2026-07-28.json
│   └── analysis_2026-07-28.json
├── reports/
│   ├── report_2026-07-28.md
│   └── summary_2026-07-28.json
└── logs/
    └── egx_intelligence.log
```

## Example Report

Sample daily report includes:

```markdown
# Daily EGX Intelligence Report
**Date:** 2026-07-28
**Generated:** 2026-07-28 08:15:32 Cairo Time

## Trading Signals
### 🟢 BUY
**Confidence:** HIGH
**Reason:** Bullish signals with high-impact news convergence

### ⚠️ CAUTION
**Confidence:** HIGH
**Reason:** Market measures announced: 2 items

## EGX Market Signals
### Signal Overview
- 🟢 **Bullish Signals:** 12
- 🔴 **Bearish Signals:** 3
- 🟡 **Neutral Signals:** 5
```

## Signal Analysis

### Bullish Signals
Generated when announcements contain keywords:
- profit, growth, increase, surge, rally, gain

### Bearish Signals
Generated when announcements contain keywords:
- loss, decline, fall, drop, crash, weakness

### Trading Recommendations

| Signal | Condition | Action |
|--------|-----------|--------|
| BUY | More bullish than bearish + high-impact news | Strong buy signal |
| SELL | More bearish than bullish + high-impact news | Strong sell signal |
| HOLD | Mixed signals | Wait for clarity |
| CAUTION | Market measures or regulatory changes | Risk alert |

## Configuration Reference

See `config.ini` for all available options:

- **Fetching**: Timeout, retry attempts, user agent
- **EGX**: Data sources and parameters
- **FRA**: Regulatory source configuration
- **News**: Multiple news source settings
- **Analysis**: Signal thresholds and parameters
- **Reporting**: Report generation options
- **Email**: Optional email notifications
- **Logging**: Log levels and file management
- **Database**: Future database integration

## Troubleshooting

### Network Errors
If data fetching fails:
```bash
# Check internet connection
ping www.google.com

# Increase timeout in config.ini
timeout = 20

# Verify source URLs are accessible
```

### Missing Data
If a data source returns empty:
```bash
# Check source availability
# Review logs for specific errors
tail -f logs/egx_intelligence.log

# Run individual fetch script for debugging
python3 scripts/fetch_egx_announcements.py --output test.json
```

### Report Generation Issues
```bash
# Ensure analysis file exists
ls -la data/analysis_*.json

# Check JSON format
python3 -m json.tool data/analysis_2026-07-28.json
```

## Contributing

Contributions are welcome! To add new features:

1. Create a new script in `scripts/` directory
2. Update `run_pipeline.py` to include new step
3. Add configuration options to `config.ini`
4. Update documentation

## Disclaimer

⚠️ **Important Legal Notice**

This system is for informational purposes only and should not be construed as investment advice. The analysis is based on available public information and automated signal processing. 

**Past performance does not guarantee future results.** Please consult with a qualified financial advisor before making any investment decisions.

The authors and contributors of this project are not responsible for any financial losses resulting from the use of this system.

## License

This project is open source. See LICENSE file for details.

## Support

For issues, questions, or suggestions:

1. **GitHub Issues**: Report bugs and request features
2. **Documentation**: Check README and config.ini for details
3. **Logs**: Review `logs/egx_intelligence.log` for debugging

## Roadmap

🔮 **Planned Features**:

- [ ] Database integration for historical data
- [ ] Real-time WebSocket data streaming
- [ ] Advanced ML sentiment analysis
- [ ] Interactive web dashboard
- [ ] Email/SMS notifications
- [ ] Mobile app integration
- [ ] Multi-language support
- [ ] REST API for external integrations

## Related Projects

- [EGX Official Website](https://www.egx.com.eg)
- [FRA Official Website](https://www.fra.gov.eg)
- [Mubasher Financial Data](https://www.mubasher.info)

---

**Last Updated**: July 28, 2026  
**Version**: 1.0.0  
**Author**: EGX Intelligence Team
