#!/usr/bin/env python3
"""
Fetch financial news from multiple Egyptian and Arab financial news sources.
"""

import json
import requests
import argparse
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup

def fetch_mubasher_news() -> List[Dict]:
    """
    Fetch news from Mubasher (Bloomberg Arabic).
    """
    news = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        url = "https://www.mubasher.info/stocks/EG"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse news items
        for item in soup.find_all('div', class_='news-item'):
            try:
                title = item.find('a', class_='news-title')
                date = item.find('span', class_='news-date')
                
                if title:
                    news.append({
                        "source": "Mubasher",
                        "title": title.get_text(),
                        "link": title.get('href', ''),
                        "date": date.get_text() if date else "Unknown",
                        "category": "market",
                        "timestamp": datetime.now().isoformat()
                    })
            except:
                continue
    except requests.exceptions.RequestException as e:
        print(f"Warning: Error fetching Mubasher news: {e}")
    
    return news

def fetch_arabfinance_news() -> List[Dict]:
    """
    Fetch news from Arab Finance.
    """
    news = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        url = "https://www.arabfinance.com/en"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse news items
        for item in soup.find_all('article'):
            try:
                title = item.find('h2') or item.find('h3')
                link = item.find('a')
                date = item.find('time') or item.find('span', class_='date')
                
                if title and link:
                    news.append({
                        "source": "Arab Finance",
                        "title": title.get_text(),
                        "link": link.get('href', ''),
                        "date": date.get_text() if date else "Unknown",
                        "category": "financial",
                        "timestamp": datetime.now().isoformat()
                    })
            except:
                continue
    except requests.exceptions.RequestException as e:
        print(f"Warning: Error fetching Arab Finance news: {e}")
    
    return news

def fetch_alborsa_news() -> List[Dict]:
    """
    Fetch news from Al-Borsa (Egyptian financial newspaper).
    """
    news = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        url = "https://www.alborsa.com"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse news items
        for item in soup.find_all('div', class_='story'):
            try:
                title = item.find('a', class_='story-title') or item.find('a')
                date = item.find('span', class_='story-date')
                
                if title:
                    news.append({
                        "source": "Al-Borsa",
                        "title": title.get_text(),
                        "link": title.get('href', ''),
                        "date": date.get_text() if date else "Unknown",
                        "category": "stocks",
                        "timestamp": datetime.now().isoformat()
                    })
            except:
                continue
    except requests.exceptions.RequestException as e:
        print(f"Warning: Error fetching Al-Borsa news: {e}")
    
    return news

def fetch_hapi_news() -> List[Dict]:
    """
    Fetch news from HAPI (Egyptian financial data provider).
    """
    news = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        url = "https://www.hapi.biz"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse news items
        for item in soup.find_all('div', class_='article'):
            try:
                title = item.find('h3') or item.find('h4')
                link = item.find('a')
                date = item.find('span', class_='date')
                
                if title and link:
                    news.append({
                        "source": "HAPI",
                        "title": title.get_text(),
                        "link": link.get('href', ''),
                        "date": date.get_text() if date else "Unknown",
                        "category": "market_data",
                        "timestamp": datetime.now().isoformat()
                    })
            except:
                continue
    except requests.exceptions.RequestException as e:
        print(f"Warning: Error fetching HAPI news: {e}")
    
    return news

def fetch_financial_news_aggregated(sources: List[str]) -> List[Dict]:
    """
    Aggregate financial news from multiple sources.
    """
    all_news = []
    
    source_handlers = {
        "mubasher": fetch_mubasher_news,
        "arab-finance": fetch_arabfinance_news,
        "al-borsa": fetch_alborsa_news,
        "hapi": fetch_hapi_news
    }
    
    for source in sources:
        if source in source_handlers:
            print(f"Fetching from {source}...")
            news = source_handlers[source]()
            all_news.extend(news)
    
    return all_news

def main():
    parser = argparse.ArgumentParser(description="Fetch financial news from multiple sources")
    parser.add_argument("--sources", default="mubasher,arab-finance,al-borsa,hapi", 
                        help="Comma-separated list of news sources")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    
    args = parser.parse_args()
    
    sources = [s.strip() for s in args.sources.split(",")]
    
    print("Fetching financial news...")
    news = fetch_financial_news_aggregated(sources)
    
    # Remove duplicates based on title
    unique_news = []
    seen_titles = set()
    for item in news:
        if item["title"] not in seen_titles:
            unique_news.append(item)
            seen_titles.add(item["title"])
    
    news_data = {
        "news": unique_news,
        "sources": sources,
        "total_count": len(unique_news),
        "timestamp": datetime.now().isoformat()
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(news_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Financial news saved to {args.output}")
    print(f"  - {len(unique_news)} unique articles")
    print(f"  - From {len(sources)} sources")

if __name__ == "__main__":
    main()
