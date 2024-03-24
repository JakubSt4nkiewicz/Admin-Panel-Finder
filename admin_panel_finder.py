# Importowanie niezbędnych modułów
import requests
import socket
from urllib.parse import urlparse
 
# Wyświetlanie powitalnego baneru dla użytkownika
print(
    """
   █████████      █████              ███              ███████████                        ████     ██████████████              █████                 
  ███░░░░░███    ░░███              ░░░              ░░███░░░░░███                      ░░███    ░░███░░░░░░░░░              ░░███                  
 ░███    ░███  ████████████████████ ████████████      ░███    ░████████ ████████   ██████░███     ░███   █ ░████████████   ███████  ██████ ████████ 
 ░███████████ ███░░██░░███░░███░░██░░██░░███░░███     ░█████████░░░░░██░░███░░███ ███░░██░███     ░███████ ░░██░░███░░███ ███░░███ ███░░██░░███░░███
 ░███░░░░░███░███ ░███░███ ░███ ░███░███░███ ░███     ░███░░░░░░ ███████░███ ░███░███████░███     ░███░░░█  ░███░███ ░███░███ ░███░███████ ░███ ░░░ 
 ░███    ░███░███ ░███░███ ░███ ░███░███░███ ░███     ░███      ███░░███░███ ░███░███░░░ ░███     ░███  ░   ░███░███ ░███░███ ░███░███░░░  ░███     
 █████   ████░░████████████░███ ████████████ █████    █████    ░░███████████ ████░░███████████    █████     ████████ ████░░███████░░██████ █████    
░░░░░   ░░░░░ ░░░░░░░░░░░░ ░░░ ░░░░░░░░░░░░ ░░░░░    ░░░░░      ░░░░░░░░░░░ ░░░░░ ░░░░░░░░░░░    ░░░░░     ░░░░░░░░ ░░░░░ ░░░░░░░░ ░░░░░░ ░░░░░     
    """
)


# Funkcja do normalizacji adresu URL, dodaje protokół HTTP jeśli nie został żaden podany
# oraz usuwa końcowy ukośnik, jeśli istnieje
def modify_url(url):
    # Rozbijamy adres url na składowe
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "http://" + url
    # Jeżeli url zawiera na końcu znak '/' to jest on usuwany
    if url.endswith("/"):
        url = url[:-1]
    return url


# Funkcja do wyszukiwania panelu administracyjnego
def find_admin_panel(url):
    try:
        url = modify_url(url)
        parsed_url = urlparse(url)
        # Wyświetlanie adresu IP wprowadzonej strony
        ip_address = socket.gethostbyname(parsed_url.netloc)
        print(f"IP address of {url}: {ip_address}")

        # Wczytanie listy ścieżek do paneli administracyjnych z pliku .txt
        with open("admin_directories.txt", "r") as file:
            common_paths = file.read().splitlines()

        # Sprawdzenie każdej z możliwych ścieżek w celu znalezienia panelu administracyjnego
        for path in common_paths:
            admin_url = url + path
            response = requests.get(admin_url)
            if response.status_code == 200:
                return f"Found admin panel: {admin_url}"
        return "Admin panel not found"
    except ValueError as e:
        print(f"Value error: {e}")
    except requests.RequestException as e:
        return f"Request error: {e}"
    except socket.gaierror as e:
        return f"Socket error: {e}"


# Główna funkcja main programu
def main():
    url = input("Podaj adres URL strony: ")
    print(find_admin_panel(url))


if __name__ == "__main__":
    main()
