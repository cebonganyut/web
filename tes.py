import requests

def load_proxies_from_file(filename):
    """Load proxies from a text file and return a list of proxies."""
    try:
        with open(filename, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        if not proxies:
            raise ValueError("File tidak mengandung proxy yang valid.")
        return proxies
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} tidak ditemukan.")
    except ValueError as e:
        raise ValueError(f"Error saat membaca file: {e}")

def test_proxy(proxy):
    """Test the provided proxy by making a request to httpbin."""
    url = 'http://httpbin.org/ip'  # URL untuk menguji proxy
    
    try:
        ip, port = proxy.split(':')
        proxy_dict = {
            'http': f'http://{ip}:{port}',
            'https': f'http://{ip}:{port}'
        }
        response = requests.get(url, proxies=proxy_dict, timeout=10)
        print(f"Response dari {url} dengan proxy {proxy}: {response.text}")
    except Exception as e:
        print(f"Error dengan proxy {proxy}: {str(e)}")

def main():
    filename = 'proxy_list.txt'
    try:
        proxies = load_proxies_from_file(filename)
        print(f"Berhasil memuat {len(proxies)} proxy dari {filename}.")
        
        for proxy in proxies:
            print(f"Uji proxy: {proxy}")
            test_proxy(proxy)
    
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
