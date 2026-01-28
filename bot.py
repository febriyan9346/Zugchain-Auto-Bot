import requests
import time
import sys
import json
import os
import random
from datetime import datetime
import pytz
from web3 import Web3
from eth_account import Account
from colorama import Fore, Style, init

init(autoreset=True)

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    try:
        from web3.middleware import ExtraDataToPOAMiddleware as geth_poa_middleware
    except ImportError:
        geth_poa_middleware = None

RPC_URL = "https://rpc.zugchain.org"
CHAIN_ID = 824642
EXPLORER_URL = "https://explorer.zugchain.org"

STAKE_CONTRACT = "0x4ed9828ba8487b9160C820C8b72c573E74eBbD0A"
STAKE_METHOD_ID = "0xc9c11fa9" 
CLAIM_METHOD_ID = "0x379607f5"

URL_SYNC = "https://testnet.zugchain.org/api/user/sync"
URL_FAUCET = "https://testnet.zugchain.org/api/faucet"
URL_CAPTCHA_SITE = "https://testnet.zugchain.org/faucet"
URL_HISTORY = "https://testnet.zugchain.org/api/staking/history"
URL_CLAIM_SYNC = "https://testnet.zugchain.org/api/incentive/sync"
URL_PROFILE = "https://testnet.zugchain.org/api/incentive/profile"
SITE_KEY_CAPTCHA = "6Lerk04sAAAAAJqTuhkaScWwo6LaUPI1ogZXwYo0"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"

class ZugChainBot:
    def __init__(self):
        self.web3 = None
        self.use_proxy = False
        
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}ZUGCHAIN AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self):
        delay = random.randint(1, 10)
        time.sleep(delay)
    
    def get_headers(self, path):
        return {
            "authority": "testnet.zugchain.org",
            "method": "POST",
            "path": path,
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://testnet.zugchain.org",
            "referer": "https://testnet.zugchain.org/",
            "user-agent": USER_AGENT
        }

    def get_profile_headers(self):
        return {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "connection": "keep-alive",
            "host": "testnet.zugchain.org",
            "referer": "https://testnet.zugchain.org/mission-control",
            "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": USER_AGENT
        }

    def format_proxy(self, proxy):
        if not proxy or not proxy.strip(): 
            return None
        p = proxy.strip()
        if not p.startswith("http") and not p.startswith("socks"):
            return {"http": f"http://{p}", "https": f"http://{p}"}
        return {"http": p, "https": p}

    def get_address(self, pk):
        try:
            if not pk.startswith("0x"): 
                pk = "0x" + pk
            return Account.from_key(pk).address
        except: 
            return None

    def setup_web3(self, proxies_list):
        request_kwargs = {
            'headers': {'User-Agent': USER_AGENT, 'Content-Type': 'application/json'}, 
            'timeout': 30
        }
        if proxies_list:
            formatted_proxy = self.format_proxy(proxies_list[0])
            if formatted_proxy:
                request_kwargs['proxies'] = formatted_proxy

        provider = Web3.HTTPProvider(RPC_URL, request_kwargs=request_kwargs)
        web3 = Web3(provider)
        
        if geth_poa_middleware:
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return web3 if web3.is_connected() else None

    def get_total_stakes_count(self, address, proxy):
        proxies = self.format_proxy(proxy)
        try:
            timestamp = f"{time.time()}_{random.random()}"
            params = {"address": address, "type": "ZUG", "_t": timestamp}
            headers = self.get_headers("/api/staking/history")
            headers["method"] = "GET"
            res = requests.get(URL_HISTORY, params=params, headers=headers, proxies=proxies, timeout=15)
            if res.status_code == 200:
                data = res.json()
                staked_events = [item for item in data if item.get("event_type") == "STAKED"]
                return len(staked_events)
            return 0
        except: return 0

    def get_profile(self, address, proxy):
        proxies = self.format_proxy(proxy)
        try:
            params = {"address": address}
            headers = self.get_profile_headers()
            res = requests.get(URL_PROFILE, params=params, headers=headers, proxies=proxies, timeout=15)
            if res.status_code == 200:
                data = res.json()
                return data
            return None
        except: 
            return None

    def run_login(self, address, proxy):
        proxies = self.format_proxy(proxy)
        try:
            res = requests.post(URL_SYNC, json={"address": address, "referralCode": None}, headers=self.get_headers("/api/user/sync"), proxies=proxies, timeout=15)
            if res.status_code in [200, 201]:
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful!{Style.RESET_ALL}")
                return True
            else:
                self.log(f"Login failed: {res.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Login error: {str(e)}", "ERROR")
            return False

    def solve_2captcha(self, api_key):
        self.log("Solving Captcha...", "INFO")
        try:
            payload = {
                "clientKey": api_key,
                "task": {
                    "type": "RecaptchaV2TaskProxyless",
                    "websiteURL": URL_CAPTCHA_SITE,
                    "websiteKey": SITE_KEY_CAPTCHA
                }
            }
            req = requests.post("https://api.2captcha.com/createTask", json=payload, timeout=20).json()
            if req.get("errorId") != 0: return None
            task_id = req.get("taskId")
            while True:
                time.sleep(5)
                res = requests.post("https://api.2captcha.com/getTaskResult", json={"clientKey": api_key, "taskId": task_id}, timeout=20).json()
                if res.get("status") == "ready": return res.get("solution", {}).get("gRecaptchaResponse")
                if res.get("errorId") != 0: return None
        except: return None

    def run_faucet(self, address, proxy, captcha_key):
        self.log("Processing Faucet:", "INFO")
        token = self.solve_2captcha(captcha_key)
        if not token:
            self.log("Captcha failed, skip faucet", "WARNING")
            return
        try:
            res = requests.post(URL_FAUCET, json={"address": address, "recaptchaToken": token, "referralCode": None}, headers=self.get_headers("/api/faucet"), proxies=self.format_proxy(proxy), timeout=30)
            if res.status_code == 200 and res.json().get("success"):
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Faucet Success! +{res.json().get('amount')} ZUG{Style.RESET_ALL}")
            else:
                self.log(f"Faucet Failed: {res.text}", "WARNING")
        except: pass

    def run_stake(self, web3, private_key, address, amount_ether):
        if not web3: return 
        self.log(f"Processing Stake: {amount_ether} ZUG", "INFO")
        try:
            amount_wei = web3.to_wei(amount_ether, 'ether')
            balance = web3.eth.get_balance(address)
            if balance < (amount_wei + web3.to_wei(0.001, 'ether')):
                self.log("Insufficient balance", "ERROR")
                return

            param1 = "0000000000000000000000000000000000000000000000000000000000000000"
            param2 = "0000000000000000000000000000000000000000000000000000000000000001"
            data_payload = STAKE_METHOD_ID + param1 + param2
            
            tx_hash = self.send_transaction(web3, private_key, address, STAKE_CONTRACT, amount_wei, data_payload)
            if tx_hash:
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Stake Success! Tx: {tx_hash}{Style.RESET_ALL}")
                web3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as e:
            self.log(f"Stake Error: {str(e)}", "ERROR")

    def run_claim(self, web3, private_key, address, proxy, stake_id):
        if not web3: return
        
        param_hex = hex(int(stake_id))[2:].zfill(64)
        data_payload = CLAIM_METHOD_ID + param_hex
        
        try:
            call_params = {
                'to': STAKE_CONTRACT,
                'data': data_payload,
                'from': address
            }
            web3.eth.call(call_params)
        except:
            return

        try:
            tx_hash = self.send_transaction(web3, private_key, address, STAKE_CONTRACT, 0, data_payload)
            if tx_hash:
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Claim Success (ID: {stake_id}) | Tx: {tx_hash}{Style.RESET_ALL}")
                try:
                    receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
                    if receipt['status'] == 1:
                        self.sync_claim(address, tx_hash, proxy)
                except:
                    self.sync_claim(address, tx_hash, proxy)
        except: pass

    def sync_claim(self, address, tx_hash, proxy):
        proxies = self.format_proxy(proxy)
        try:
            if not tx_hash.startswith("0x"): tx_hash = "0x" + tx_hash
            payload = {"txHash": tx_hash, "walletAddress": address}
            requests.post(URL_CLAIM_SYNC, json=payload, headers=self.get_headers("/api/incentive/sync"), proxies=proxies, timeout=15)
        except: pass

    def send_transaction(self, web3, private_key, address, to_contract, value_wei, data):
        try:
            base_fee = web3.eth.get_block('latest')['baseFeePerGas']
            priority_fee = web3.to_wei(1.5, 'gwei') 
            max_fee = base_fee + priority_fee

            tx = {
                'chainId': CHAIN_ID,
                'nonce': web3.eth.get_transaction_count(address),
                'to': to_contract,
                'value': value_wei,
                'data': data,
                'maxFeePerGas': max_fee,
                'maxPriorityFeePerGas': priority_fee,
                'type': '0x2' 
            }
            try:
                gas_est = web3.eth.estimate_gas(tx)
                tx['gas'] = int(gas_est * 1.2)
            except: tx['gas'] = 400000 

            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            return web3.to_hex(tx_hash)
        except:
            return None

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)

    def run(self):
        self.print_banner()
        
        choice = self.show_menu()
        
        use_faucet = input("Auto claim faucet (y/n): ").strip().lower() == 'y'
        
        stake_amt = 0.0
        try: 
            stake_input = input("How many amount to stake: ").strip()
            if stake_input:
                stake_amt = float(stake_input)
        except: 
            stake_amt = 0.0
        
        auto_claim = input("Auto claim stake (y/n): ").strip().lower() == 'y'
        
        if choice == '1':
            self.log("Running with proxy", "INFO")
            self.use_proxy = True
        else:
            self.log("Running without proxy", "INFO")
            self.use_proxy = False
        
        try:
            with open("accounts.txt", "r") as f: accounts = [l.strip() for l in f if l.strip()]
        except:
            self.log("accounts.txt missing", "ERROR")
            return

        proxies = []
        if self.use_proxy:
            try:
                with open("proxy.txt", "r") as f: proxies = [l.strip() for l in f if l.strip()]
            except: 
                self.log("proxy.txt missing", "WARNING")
                pass

        captcha_key = ""
        if use_faucet:
            try: 
                with open("2captcha.txt") as f: captcha_key = f.read().strip()
            except: 
                use_faucet = False
                self.log("2captcha.txt missing, faucet disabled", "WARNING")

        self.log(f"Loaded {len(accounts)} accounts successfully", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.web3 = self.setup_web3(proxies if self.use_proxy else [])
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            
            for i, pk in enumerate(accounts):
                proxy = proxies[i % len(proxies)] if (self.use_proxy and proxies) else None
                address = self.get_address(pk)
                if not address: continue

                self.log(f"Account #{i+1}/{len(accounts)}", "INFO")
                proxy_display = proxy if proxy else "No Proxy"
                self.log(f"Proxy: {proxy_display}", "INFO")
                self.log(f"{address}", "INFO")
                
                self.random_delay()
                
                login_success = self.run_login(address, proxy)
                if login_success:
                    success_count += 1
                
                if use_faucet: 
                    self.run_faucet(address, proxy, captcha_key)
                    self.random_delay()
                
                if stake_amt > 0:
                    self.run_stake(self.web3, pk, address, stake_amt)
                    self.random_delay()

                if auto_claim:
                    total_stakes = self.get_total_stakes_count(address, proxy)
                    if total_stakes > 0:
                        self.log(f"Processing Claim:", "INFO")
                        for sid in range(total_stakes + 5):
                            self.run_claim(self.web3, pk, address, proxy, sid)

                profile = self.get_profile(address, proxy)
                if profile:
                    points = profile.get("points", "0")
                    total_claims = profile.get("total_claims", "0")
                    rank = profile.get("rank", "N/A")
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Points: {points} | Claims: {total_claims} | Rank: {rank}{Style.RESET_ALL}")

                if i < len(accounts) - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)

            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{len(accounts)}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            
            wait_time = 86400
            self.countdown(wait_time)

if __name__ == "__main__":
    ZugChainBot().run()
