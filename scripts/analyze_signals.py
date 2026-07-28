#!/usr/bin/env python3
"""
Analyze financial signals and compare with previous reports.
"""

import json
import argparse
from datetime import datetime
from typing import List, Dict, Any

def analyze_egx_signals(egx_data: Dict) -> Dict:
    """
    Analyze EGX announcements and indices for trading signals.
    """
    signals = {
        "bullish": [],
        "bearish": [],
        "neutral": []
    }
    
    # Analyze announcements
    announcements = egx_data.get("announcements", [])
    for announcement in announcements:
        title = announcement.get("title", "").lower()
        snippet = announcement.get("snippet", "").lower()
        
        # Simple sentiment analysis based on keywords
        bullish_keywords = ["profit", "growth", "increase", "surge", "rally", "gain"]
        bearish_keywords = ["loss", "decline", "fall", "drop", "crash", "weakness"]
        
        text = f"{title} {snippet}"
        
        bullish_count = sum(1 for keyword in bullish_keywords if keyword in text)
        bearish_count = sum(1 for keyword in bearish_keywords if keyword in text)
        
        if bullish_count > bearish_count:
            signals["bullish"].append({
                "type": "announcement",
                "title": announcement.get("title"),
                "strength": bullish_count,
                "timestamp": datetime.now().isoformat()
            })
        elif bearish_count > bullish_count:
            signals["bearish"].append({
                "type": "announcement",
                "title": announcement.get("title"),
                "strength": bearish_count,
                "timestamp": datetime.now().isoformat()
            })
        else:
            signals["neutral"].append({
                "type": "announcement",
                "title": announcement.get("title"),
                "timestamp": datetime.now().isoformat()
            })
    
    return signals

def analyze_fra_signals(fra_data: Dict) -> Dict:
    """
    Analyze FRA regulatory announcements for market impact signals.
    """
    signals = {
        "regulatory_changes": [],
        "compliance_alerts": [],
        "market_measures": []
    }
    
    announcements = fra_data.get("announcements", [])
    for announcement in announcements:
        title = announcement.get("title", "").lower()
        
        if "regulation" in title or "rule" in title:
            signals["regulatory_changes"].append({
                "title": announcement.get("title"),
                "date": announcement.get("date"),
                "timestamp": datetime.now().isoformat()
            })
        elif "compliance" in title or "requirement" in title:
            signals["compliance_alerts"].append({
                "title": announcement.get("title"),
                "date": announcement.get("date"),
                "timestamp": datetime.now().isoformat()
            })
        elif "trading" in title or "halt" in title or "suspension" in title:
            signals["market_measures"].append({
                "title": announcement.get("title"),
                "date": announcement.get("date"),
                "timestamp": datetime.now().isoformat()
            })
    
    return signals

def analyze_news_signals(news_data: Dict) -> Dict:
    """
    Analyze financial news for market sentiment signals.
    """
    signals = {
        "high_impact": [],
        "medium_impact": [],
        "low_impact": []
    }
    
    news_items = news_data.get("news", [])
    for item in news_items:
        title = item.get("title", "").lower()
        source = item.get("source", "")
        
        # Weighted impact based on keywords and source
        impact_keywords = {
            "merger": 3, "acquisition": 3, "ipo": 3, "bankruptcy": 3,
            "earnings": 2, "dividend": 2, "scandal": 2, "crisis": 2,
            "profit": 1, "announcement": 1, "update": 1
        }
        
        impact_score = 0
        for keyword, weight in impact_keywords.items():
            if keyword in title:
                impact_score += weight
        
        news_item = {
            "title": item.get("title"),
            "source": source,
            "date": item.get("date"),
            "impact_score": impact_score,
            "timestamp": datetime.now().isoformat()
        }
        
        if impact_score >= 3:
            signals["high_impact"].append(news_item)
        elif impact_score >= 2:
            signals["medium_impact"].append(news_item)
        else:
            signals["low_impact"].append(news_item)
    
    return signals

def compare_with_previous_report(current_analysis: Dict, previous_report_path: str = None) -> Dict:
    """
    Compare current analysis with previous report to identify trends.
    """
    comparison = {
        "new_signals": [],
        "resolved_signals": [],
        "ongoing_signals": [],
        "trend_analysis": {}
    }
    
    if previous_report_path:
        try:
            with open(previous_report_path, 'r', encoding='utf-8') as f:
                previous_content = f.read()
            # Simple comparison - in production would parse markdown/json
            comparison["previous_report_found"] = True
        except FileNotFoundError:
            comparison["previous_report_found"] = False
    else:
        comparison["previous_report_found"] = False
    
    return comparison

def generate_trading_signals(analysis: Dict) -> List[Dict]:
    """
    Generate actionable trading signals based on analysis.
    """
    signals = []
    
    egx_signals = analysis.get("egx_signals", {})
    fra_signals = analysis.get("fra_signals", {})
    news_signals = analysis.get("news_signals", {})
    
    # Generate signals based on signal convergence
    bullish_count = len(egx_signals.get("bullish", []))
    bearish_count = len(egx_signals.get("bearish", []))
    high_impact_count = len(news_signals.get("high_impact", []))
    
    if bullish_count > bearish_count and high_impact_count > 0:
        signals.append({
            "type": "BUY",
            "confidence": "HIGH",
            "reason": "Bullish signals with high-impact news convergence",
            "timestamp": datetime.now().isoformat()
        })
    elif bearish_count > bullish_count and high_impact_count > 0:
        signals.append({
            "type": "SELL",
            "confidence": "HIGH",
            "reason": "Bearish signals with high-impact news convergence",
            "timestamp": datetime.now().isoformat()
        })
    else:
        signals.append({
            "type": "HOLD",
            "confidence": "MEDIUM",
            "reason": "Mixed signals, recommend holding position",
            "timestamp": datetime.now().isoformat()
        })
    
    # Add regulatory signals
    if fra_signals.get("market_measures"):
        signals.append({
            "type": "CAUTION",
            "confidence": "HIGH",
            "reason": f"Market measures announced: {len(fra_signals.get('market_measures', []))} items",
            "timestamp": datetime.now().isoformat()
        })
    
    return signals

def main():
    parser = argparse.ArgumentParser(description="Analyze financial signals")
    parser.add_argument("--egx-data", required=True, help="EGX data JSON file")
    parser.add_argument("--fra-data", required=True, help="FRA data JSON file")
    parser.add_argument("--news-data", required=True, help="News data JSON file")
    parser.add_argument("--previous-report", help="Previous report markdown file for comparison")
    parser.add_argument("--output", required=True, help="Output analysis JSON file")
    
    args = parser.parse_args()
    
    # Load data files
    print("Loading data files...")
    with open(args.egx_data, 'r', encoding='utf-8') as f:
        egx_data = json.load(f)
    
    with open(args.fra_data, 'r', encoding='utf-8') as f:
        fra_data = json.load(f)
    
    with open(args.news_data, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    # Analyze signals
    print("Analyzing EGX signals...")
    egx_signals = analyze_egx_signals(egx_data)
    
    print("Analyzing FRA signals...")
    fra_signals = analyze_fra_signals(fra_data)
    
    print("Analyzing news signals...")
    news_signals = analyze_news_signals(news_data)
    
    # Compile analysis
    analysis = {
        "egx_signals": egx_signals,
        "fra_signals": fra_signals,
        "news_signals": news_signals
    }
    
    # Compare with previous report
    print("Comparing with previous report...")
    comparison = compare_with_previous_report(analysis, args.previous_report)
    analysis["comparison"] = comparison
    
    # Generate trading signals
    print("Generating trading signals...")
    trading_signals = generate_trading_signals(analysis)
    analysis["trading_signals"] = trading_signals
    
    # Add metadata
    analysis["timestamp"] = datetime.now().isoformat()
    analysis["summary"] = {
        "total_bullish": len(egx_signals.get("bullish", [])),
        "total_bearish": len(egx_signals.get("bearish", [])),
        "total_neutral": len(egx_signals.get("neutral", [])),
        "high_impact_news": len(news_signals.get("high_impact", [])),
        "regulatory_changes": len(fra_signals.get("regulatory_changes", []))
    }
    
    # Save analysis
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Analysis saved to {args.output}")
    print(f"  - {len(trading_signals)} trading signals generated")
    print(f"  - Bullish: {analysis['summary']['total_bullish']}, Bearish: {analysis['summary']['total_bearish']}")

if __name__ == "__main__":
    main()
