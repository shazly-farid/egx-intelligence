#!/usr/bin/env python3
"""
Generate daily EGX intelligence report in Markdown format.
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List

def generate_report_header(date: str) -> str:
    """
    Generate report header and metadata.
    """
    header = f"""# Daily EGX Intelligence Report
**Date:** {date}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S Cairo Time')}

---

## Executive Summary

This daily intelligence report provides comprehensive analysis of Egyptian Exchange (EGX) market signals, regulatory updates from the Financial Regulatory Authority (FRA), and significant financial news affecting the Egyptian market.

"""
    return header

def generate_trading_signals_section(analysis: Dict) -> str:
    """
    Generate trading signals section.
    """
    trading_signals = analysis.get("trading_signals", [])
    
    section = "## Trading Signals\n\n"
    
    if trading_signals:
        for signal in trading_signals:
            signal_type = signal.get("type", "UNKNOWN")
            confidence = signal.get("confidence", "")
            reason = signal.get("reason", "")
            
            emoji = "🟢" if signal_type == "BUY" else "🔴" if signal_type == "SELL" else "🟡" if signal_type == "HOLD" else "⚠️"
            
            section += f"### {emoji} {signal_type}\n"
            section += f"**Confidence:** {confidence}  \n"
            section += f"**Reason:** {reason}\n\n"
    else:
        section += "No trading signals generated.\n\n"
    
    return section

def generate_egx_signals_section(analysis: Dict) -> str:
    """
    Generate EGX market signals section.
    """
    egx_signals = analysis.get("egx_signals", {})
    summary = analysis.get("summary", {})
    
    section = "## EGX Market Signals\n\n"
    
    bullish = egx_signals.get("bullish", [])
    bearish = egx_signals.get("bearish", [])
    neutral = egx_signals.get("neutral", [])
    
    section += f"### Signal Overview\n"
    section += f"- 🟢 **Bullish Signals:** {len(bullish)}\n"
    section += f"- 🔴 **Bearish Signals:** {len(bearish)}\n"
    section += f"- 🟡 **Neutral Signals:** {len(neutral)}\n\n"
    
    if bullish:
        section += "### Bullish Announcements\n"
        for signal in bullish[:5]:  # Show top 5
            section += f"- **{signal.get('title', 'N/A')}** (Strength: {signal.get('strength', 'N/A')})\n"
        if len(bullish) > 5:
            section += f"- ... and {len(bullish) - 5} more\n"
        section += "\n"
    
    if bearish:
        section += "### Bearish Announcements\n"
        for signal in bearish[:5]:  # Show top 5
            section += f"- **{signal.get('title', 'N/A')}** (Strength: {signal.get('strength', 'N/A')})\n"
        if len(bearish) > 5:
            section += f"- ... and {len(bearish) - 5} more\n"
        section += "\n"
    
    return section

def generate_fra_signals_section(analysis: Dict) -> str:
    """
    Generate FRA regulatory signals section.
    """
    fra_signals = analysis.get("fra_signals", {})
    
    section = "## Regulatory Updates (FRA)\n\n"
    
    regulatory_changes = fra_signals.get("regulatory_changes", [])
    compliance_alerts = fra_signals.get("compliance_alerts", [])
    market_measures = fra_signals.get("market_measures", [])
    
    if regulatory_changes:
        section += "### Regulatory Changes\n"
        for item in regulatory_changes[:3]:
            section += f"- **{item.get('title', 'N/A')}** ({item.get('date', 'N/A')})\n"
        if len(regulatory_changes) > 3:
            section += f"- ... and {len(regulatory_changes) - 3} more\n"
        section += "\n"
    
    if compliance_alerts:
        section += "### Compliance Alerts\n"
        for item in compliance_alerts[:3]:
            section += f"- **{item.get('title', 'N/A')}** ({item.get('date', 'N/A')})\n"
        if len(compliance_alerts) > 3:
            section += f"- ... and {len(compliance_alerts) - 3} more\n"
        section += "\n"
    
    if market_measures:
        section += "### Market Measures\n"
        for item in market_measures[:3]:
            section += f"- **{item.get('title', 'N/A')}** ({item.get('date', 'N/A')})\n"
        if len(market_measures) > 3:
            section += f"- ... and {len(market_measures) - 3} more\n"
        section += "\n"
    
    if not (regulatory_changes or compliance_alerts or market_measures):
        section += "No significant regulatory updates today.\n\n"
    
    return section

def generate_news_signals_section(analysis: Dict) -> str:
    """
    Generate financial news signals section.
    """
    news_signals = analysis.get("news_signals", {})
    
    section = "## Financial News & Market Impact\n\n"
    
    high_impact = news_signals.get("high_impact", [])
    medium_impact = news_signals.get("medium_impact", [])
    
    if high_impact:
        section += "### 🔴 High Impact News\n"
        for item in high_impact[:5]:
            source = item.get("source", "Unknown")
            title = item.get("title", "N/A")
            section += f"- **{title}** *(Source: {source})*\n"
        if len(high_impact) > 5:
            section += f"- ... and {len(high_impact) - 5} more\n"
        section += "\n"
    
    if medium_impact:
        section += "### 🟡 Medium Impact News\n"
        for item in medium_impact[:3]:
            source = item.get("source", "Unknown")
            title = item.get("title", "N/A")
            section += f"- **{title}** *(Source: {source})*\n"
        if len(medium_impact) > 3:
            section += f"- ... and {len(medium_impact) - 3} more\n"
        section += "\n"
    
    if not (high_impact or medium_impact):
        section += "No significant financial news today.\n\n"
    
    return section

def generate_comparison_section(analysis: Dict) -> str:
    """
    Generate comparison with previous report section.
    """
    comparison = analysis.get("comparison", {})
    
    section = "## Day-over-Day Analysis\n\n"
    
    if comparison.get("previous_report_found"):
        section += "✓ Previous report found and analyzed for trend comparison.\n\n"
    else:
        section += "⚠️ Previous report not found. This is the first report or comparison data unavailable.\n\n"
    
    return section

def generate_footer(analysis: Dict) -> str:
    """
    Generate report footer with metadata.
    """
    summary = analysis.get("summary", {})
    
    footer = f"""---

## Report Statistics

| Metric | Value |
|--------|-------|
| Bullish Signals | {summary.get('total_bullish', 0)} |
| Bearish Signals | {summary.get('total_bearish', 0)} |
| Neutral Signals | {summary.get('total_neutral', 0)} |
| High Impact News | {summary.get('high_impact_news', 0)} |
| Regulatory Changes | {summary.get('regulatory_changes', 0)} |

---

## Disclaimer

This report is for informational purposes only and should not be construed as investment advice. The analysis is based on available public information and market signals. Past performance does not guarantee future results. Please consult with a qualified financial advisor before making any investment decisions.

**Report Generated By:** EGX Intelligence Bot  
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    return footer

def main():
    parser = argparse.ArgumentParser(description="Generate daily EGX intelligence report")
    parser.add_argument("--analysis", required=True, help="Analysis JSON file")
    parser.add_argument("--date", required=True, help="Report date (YYYY-MM-DD)")
    parser.add_argument("--output", required=True, help="Output report markdown file")
    
    args = parser.parse_args()
    
    # Load analysis
    print("Loading analysis data...")
    with open(args.analysis, 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # Generate report sections
    print("Generating report...")
    report = ""
    
    report += generate_report_header(args.date)
    report += generate_trading_signals_section(analysis)
    report += generate_egx_signals_section(analysis)
    report += generate_fra_signals_section(analysis)
    report += generate_news_signals_section(analysis)
    report += generate_comparison_section(analysis)
    report += generate_footer(analysis)
    
    # Save report
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✓ Report generated: {args.output}")
    print(f"  - {len(report)} characters")
    print(f"  - {len(report.splitlines())} lines")

if __name__ == "__main__":
    main()
