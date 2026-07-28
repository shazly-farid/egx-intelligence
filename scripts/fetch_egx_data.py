#!/usr/bin/env python3
"""
Fetch Egyptian Exchange (EGX) announcements and data.
"""

import json
import requests
import argparse
from datetime import datetime
from typing import List, Dict

def fetch_egx_announcements(api_key: str) -> List[Dict]:
    """
    Fetch EGX announcements using Serper API.
    """
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    query = "site:egx.com.eg announcements news"
    url = "https://google.serper.dev/search"
    params = {
        "q": query,
        "num": 50,
        "type": "news"
    }
    
    try:
        response = requests.post(url, headers=headers, json=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        announcements = []
        for result in data.get("news", []):
            announcements.append({
                "source": "EGX",
                "title": result.get("title"),
                "link": result.get("link"),
                "date": result.get("date"),
                "snippet": result.get("snippet"),
                "timestamp": datetime.now().isoformat()
            })
        
        return announcements
    except requests.exceptions.RequestException as e:
        print(f"Error fetching EGX data: {e}")
        return []

def fetch_egx_indices() -> List[Dict]:
    """
    Fetch EGX index data (EGX30, EGX70, EGX100).
    """
    try:
        # Note: This would require scraping or API access to EGX official website
        # For now, returning placeholder structure
        indices = [
            {
                "name": "EGX30",
                "type": "index",
                "source": "EGX",
                "timestamp": datetime.now().isoformat()
            },
            {
                "name": "EGX70",
                "type": "index",
                "source": "EGX",
                "timestamp": datetime.now().isoformat()
            },
            {
                "name": "EGX100",
                "type": "index",
                "source": "EGX",
                "timestamp": datetime.now().isoformat()
            }
        ]
        return indices
    except Exception as e:
        print(f"Error fetching EGX indices: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Fetch EGX announcements and data")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--api-key", required=True, help="Serper API key")
    
    args = parser.parse_args()
    
    print("Fetching EGX announcements...")
    announcements = fetch_egx_announcements(args.api_key)
    
    print("Fetching EGX indices...")
    indices = fetch_egx_indices()
    
    egx_data = {
        "announcements": announcements,
        "indices": indices,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(egx_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ EGX data saved to {args.output}")
    print(f"  - {len(announcements)} announcements")
    print(f"  - {len(indices)} indices")

if __name__ == "__main__":
    main()
