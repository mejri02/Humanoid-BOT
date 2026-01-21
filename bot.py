from curl_cffi import requests
from fake_useragent import FakeUserAgent
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from datetime import datetime
from colorama import *
import asyncio, random, string, json, os, pytz
import time, hashlib

init(autoreset=True)
wib = pytz.timezone('Africa/Tunis')

class Humanoid:
    def __init__(self) -> None:
        self.BASE_API = "https://app.humanoidnetwork.org"
        self.HF_API = "https://huggingface.co"
        self.REF_CODE = "E2YE9U"
        self.HEADERS = {}
        self.user_agents = {} 
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.ua_factory = FakeUserAgent()
        self.request_timestamps = {}
        self.session_ids = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message, type="INFO"):
        time_str = datetime.now().astimezone(wib).strftime('%H:%M:%S')
        colors = {
            "INFO": Fore.CYAN,
            "SUCCESS": Fore.GREEN,
            "ERROR": Fore.RED,
            "WARN": Fore.YELLOW,
            "TASK": Fore.MAGENTA,
            "PROXY": Fore.BLUE
        }
        prefix = colors.get(type, Fore.WHITE)
        print(
            f"{Fore.WHITE}[{time_str}]{Style.RESET_ALL} "
            f"{prefix}{Style.BRIGHT}│ {type.ljust(7)}{Style.RESET_ALL} "
            f"{Fore.WHITE}│ {message}{Style.RESET_ALL}"
        )

    def welcome(self):
        self.clear_terminal()
        banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}    __  __                               _     __
{Fore.MAGENTA}{Style.BRIGHT}   / / / /_  ______ ___  ____ _____  ____ (_)___/ /
{Fore.BLUE}{Style.BRIGHT}  / /_/ / / / / __ `__ \/ __ `/ __ \/ __ \/ / __  / 
{Fore.CYAN}{Style.BRIGHT} / __  / /_/ / / / / / / /_/ / / / / /_/ / / /_/ /  
{Fore.CYAN}{Style.BRIGHT}/_/ /_/\__,_/_/ /_/ /_/\__,_/_/ /_/\____/_/\__,_/   
{Fore.WHITE}        {Back.MAGENTA} AUTO-FARMING BOT v3.0 - 2026 {Style.RESET_ALL}
{Fore.YELLOW}           Created by: Rey? <WATERMARK>
        """
        print(banner)

    async def human_delay(self, address, min_s=1, max_s=3):
        current_time = time.time()
        if address in self.request_timestamps:
            last_time = self.request_timestamps[address]
            elapsed = current_time - last_time
            if elapsed < 1:
                wait_time = random.uniform(1.5, 2.5)
                await asyncio.sleep(wait_time)
        
        delay = random.uniform(min_s, max_s)
        await asyncio.sleep(delay)
        self.request_timestamps[address] = time.time()
        return delay

    def generate_session_id(self, address):
        if address not in self.session_ids:
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            timestamp = str(int(time.time()))
            session_data = f"{address}{random_str}{timestamp}"
            session_id = hashlib.md5(session_data.encode()).hexdigest()[:16]
            self.session_ids[address] = session_id
        return self.session_ids[address]

    def get_headers(self, address):
        if address not in self.user_agents:
            self.user_agents[address] = self.ua_factory.random
        
        session_id = self.generate_session_id(address)
        
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://app.humanoidnetwork.org",
            "Referer": "https://app.humanoidnetwork.org/",
            "User-Agent": self.user_agents[address],
            "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": random.choice(['"Windows"', '"macOS"', '"Linux"']),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Session-ID": session_id,
            "X-Client-Timestamp": str(int(time.time() * 1000))
        }

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}h {int(minutes):02}m {int(seconds):02}s"
    
    def load_accounts(self):
        try:
            with open("accounts.txt", 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            self.log(f"Accounts Total: {len(accounts)}", "INFO")
            return accounts
        except Exception as e:
            self.log(f"Failed To Load Accounts: {e}", "ERROR")
            return None

    def load_proxies(self):
        try:
            if not os.path.exists("proxy.txt"): return
            with open("proxy.txt", 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            if self.proxies:
                self.log(f"Proxies Total  : {len(self.proxies)}", "INFO")
        except Exception as e:
            self.log(f"Failed To Load Proxies: {e}", "ERROR")

    def check_proxy_schemes(self, proxy):
        for scheme in ["http://", "https://", "socks4://", "socks5://"]:
            if proxy.startswith(scheme): return proxy
        return f"http://{proxy}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies: return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def generate_address(self, private_key: str):
        try:
            return Account.from_key(private_key).address
        except:
            return None
    
    def generate_payload(self, account: str, address: str, message: str):
        encoded_message = encode_defunct(text=message)
        signed_message = Account.sign_message(encoded_message, private_key=account)
        return {
            "walletAddress": address,
            "signature": to_hex(signed_message.signature),
            "message": message
        }
        
    def generate_tweet_id(self, x_handle):
        if x_handle:
            handle = x_handle
        else:
            handle = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        tweet_id = str(random.randint(10**17, 10**18 - 1))
        return { "tweetId": f"https://x.com/{handle}/status/{tweet_id}" }

    def print_question(self):
        self.welcome()
        print(f"{Fore.WHITE}{'─'*50}")
        print(f"{Fore.CYAN}[1]{Fore.WHITE} Run With Proxy")
        print(f"{Fore.CYAN}[2]{Fore.WHITE} Run Without Proxy")
        choice = input(f"{Fore.YELLOW}Select Option > {Style.RESET_ALL}")
        
        rotate = 'n'
        if choice == '1':
            rotate = input(f"{Fore.YELLOW}Rotate proxy on error? (y/n) > {Style.RESET_ALL}")
        
        return int(choice), rotate.lower() == 'y'

    async def check_connection(self, proxy_url=None):
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            response = await asyncio.to_thread(requests.get, "https://api.ipify.org?format=json", proxies=proxies, timeout=15, impersonate="chrome120")
            return response.status_code == 200
        except Exception:
            return False

    async def auth_nonce(self, address: str, proxy_url=None):
        url = f"{self.BASE_API}/api/auth/nonce"
        data = json.dumps({"walletAddress": address})
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await self.human_delay(address, 0.5, 1.5)
            resp = await asyncio.to_thread(requests.post, url, headers=self.get_headers(address), data=data, proxies=proxies, impersonate="chrome120")
            return resp.json() if resp.ok else None
        except: 
            return None

    async def auth_authenticate(self, account: str, address: str, message: str, proxy_url=None):
        url = f"{self.BASE_API}/api/auth/authenticate"
        data = json.dumps(self.generate_payload(account, address, message))
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await self.human_delay(address, 0.5, 1.5)
            resp = await asyncio.to_thread(requests.post, url, headers=self.get_headers(address), data=data, proxies=proxies, impersonate="chrome120")
            return resp.json() if resp.ok else None
        except: 
            return None

    async def user_data(self, address: str, proxy_url=None):
        url = f"{self.BASE_API}/api/user"
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await self.human_delay(address)
            resp = await asyncio.to_thread(requests.get, url, headers=headers, proxies=proxies, impersonate="chrome120")
            return resp.json() if resp.ok else None
        except: 
            return None

    async def apply_ref(self, address: str, proxy_url=None):
        url = f"{self.BASE_API}/api/referral/apply"
        data = json.dumps({"referralCode": self.REF_CODE})
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await self.human_delay(address)
            await asyncio.to_thread(requests.post, url, headers=headers, data=data, proxies=proxies, impersonate="chrome120")
        except: 
            pass

    async def training_progress(self, address: str, proxy_url=None):
        url = f"{self.BASE_API}/api/training/progress"
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await self.human_delay(address)
            resp = await asyncio.to_thread(requests.get, url, headers=headers, proxies=proxies, impersonate="chrome120")
            return resp.json() if resp.ok else None
        except: 
            return None

    async def scrape_huggingface(self, endpoint: str, limit: int, proxy_url=None):
        url = f"{self.HF_API}/api/{endpoint}"
        params = {"limit": limit, "sort": "lastModified", "direction": -1}
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await asyncio.sleep(random.uniform(1, 2))
            resp = await asyncio.to_thread(requests.get, url, params=params, proxies=proxies, impersonate="chrome120")
            return resp.json() if resp.ok else None
        except: 
            return None

    async def submit_training(self, address: str, training_data: dict, proxy_url=None):
        url = f"{self.BASE_API}/api/training"
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await self.human_delay(address)
            resp = await asyncio.to_thread(requests.post, url, headers=headers, data=json.dumps(training_data), proxies=proxies, impersonate="chrome120")
            return resp.json() if resp.ok else None
        except: 
            return None

    async def task_lists(self, address: str, proxy_url=None):
        url = f"{self.BASE_API}/api/tasks"
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await self.human_delay(address)
            resp = await asyncio.to_thread(requests.get, url, headers=headers, proxies=proxies, impersonate="chrome120")
            return resp.json() if resp.ok else None
        except: 
            return None

    async def complete_task(self, address: str, task_id: str, title: str, requirements: dict, proxy_url=None):
        url = f"{self.BASE_API}/api/tasks"
        data = json.dumps({"taskId": task_id, "data": requirements})
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            await self.human_delay(address)
            resp = await asyncio.to_thread(requests.post, url, headers=headers, data=data, proxies=proxies, impersonate="chrome120")
            if resp.status_code == 400:
                self.log(f"Task: {title[:20]}... [Already Done]", "WARN")
                return False
            return resp.json() if resp.ok else None
        except: 
            return None

    async def process_accounts(self, account: str, idx: int, use_proxy: bool, rotate_proxy: bool):
        address = None
        try:
            address = self.generate_address(account)
            if not address:
                self.log(f"Invalid Private Key (Idx: {idx})", "ERROR")
                return

            print(f"\n{Fore.MAGENTA}{'='*60}")
            self.log(f"Account #{idx} | Wallet: {address[:6]}...{address[-4:]}", "INFO")
            
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            if use_proxy and proxy:
                self.log(f"Proxy: {proxy}", "PROXY")
                is_valid = await self.check_connection(proxy)
                if not is_valid:
                    self.log(f"Proxy connection failed", "ERROR")
                    if rotate_proxy:
                        self.account_proxies.pop(address, None)
                    return

            nonce_data = await self.auth_nonce(address, proxy)
            if not nonce_data: 
                self.log("Failed to get nonce", "ERROR")
                return
            
            auth_data = await self.auth_authenticate(account, address, nonce_data.get("message"), proxy)
            if not auth_data: 
                self.log("Authentication failed", "ERROR")
                return
            
            self.access_tokens[address] = auth_data.get("token")
            self.log("Authentication successful", "SUCCESS")

            x_handle = None
            
            user = await self.user_data(address, proxy)
            if user:
                x_handle = user.get("user", {}).get("twitterId")
                points = user.get('totalPoints', 0)
                self.log(f"Current Points: {Fore.YELLOW}{points}", "INFO")
                if user.get("user", {}).get("referredBy") is None:
                    await self.apply_ref(address, proxy)
            else:
                self.log("Failed to get user data", "WARN")

            progress = await self.training_progress(address, proxy)
            if progress:
                for category in ["models", "datasets"]:
                    data = progress.get("daily", {}).get(category, {})
                    rem = data.get("remaining", 0)
                    comp = data.get("completed", 0)
                    limit = data.get("limit", 0)
                    
                    self.log(f"Processing {category.capitalize()}: {comp}/{limit}", "TASK")
                    
                    if rem > 0:
                        items = await self.scrape_huggingface(category, rem, proxy)
                        if items:
                            for item in items:
                                t_data = {
                                    "fileName": item.get("id", ""),
                                    "fileUrl": f"{self.HF_API}/{'datasets/' if category=='datasets' else ''}{item.get('id', '')}",
                                    "fileType": "model" if category=="models" else "dataset",
                                    "recaptchaToken": ""
                                }
                                res = await self.submit_training(address, t_data, proxy)
                                if res:
                                    self.log(f"Uploaded {category[:-1]}: {item.get('id', '')[:25]}...", "SUCCESS")
                                await asyncio.sleep(random.uniform(2, 4))
                    else:
                        self.log(f"Daily {category} limit reached.", "WARN")

            tasks = await self.task_lists(address, proxy)
            if tasks:
                for task in tasks:
                    t_id = task.get("id")
                    t_title = task.get("title", "Unknown Task")
                    t_type = task.get("type")
                    req = task.get("requirements", {})
                    
                    if t_type == "SOCIAL_TWEET":
                        req = self.generate_tweet_id(x_handle)
                    
                    if req:
                        res = await self.complete_task(address, t_id, t_title, req, proxy)
                        if res:
                            points = task.get('points', 0)
                            self.log(f"Task '{t_title}' Completed! +{points} pts", "SUCCESS")
                        await self.human_delay(address, 1, 2)
                        
        except Exception as e:
            self.log(f"Account Loop Error: {str(e)}", "ERROR")

    async def main(self):
        accounts = self.load_accounts()
        if not accounts: 
            self.log("No accounts found in accounts.txt", "ERROR")
            return

        proxy_choice, rotate_proxy = self.print_question()
        use_proxy = (proxy_choice == 1)
        if use_proxy: 
            self.load_proxies()

        processed_count = 0
        
        self.welcome()
        self.log(f"Total Accounts: {len(accounts)}", "INFO")
        
        for idx, account in enumerate(accounts, start=1):
            try:
                await self.process_accounts(account, idx, use_proxy, rotate_proxy)
                processed_count += 1
                await asyncio.sleep(random.uniform(5, 10))
            except Exception as e:
                self.log(f"Account Loop Error: {e}", "ERROR")

        print(f"\n{Fore.CYAN}{'='*60}")
        self.log(f"Processing complete. Success: {processed_count}", "INFO")
        
        if processed_count > 0:
            self.log("Entering 24h hibernation...", "INFO")
            delay = 24 * 60 * 60
            while delay > 0:
                print(f"{Fore.WHITE}Time until next run: {Fore.YELLOW}{self.format_seconds(delay)} {Fore.WHITE}│ Monitoring active... ", end="\r")
                await asyncio.sleep(1)
                delay -= 1
        else:
            self.log("No accounts processed successfully. Check your accounts/proxies.", "ERROR")
            input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        bot = Humanoid()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}BOT STOPPED MANUALLY")
