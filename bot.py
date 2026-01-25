from curl_cffi.requests import AsyncSession
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from datetime import datetime
from colorama import *
import asyncio, random, string, json, os, pytz
import time, hashlib

init(autoreset=True)
wib = pytz.timezone('Asia/Jakarta')

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
        self.sessions = {}
        self.access_tokens = {}
        self.request_timestamps = {}
        self.session_ids = {}
        
        self.USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/116.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        ]

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
        print(f"{Fore.WHITE}[{time_str}]{Style.RESET_ALL} {prefix}{Style.BRIGHT}│ {type.ljust(7)}{Style.RESET_ALL} {Fore.WHITE}│ {message}{Style.RESET_ALL}")

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

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}h {int(minutes):02}m {int(seconds):02}s"
    
    def load_accounts(self):
        filename = "accounts.txt"
        try:
            with open(filename, 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            self.log(f"Accounts Total: {len(accounts)}", "INFO")
            return accounts
        except Exception as e:
            self.log(f"Failed To Load Accounts: {e}", "ERROR")
            return None

    def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"File {filename} Not Found.", "ERROR")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"No Proxies Found.", "ERROR")
                return

            self.log(f"Proxies Total: {len(self.proxies)}", "INFO")
        
        except Exception as e:
            self.log(f"Failed To Load Proxies: {e}", "ERROR")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address
            return address
        except Exception as e:
            return None
    
    def generate_payload(self, account: str, address: str, message: str):
        try:
            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            return {
                "walletAddress": address,
                "signature": signature,
                "message": message
            }
        except Exception as e:
            raise Exception(f"Generate Req Payload Failed: {str(e)}")
        
    def generate_random_x_handle(self, min_len=5, max_len=12):
        chars = string.ascii_lowercase + string.digits
        length = random.randint(min_len, max_len)
        return ''.join(random.choice(chars) for _ in range(length))
        
    def generate_tweet_id(self, x_handle):
        if x_handle is None:
            x_handle = self.generate_random_x_handle()

        tweet_id = str(random.randint(10**17, 10**18 - 1))

        return { "tweetId": f"https://x.com/{x_handle}/status/{tweet_id}" }
    
    def get_next_user_agent(self):
        return random.choice(self.USER_AGENTS)
    
    def get_headers(self, address: str):
        if address not in self.HEADERS:
            session_id = self.generate_session_id(address)
            
            self.HEADERS[address] = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "no-cache",
                "Content-Type": "application/json",
                "Origin": "https://app.humanoidnetwork.org",
                "Pragma": "no-cache",
                "Referer": "https://app.humanoidnetwork.org/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": self.get_next_user_agent(),
                "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": random.choice(['"Windows"', '"macOS"', '"Linux"']),
                "X-Session-ID": session_id,
                "X-Client-Timestamp": str(int(time.time() * 1000))
            }
            
        return self.HEADERS[address]
    
    def get_session(self, address: str, proxy_url=None, timeout=60):
        if address not in self.sessions:
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

            session = AsyncSession(
                proxies=proxies,
                timeout=timeout, 
                impersonate="chrome120"
            )
            
            self.sessions[address] = session
        
        return self.sessions[address]
    
    async def close_session(self, address: str):
        if address in self.sessions:
            await self.sessions[address].close()
            del self.sessions[address]
    
    async def close_all_sessions(self):
        for address in list(self.sessions.keys()):
            await self.close_session(address)

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

    def ensure_ok(self, response):
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}:{response.text}")
    
    async def check_connection(self, address: str, proxy_url=None):
        url = "https://api.ipify.org?format=json"
        try:
            session = self.get_session(address, proxy_url, 15)
            response = await session.get(url=url)
            self.ensure_ok(response)
            return True
        except Exception as e:
            self.log(f"Connection Not 200 OK - {str(e)}", "ERROR")
        
        return None
    
    async def auth_nonce(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/auth/nonce"
        payload = {"walletAddress": address}
        headers = self.get_headers(address)

        await self.human_delay(address, 0.5, 1.5)
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.post(url=url, headers=headers, json=payload)
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Fetch Nonce Failed - {str(e)}", "ERROR")

        return None
    
    async def auth_authenticate(self, account: str, address: str, message: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/auth/authenticate"
        payload = self.generate_payload(account, address, message)
        headers = self.get_headers(address)

        await self.human_delay(address, 0.5, 1.5)
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.post(url=url, headers=headers, json=payload)
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Login Failed - {str(e)}", "ERROR")

        return None
    
    async def user_data(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/user"
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        
        await self.human_delay(address, 0.5, 1.5)
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.get(url=url, headers=headers)
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Failed to fetch user data - {str(e)}", "ERROR")

        return None
    
    async def apply_ref(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/referral/apply"
        payload = {"referralCode": self.REF_CODE}
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        
        await self.human_delay(address, 0.5, 1.5)
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.post(url=url, headers=headers, json=payload)
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Apply Ref Failed - {str(e)}", "ERROR")

        return None
    
    async def training_progress(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/training/progress"
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        
        await self.human_delay(address, 0.5, 1.5)
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.get(url=url, headers=headers)
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Failed to fetch progress data - {str(e)}", "ERROR")

        return None
    
    async def scrape_huggingface(self, address: str, endpoint: str, limit: int, proxy_url=None, retries=5):
        if endpoint == "models":
            url = f"{self.HF_API}/api/models"
        elif endpoint == "datasets":
            url = f"{self.HF_API}/api/datasets"
        else:
            return None
        
        params = {
            "limit": limit,
            "sort": "lastModified",
            "direction": -1,
            "filter": ""
        }

        await asyncio.sleep(random.uniform(1, 2))
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.get(url=url, params=params)
                self.ensure_ok(response)
                data = response.json()
                
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and endpoint in data:
                    return data[endpoint]
                elif isinstance(data, dict) and "models" in data:
                    return data["models"]
                elif isinstance(data, dict) and "datasets" in data:
                    return data["datasets"]
                else:
                    self.log(f"Invalid response format for {endpoint}", "WARN")
                    return None
                    
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Failed to scrape {endpoint} data - {str(e)}", "ERROR")

        return None
    
    async def submit_training(self, address: str, training_data: dict, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/training"
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        
        await self.human_delay(address, 0.5, 1.5)
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.post(url=url, headers=headers, json=training_data)
                
                if response.status_code == 400:
                    try:
                        result = response.json()
                        err_msg = result.get("error") or result.get("message") or response.text
                        if "Invalid HuggingFace URL" in err_msg:
                            return None
                        self.log(f"Submit Failed - {err_msg}", "ERROR")
                    except:
                        self.log(f"Submit Failed - HTTP {response.status_code}", "ERROR")
                    return None
                
                if not response.ok:
                    self.log(f"Submit Failed - HTTP {response.status_code}: {response.text[:100]}", "ERROR")
                    return None
                    
                return response.json()
                
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Submit Failed - {str(e)}", "ERROR")

        return None
    
    async def task_lists(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/tasks"
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        
        await self.human_delay(address, 0.5, 1.5)
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.get(url=url, headers=headers)
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Failed to fetch tasks data - {str(e)}", "ERROR")

        return None
    
    async def complete_task(self, address: str, task_id: str, title: str, recurements: dict, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/tasks"
        payload = {"taskId": task_id,"data": recurements}
        headers = self.get_headers(address)
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        
        await self.human_delay(address, 0.5, 1.5)
        for attempt in range(retries):
            try:
                session = self.get_session(address, proxy_url)
                response = await session.post(url=url, headers=headers, json=payload)
                if response.status_code == 400:
                    self.log(f"Task: {title[:20]}... [Already Done]", "WARN")
                    return False
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Task '{title}' Not Completed - {str(e)}", "ERROR")

        return None
    
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            if use_proxy and proxy:
                self.log(f"Proxy: {proxy}", "PROXY")

            is_valid = await self.check_connection(address, proxy)
            if is_valid: return True

            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(address)
                await asyncio.sleep(1)
                continue

            return False
    
    async def process_auth_login(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
        if is_valid:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            nonce = await self.auth_nonce(address, proxy)
            if not nonce: return False

            message = nonce.get("message")

            authenticate = await self.auth_authenticate(account, address, message, proxy)
            if not authenticate: return False
            
            self.access_tokens[address] = authenticate.get("token")

            self.log("Login Success", "SUCCESS")
            return True

    async def process_accounts(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool, idx: int):
        print(f"\n{Fore.MAGENTA}{'='*60}")
        self.log(f"Account #{idx} | Wallet: {address[:6]}...{address[-4:]}", "INFO")
        
        logined = await self.process_auth_login(account, address, use_proxy, rotate_proxy)
        if logined:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            user = await self.user_data(address, proxy)
            if not user: return False

            refer_by = user.get("user", {}).get("referredBy", None)
            x_handle = user.get("user", {}).get("twitterId", None)
            total_points = user.get("totalPoints")

            if refer_by is None:
                await self.apply_ref(address, proxy)

            self.log(f"Current Points: {Fore.YELLOW}{total_points}", "INFO")

            progress = await self.training_progress(address, proxy)
            if progress:
                self.log(f"Processing Training Tasks", "TASK")

                models_completed = progress.get("daily", {}).get("models", {}).get("completed")
                models_limit = progress.get("daily", {}).get("models", {}).get("limit")
                models_remaining = progress.get("daily", {}).get("models", {}).get("remaining")

                if models_remaining > 0:
                    models = await self.scrape_huggingface(address, "models", models_remaining, proxy)
                    if models:
                        for model in models:
                            if not isinstance(model, dict):
                                continue
                                
                            model_name = model.get("id")
                            if not model_name:
                                continue
                                
                            model_url = f"https://huggingface.co/{model_name}"
                            is_private = model.get("private", False)
                            gated = model.get("gated", False)

                            if is_private or gated:
                                continue

                            training_data = {
                                "fileName": model_name,
                                "fileUrl": model_url,
                                "fileType": "model",
                                "recaptchaToken": ""
                            }

                            self.log(f"Uploading model: {model_name[:30]}...", "INFO")

                            submit = await self.submit_training(address, training_data, proxy)
                            if submit:
                                self.log(f"Model Submitted Successfully", "SUCCESS")
                                models_completed += 1
                                await asyncio.sleep(random.uniform(2, 4))

                else:
                    self.log(f"Daily models limit reached [{models_completed}/{models_limit}]", "WARN")

                datasets_completed = progress.get("daily", {}).get("datasets", {}).get("completed")
                datasets_limit = progress.get("daily", {}).get("datasets", {}).get("limit")
                datasets_remaining = progress.get("daily", {}).get("datasets", {}).get("remaining")

                if datasets_remaining > 0:
                    datasets = await self.scrape_huggingface(address, "datasets", datasets_remaining, proxy)
                    if datasets:
                        for dataset in datasets:
                            if not isinstance(dataset, dict):
                                continue
                                
                            dataset_name = dataset.get("id")
                            if not dataset_name:
                                continue
                                
                            dataset_url = f"https://huggingface.co/datasets/{dataset_name}"
                            is_private = dataset.get("private", False)
                            gated = dataset.get("gated", False)

                            if is_private or gated:
                                continue

                            training_data = {
                                "fileName": dataset_name,
                                "fileUrl": dataset_url,
                                "fileType": "dataset",
                                "recaptchaToken": ""
                            }

                            self.log(f"Uploading dataset: {dataset_name[:30]}...", "INFO")

                            submit = await self.submit_training(address, training_data, proxy)
                            if submit:
                                self.log(f"Dataset Submitted Successfully", "SUCCESS")
                                datasets_completed += 1
                                await asyncio.sleep(random.uniform(2, 4))

                else:
                    self.log(f"Daily datasets limit reached [{datasets_completed}/{datasets_limit}]", "WARN")

            tasks = await self.task_lists(address, proxy)
            if tasks:
                self.log(f"Processing Daily Tasks", "TASK")

                for task in tasks:
                    task_id = task.get("id")
                    title = task.get("title")
                    type = task.get("type")
                    recurements = task.get("requirements")
                    reward = task.get("points")

                    if type == "SOCIAL_TWEET":
                        recurements = self.generate_tweet_id(x_handle)

                    if recurements:
                        complete = await self.complete_task(address, task_id, title, recurements, proxy)
                        if complete:
                            self.log(f"Task '{title}' Completed! +{reward} pts", "SUCCESS")
                        await self.human_delay(address, 1, 2)
            
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts: return

            proxy_choice, rotate_proxy = self.print_question()

            self.welcome()
            self.log(f"Total Accounts: {len(accounts)}", "INFO")

            use_proxy = True if proxy_choice == 1 else False
            if use_proxy: self.load_proxies()

            processed_count = 0
            
            for idx, account in enumerate(accounts, start=1):
                if account:
                    address = self.generate_address(account)
                    
                    if not address:
                        self.log(f"Invalid Private Key (Idx: {idx})", "ERROR")
                        continue
                    
                    await self.process_accounts(account, address, use_proxy, rotate_proxy, idx)
                    processed_count += 1
                    await asyncio.sleep(random.uniform(5, 10))

            await self.close_all_sessions()

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

        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
            raise e
        finally:
            await self.close_all_sessions()

if __name__ == "__main__":
    try:
        bot = Humanoid()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}BOT STOPPED MANUALLY")
