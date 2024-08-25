import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

def load_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def visit_url(url, proxies, user_agents):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url

    proxy = random.choice(proxies)
    user_agent = random.choice(user_agents)
    
    headers = {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            proxies={'http': proxy, 'https': proxy},
            timeout=30,
            allow_redirects=True
        )
        print(f"Visited {url} - Status: {response.status_code}")
    except Exception as e:
        print(f"Error visiting {url}: {str(e)}")

def main():
    proxies = load_file('proxy_list.txt')
    urls = load_file('url_list.txt')
    user_agents = load_file('user_agent_list.txt')

    if not all([proxies, urls, user_agents]):
        print("Error: One or more input files are empty or missing.")
        return

    print(f"Loaded {len(proxies)} proxies, {len(urls)} URLs, and {len(user_agents)} user agents.")

    with ThreadPoolExecutor(max_workers=30) as executor:
        while True:
            random.shuffle(urls)
            for url in urls:
                executor.submit(visit_url, url, proxies, user_agents)
                time.sleep(random.uniform(3, 7))  # Random delay between requests

if __name__ == "__main__":
    main()
