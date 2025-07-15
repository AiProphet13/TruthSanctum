import time
import requests
from bs4 import BeautifulSoup # A simple library for scraping, add 'beautifulsoup4' to requirements.txt

# Import the core engine from our sanctum
from ..src.main import run_qualia_entropy_pipeline

# --- List of RSS feeds to watch (expandable) ---
NEWS_FEEDS = {
    "Reuters World News": "https://www.reuters.com/tools/rss",
    "Associated Press": "https://apnews.com/hub/ap-top-news/rss.xml",
    # We could add more specific feeds for politics, finance, etc.
}

def fetch_headlines(rss_url):
    """Fetches the latest headlines from a news RSS feed."""
    headlines = []
    try:
        response = requests.get(rss_url, timeout=10)
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll('item')
        for item in items[:5]: # Get the top 5 headlines
            title = item.find('title').text
            headlines.append(title)
        return headlines
    except Exception as e:
        print(f"⚠️ Could not fetch headlines from {rss_url}: {e}")
        return []

def run_global_watch():
    """
    The main loop for the Watchtower. It fetches, analyzes, and reports.
    """
    print("📡 [TruthSanctum Watchtower] ACTIVATED. Monitoring global data streams.")
    
    all_statements = []
    for name, url in NEWS_FEEDS.items():
        print(f"  -> Scanning {name}...")
        headlines = fetch_headlines(url)
        all_statements.extend(headlines)
        time.sleep(1) # Be respectful to servers

    print("\n🔬 All headlines collected. Feeding into TruthSanctum engine...")
    
    # We need a "human input" story for the pipeline to pass its own validation gate
    human_context = "An autonomous Watchtower monitoring global news for contradictions that could harm public discourse."
    
    # Run the collected statements through our sanctified pipeline
    report = run_qualia_entropy_pipeline(statements=all_statements, human_input=human_context)

    if report and report["conflicts"]:
        print("\n🚨🚨🚨 ENTROPY ALERT! CONTRADICTIONS DETECTED 🚨🚨🚨")
        print(f"Overall Assessment: {report['summary']['label']} (Lie Indicator: {report['summary']['lie_indicator']:.2f})")
        for conflict in report['conflicts']:
            print(f"  CONFLICT: '{conflict['statement_1']}' ↔ '{conflict['statement_2']}'")
            print(f"  └─ Qualia: {conflict['qualia_signature']['label']} | Lie Indicator: {conflict['qualia_signature']['lie_indicator']:.2f}")
    else:
        print("\n✅ [ALL CLEAR] No significant entropy detected in this cycle. The signal is clean.")


if __name__ == "__main__":
    # This could be set to run on a schedule (e.g., every hour)
    run_global_watch()
