import re
import requests
import base64
import os
import json
import socket
import struct
import uuid

CONFIG_FILE = "config_kstar3.json"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print("\033[1;35m" + "="*62)
    print("  ██╗  ██╗    ██████╗████████╗ █████╗ ██████╗     ██████╗ ")
    print("  ██║ ██╔╝    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ╚════██╗")
    print("  █████╔╝     ╚█████╗    ██║   ███████║██████╔╝     █████╔╝")
    print("  ██╔═██╗      ╚═══██╗   ██║   ██╔══██║██╔══██╗     ╚═══██╗")
    print("  ██║  ██╗    ██████╔╝   ██║   ██║  ██║██║  ██║    ██████╔╝")
    print("  ╚═╝  ╚═╝    ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ")
    print("="*62 + "\033[0m")
    print("\033[1;36m                   မင်္ဂလာပါ - K star 3 Project\033[0m")
    print("\033[1;32m               Developer: RSHO KA | @K_star3\033[0m")
    print("\033[1;35m" + "="*62 + "\033[0m")

# Network Auto Detection Functions
def get_gateway_ip():
    try:
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if len(fields) > 2 and fields[1] == '00000000':
                    return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
    except Exception:
        pass
    try:
        import subprocess
        out = subprocess.check_output(["ip", "route"], stderr=subprocess.DEVNULL).decode()
        match = re.search(r"default via ([\d.]+)", out)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "192.168.22.1" # Fallback

def get_local_mac():
    try:
        mac_num = uuid.getnode()
        mac = ':'.join(['{:02x}'.format((mac_num >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])
        return mac
    except Exception:
        return "1a:10:98:62:df:64" # Fallback

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.22.25" # Fallback

def update_url_params(url, new_mac, new_gw, new_ip):
    url = re.sub(r'(?<=mac=)[^&]+', new_mac, url)
    url = re.sub(r'(?<=gw_address=)[^&]+', new_gw, url)
    url = re.sub(r'(?<=ip=)[^&]+', new_ip, url)
    return url

def replace_mac(url, new_mac):
    url = re.sub(r'(?<=mac=)[^&]+', new_mac, url)       
    return url

def get_session_id(session_url, mac_address):
    final_url = replace_mac(session_url, mac_address)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': final_url,
        'sec-ch-ua': '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'cookie':'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fgemini.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTllMGRkYmQ5ZjIxNTItMGRmOTQxZjJlZmM2YjA4LTRjNjU3YjU4LTEzMjcxMDQtMTllMGRkYmQ5ZjNhNjAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219e0ddbd9f2152-0df941f2efc6b08-4c657b58-1327104-19e0ddbd9f3a60%22%7D'
    }
    
    try:
        response = requests.get(final_url, headers=headers)
        session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response.url).group(1)
        return session_id
    except Exception as e:
        print(f"\033[1;31m[-] Error Getting Session ID: {e}\033[0m")
        return None

def login_voucher(session_id, voucher):
    data = {
        "accessCode": voucher,
        "sessionId": session_id,
        "apiVersion": 1
    }
    post_url = base64.b64decode(b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3ZvdWNoZXIvP2xhbmc9ZW5fVVM=').decode()
    headers = {
        "authority": "portal-as.ruijienetworks.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId={session_id}",
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": 'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        with requests.post(post_url, json=data, headers=headers) as response:
            res_text = response.text
            return re.search('token=(.*?)&', res_text).group(1)
    except Exception as Error:
        print(f"\033[1;31m[-] Voucher Login Error: {Error}\033[0m")
        return None
    
def start_bypass():
    clear_screen()
    banner()
    
    # ၎င်းနေရာတွင် အသုံးပြုလိုသော URL အသေကို ထည့်သွင်းထားပါတယ်
    base_url = "https://portal-as.ruijienetworks.com/api/auth/wifidog?stage=portal&gw_id=c4b25becb273&gw_sn=H1U408M001189&gw_address=192.168.22.1&gw_port=2060&ip=192.168.22.25&mac=1a:10:98:62:df:64&slot_num=14&nasip=192.168.1.136&ssid=VLAN22&ustate=0&mac_req=1&url=http%3A%2F%2F192.168.0.1%2F&chap_id=%5C076&chap_challenge=%5C165%5C064%5C213%5C340%5C354%5C220%5C217%5C164%5C042%5C361%5C153%5C216%5C215%5C051%5C335%5C035"
    
    print("\033[1;33m[*] Network Information များကို Auto ရှာဖွေနေပါသည်...\033[0m")
    gateway_ip = get_gateway_ip()
    mac_address = get_local_mac()
    local_ip = get_local_ip()
    
    print(f"\033[1;34m[ Detected Gateway IP  ]: {gateway_ip}\033[0m")
    print(f"\033[1;34m[ Detected MAC Address ]: {mac_address}\033[0m")
    print(f"\033[1;34m[ Detected Local IP    ]: {local_ip}\033[0m")
    print("\033[1;35m" + "-"*40 + "\033[0m")
    
    # Voucher Code တစ်ခုတည်းကိုသာ ကိုယ်တိုင်ထည့်သွင်းရန် တောင်းဆိုခြင်း
    voucher = input("\033[1;32m=> Voucher Code ထည့်ပါ: \033[0m").strip()

    if not voucher:
        print("\033[1;31m[-] Voucher Code မရှိဘဲ ဆက်လုပ်၍မရပါ။\033[0m")
        input("\nGo back to menu..."); return

    # URL ထဲရှိ တန်ဖိုးများကို Auto ရှာဖွေထားသော အချက်အလက်များနှင့် အစားထိုးခြင်း
    session_url = update_url_params(base_url, mac_address, gateway_ip, local_ip)
    
    print("\n\033[1;33m[*] Processing Bypass, Please wait...\033[0m")
    
    session_id = get_session_id(session_url, mac_address)
    print(f"[+] Inactive Session Id: {session_id}")
    
    if not session_id:
        input("\nBypass Failed to get Session ID. Press Enter..."); return
        
    active_session_id = login_voucher(session_id, voucher)
    print(f"[+] Active Session Id: {active_session_id}")
    
    if not active_session_id:
        input("\nBypass Failed to active voucher. Press Enter..."); return

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    params = {
        'token': active_session_id,
        'phoneNumber': 'Kstar3User',
    }
    
    try:
        final_req_url = f'http://{gateway_ip}:2060/wifidog/auth?'
        response_url = requests.get(final_req_url, params=params, headers=headers).url
        
        success_conditions = [
            "http://www.baidu.com", 
            "http://www.baidu.com/", 
            "http://portal-as.ruijienetworks.com/download/static/maccauth/src/success.html?",
            "success"
        ]
        
        if any(cond in response_url for cond in success_conditions):
            print("\n\033[1;32m[✓] Internet Bypass Successful! Enjoy your internet.\033[0m")
        else:
            print("\n\033[1;31m[-] Internet Bypass Failed or Unknown Response Route.\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m[-] Auth Gateway connection error: {e}\033[0m")
        
    input("\nPress Enter to back to menu...")

def main_menu():
    while True:
        clear_screen()
        banner()
        print("\033[1;33m[ Main Menu Options ]\033[0m")
        print(" [1] Start WiFi Bypass")
        print(" [2] Reset Saved Data (Clear Cache)")
        print(" [3] Exit Tool")
        print("\033[1;35m"+"-"*62+"\033[0m")
        
        choice = input("\033[1;32m=> ရွေးချယ်မှုအမှတ်စဉ် ထည့်ပါ: \033[0m").strip()
        
        if choice == "1":
            start_bypass()
        elif choice == "2":
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
                print("\033[1;32m[✓] Saved Data Cleared Successfully!\033[0m")
            else:
                print("\033[1;33m[!] No data saved yet.\033[0m")
            input("\nPress Enter to continue...")
        elif choice == "3":
            print("\n\033[1;36mGood Bye! See you again.\033[0m")
            break
        else:
            print("\033[1;31m[-] မှားယွင်းနေပါသည်။ နံပါတ် ၁ မှ ၃ အတွင်းသာ ရွေးပေးပါ။\033[0m")
            input("\nPress Enter to try again...")

if __name__ == "__main__":
    main_menu()
