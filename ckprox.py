import requests
import threading
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Warna
pink = Fore.MAGENTA
reset = Style.RESET_ALL
green = Fore.GREEN
cyan = Fore.CYAN

# Variabel global
http_checked = 0
valid_http = []
output_lock = threading.Lock()

def get_time_rn():
    return time.strftime("%H:%M:%S", time.localtime())

def check_proxy(proxy):
    global http_checked
    proxy_dict = {
        "http": "http://" + proxy,
        "https": "https://" + proxy
    }
    try:
        url = 'http://httpbin.org/get'
        r = requests.get(url, proxies=proxy_dict, timeout=30)
        if r.status_code == 200:
            with output_lock:
                time_rn = get_time_rn()
                print(f"[ {pink}{time_rn}{reset} ] | ( {green}VALID{reset} ) HTTP/S --> {cyan}{proxy}{reset}")
            valid_http.append(proxy)
            with output_lock:
                http_checked += 1
            with open(os.path.join("Results", "http.txt"), "a+") as f:
                f.write(proxy + "\n")
    except:
        with output_lock:
            time_rn = get_time_rn()
            print(f"[ {pink}{time_rn}{reset} ] | ( {Fore.RED}INVALID{reset} ) HTTP/S --> {proxy}")
        with output_lock:
            http_checked += 1

def load_proxies(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    global http_checked

    # Membuat direktori Results jika belum ada
    if not os.path.exists("Results"):
        os.makedirs("Results")

    proxies = load_proxies('proxy_list.txt')
    total_proxies = len(proxies)

    print(f"{Fore.CYAN}Loaded {total_proxies} proxies.{reset}")

    max_workers = 50 # Anda bisa menyesuaikan jumlah thread sesuai kebutuhan
    print(f"{Fore.CYAN}Using {max_workers} threads for checking.{reset}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(check_proxy, proxies)

    print(f"\n{Fore.GREEN}Checking completed!{reset}")
    print(f"Total proxies checked: {http_checked}")
    print(f"Valid HTTP/S proxies: {len(valid_http)}")
    print(f"Results saved in Results/http.txt")

if __name__ == "__main__":
    main()
