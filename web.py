import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import logging
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_file(filename):
    """Load lines from a file and return a list of non-empty lines."""
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File {filename} tidak ditemukan.{Style.RESET_ALL}")
        return []

def simulate_user_behavior(session, url, user_agent):
    """Simulate realistic user behavior on a given URL."""
    try:
        # Initial page visit
        response = session.get(url, timeout=30)
        if response.status_code == 200:
            print(f"{Fore.GREEN}Berhasil mengunjungi {url} - Status: {response.status_code}{Style.RESET_ALL}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Simulate scrolling and time on site
            time.sleep(random.uniform(5, 15))
            
            # Click on a random link
            links = soup.find_all('a', href=True)
            if links:
                random_link = random.choice(links)['href']
                random_link = urljoin(url, random_link)  # Resolve relative URLs
                print(f"{Fore.GREEN}Berhasil mengklik link: {random_link}{Style.RESET_ALL}")
                session.get(random_link, timeout=30)
                
            # Simulate more time on site
            time.sleep(random.uniform(10, 30))
        else:
            print(f"{Fore.RED}Gagal mengunjungi {url} - Status: {response.status_code}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Error saat mensimulasikan perilaku pengguna pada {url}: {str(e)}{Style.RESET_ALL}")

def parse_residential_proxy(proxy_string):
    """
    Parse residential proxy string in format username:password@hostname:port
    Returns a dictionary with proxy details
    """
    try:
        # Split credentials and host:port
        auth, host_port = proxy_string.split('@')
        username, password = auth.split(':')
        hostname, port = host_port.split(':')
        
        return {
            'username': username,
            'password': password,
            'hostname': hostname,
            'port': port
        }
    except ValueError:
        print(f"{Fore.RED}Error: Format proxy tidak valid: {proxy_string}{Style.RESET_ALL}")
        return None

def visit_url(url, proxies, user_agents):
    """Set up a session with random proxy and user agent, then visit the URL."""
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url

    proxy_details = parse_residential_proxy(random.choice(proxies))
    if not proxy_details:
        return
    
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
        proxy_dict = {
            'http': f'http://{proxy_details["username"]}:{proxy_details["password"]}@{proxy_details["hostname"]}:{proxy_details["port"]}',
            'https': f'https://{proxy_details["username"]}:{proxy_details["password"]}@{proxy_details["hostname"]}:{proxy_details["port"]}'
        }
        
        session = requests.Session()
        session.headers.update(headers)
        session.proxies.update(proxy_dict)
        simulate_user_behavior(session, url, user_agent)
    except Exception as e:
        print(f"{Fore.RED}Error saat menyiapkan sesi untuk {url}: {str(e)}{Style.RESET_ALL}")

def main():
    proxies = load_file('proxy_list.txt')
    urls = load_file('url_list.txt')
    user_agents = load_file('user_agent_list.txt')
    
    if not all([proxies, urls, user_agents]):
        print(f"{Fore.RED}Error: Satu atau lebih file input kosong atau hilang.{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}Berhasil memuat {len(proxies)} proxy, {len(urls)} URL, dan {len(user_agents)} user agent.{Style.RESET_ALL}")
    
    while True:
        try:
            max_workers = int(input("Masukkan jumlah ThreadPoolExecutor (1-10): "))
            if 1 <= max_workers <= 10:
                break
            else:
                print(f"{Fore.YELLOW}Mohon masukkan angka antara 1 dan 10.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.YELLOW}Mohon masukkan angka yang valid.{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}Menggunakan {max_workers} ThreadPoolExecutor.{Style.RESET_ALL}")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            random.shuffle(urls)
            for url in urls:
                executor.submit(visit_url, url, proxies, user_agents)
                time.sleep(random.uniform(30, 60))  # Longer delay between requests

if __name__ == "__main__":
    main()
