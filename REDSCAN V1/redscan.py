import socket
import subprocess
import requests
import time
import sys

def banner():
    print("2024 THEMERT28, bu tool sonucunda başınıza geleceklerden sorumlu değilim ve eğitim amaçlı yapılmıştır\n")

def ip_port_scan():
    target = input("IP adresini girin: ")
    try:
        for port in range(1, 100):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"Port {port}: Açık")
            sock.close()
    except KeyboardInterrupt:
        print("\nTarama kullanıcı tarafından iptal edildi.")
        sys.exit()
    except socket.gaierror:
        print("Hostname çözümlenemedi.")
        sys.exit()
    except socket.error:
        print("Bağlantı hatası.")
        sys.exit()

def cloudflare_scan():
    domain = input("Taramak istediğiniz site adresini girin: ")
    try:
        response = requests.get(f"https://www.cloudflare.com/ips-v4?callback=ip&format=text&hostname={domain}")
        if response.status_code == 200:
            ips = response.text.splitlines()
            print(f"{domain} Cloudflare IP adresleri:")
            for ip in ips:
                print(ip)
        else:
            print("Cloudflare IP adresleri alınamadı.")
    except requests.exceptions.RequestException:
        print("İstek hatası.")
        sys.exit()

def sql_test():
    url = input("Test etmek istediğiniz site adresini girin: ")
    payloads = ["' or 1=1 --", "' or 'a'='a"]
    try:
        for payload in payloads:
            r = requests.get(url + "/?id=" + payload)
            if payload in r.text:
                print(f"SQL Injection açığı bulundu: {payload}")
                return
        print("SQL Injection açığı bulunamadı.")
    except requests.exceptions.RequestException:
        print("İstek hatası.")
        sys.exit()

def ip_check():
    domain = input("IP'sini öğrenmek istediğiniz site adresini girin: ")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{domain} IP adresi: {ip}")
    except socket.gaierror:
        print("Hostname çözümlenemedi.")
        sys.exit()

def ping_measure():
    target = input("Ping ölçmek istediğiniz site adresini veya IP adresini girin: ")
    try:
        result = subprocess.run(['ping', '-c', '4', target], capture_output=True, text=True)
        print(result.stdout)
    except subprocess.SubprocessError:
        print("Ping hatası.")
        sys.exit()

def geoip_info():
    ip = input("Geo-IP bilgisini almak istediğiniz IP adresini girin: ")
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            print(f"IP: {data['ip']}")
            print(f"Konum: {data['city']}, {data['region']}, {data['country']}")
            print(f"ASN: {data['org']}")
        else:
            print("Geo-IP bilgisi alınamadı.")
    except requests.exceptions.RequestException:
        print("İstek hatası.")
        sys.exit()

def server_load_test():
    target = input("Hedef IP adresini girin: ")
    port = int(input("Hedef port numarasını girin: "))
    duration = int(input("Test süresini saniye cinsinden girin: "))

    # Test başlangıcı
    print(f"Server yük testi {target}:{port} adresine başlatılıyor...")

    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            # İstemciye herhangi bir veri göndermeye gerek yok, sadece bağlantı kurulması yeterli
            sock.close()
            print(f"Bağlantı kuruldu: {target}:{port}")
            time.sleep(1)  # Her bağlantı arasında 1 saniye bekleyin
    except KeyboardInterrupt:
        print("\nTest kullanıcı tarafından iptal edildi.")
    except socket.error as e:
        print(f"Hata: {e}")

def main():
    banner()
    while True:
        print("\nSECİMİNİ YAP\n"
              "[1]: IP Açık Port Görüntüle\n"
              "[2]: Site Cloudflare Taraması Yap\n"
              "[3]: Site SQL Testi Yap\n"
              "[4]: Site IP Kontrol Et\n"
              "[5]: Site Ping Ölç\n"
              "[6]: GEO-IP Bilgisi Görüntüle\n"
              "[7]: DDOS Attack Başlat\n"
              "[q]: Çıkış\n")
        choice = input("Seçiminiz (1/2/3/4/5/6/7/q): ")

        if choice == '1':
            ip_port_scan()
        elif choice == '2':
            cloudflare_scan()
        elif choice == '3':
            sql_test()
        elif choice == '4':
            ip_check()
        elif choice == '5':
            ping_measure()
        elif choice == '6':
            geoip_info()
        elif choice == '7':
            server_load_test()
        elif choice.lower() == 'q':
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçenek. Tekrar deneyin.")

if __name__ == "__main__":
    main()
