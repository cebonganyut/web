import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def simulate_user_behavior(session, url, user_agent):
    try:
        # Initial page visit
        response = session.get(url, timeout=30)
        if response.status_code == 200:
            print(f"{Fore.GREEN}Berhasil mengunjungi {url} - Status: {response.status_code}{Style.RESET_ALL}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Simulate scrolling
            time.sleep(random.uniform(5, 15))
            
            # Click on a random link
            links = soup.find_all('a', href=True)
            if links:
                random_link = random.choice(links)['href']
                if not random_link.startswith(('http://', 'https://')):
                    random_link = urlparse(url)._replace(path=random_link).geturl()
                print(f"{Fore.GREEN}Berhasil mengklik link: {random_link}{Style.RESET_ALL}")
                session.get(random_link, timeout=30)
                
            # Simulate more time on site
            time.sleep(random.uniform(10, 30))
        else:
            print(f"{Fore.RED}Gagal mengunjungi {url} - Status: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saat mensimulasikan perilaku pengguna pada {url}: {str(e)}{Style.RESET_ALL}")

def check_proxy(proxy):
    try:
        ip, port = proxy.split(':')
        proxy_dict = {
            'http': f'http://{ip}:{port}',
            'https': f'https://{ip}:{port}'
        }
        response = requests.get('http://httpbin.org/ip', proxies=proxy_dict, timeout=10)
        if response.status_code == 200:
            return True
        return False
    except:
        return False

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
        ip, port = proxy.split(':')
        proxy_dict = {
            'http': f'http://{ip}:{port}',
            'https': f'https://{ip}:{port}'
        }
        
        session = requests.Session()
        session.headers.update(headers)
        session.proxies.update(proxy_dict)
        
        # Test koneksi proxy
        test_url = 'http://httpbin.org/ip'
        response = session.get(test_url, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.GREEN}Proxy {proxy} berhasil terhubung.{Style.RESET_ALL}")
            print(f"IP terdeteksi: {response.json()['origin']}")
        
        simulate_user_behavior(session, url, user_agent)
    except requests.exceptions.ProxyError as e:
        print(f"{Fore.RED}Error proxy untuk {proxy}: {str(e)}{Style.RESET_ALL}")
    except requests.exceptions.ConnectTimeout:
        print(f"{Fore.RED}Timeout saat menghubungi proxy {proxy}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error request untuk {url} menggunakan proxy {proxy}: {str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error tidak terduga saat menggunakan {proxy} untuk {url}: {str(e)}{Style.RESET_ALL}")

def visit_url_with_retry(url, proxies, user_agents, max_retries=3):
    for _ in range(max_retries):
        try:
            visit_url(url, proxies, user_agents)
            break
        except Exception as e:
            print(f"{Fore.YELLOW}Gagal, mencoba lagi... ({str(e)}){Style.RESET_ALL}")
            time.sleep(5)
    else:
        print(f"{Fore.RED}Gagal setelah {max_retries} percobaan untuk {url}{Style.RESET_ALL}")

def main():
    proxies = load_file('proxy_list.txt')
    urls = load_file('url_list.txt')
    user_agents = load_file('user_agent_list.txt')
    
    if not all([proxies, urls, user_agents]):
        print(f"{Fore.RED}Error: Satu atau lebih file input kosong atau hilang.{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}Berhasil memuat {len(proxies)} proxy, {len(urls)} URL, dan {len(user_agents)} user agent.{Style.RESET_ALL}")
    
    valid_proxies = [proxy for proxy in proxies if check_proxy(proxy)]
    print(f"{Fore.CYAN}Ditemukan {len(valid_proxies)} proxy valid dari {len(proxies)} total.{Style.RESET_ALL}")
    if not valid_proxies:
        print(f"{Fore.RED}Tidak ada proxy valid. Program berhenti.{Style.RESET_ALL}")
        return
    
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
                executor.submit(visit_url_with_retry, url, valid_proxies, user_agents)
                time.sleep(random.uniform(30, 60))  # Longer delay between requests

if __name__ == "__main__":
    main()
