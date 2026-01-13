from curl_cffi import requests
from fake_useragent import FakeUserAgent
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from datetime import datetime
from colorama import *
import asyncio, random, string, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Humanoid:
    def __init__(self) -> None:
        self.BASE_API = "https://prelaunch.humanoidnetwork.org"
        self.HF_API = "https://huggingface.co"
        self.REF_CODE = "E2YE9U"
        self.HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.user_agents = []

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message, color=Fore.WHITE, style=Style.BRIGHT, symbol="●"):
        print(
            f"{Fore.MAGENTA + Style.BRIGHT}║{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[{datetime.now().astimezone(wib).strftime('%H:%M:%S')}]{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}│{Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT} {symbol} {Style.RESET_ALL}"
            f"{color + style}{message}{Style.RESET_ALL}"
        )

    def welcome(self):
        self.clear_terminal()
        print(f"""
{Fore.CYAN + Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════╗
{Fore.CYAN + Style.BRIGHT}║{Fore.MAGENTA + Style.BRIGHT}   ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗ ██████╗ ██╗██████╗   {Fore.CYAN + Style.BRIGHT}║
{Fore.CYAN + Style.BRIGHT}║{Fore.MAGENTA + Style.BRIGHT}   ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║██╔═══██╗██║██╔══██╗  {Fore.CYAN + Style.BRIGHT}║
{Fore.CYAN + Style.BRIGHT}║{Fore.MAGENTA + Style.BRIGHT}   ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║   ██║██║██║  ██║  {Fore.CYAN + Style.BRIGHT}║
{Fore.CYAN + Style.BRIGHT}║{Fore.MAGENTA + Style.BRIGHT}   ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██║██║  ██║  {Fore.CYAN + Style.BRIGHT}║
{Fore.CYAN + Style.BRIGHT}║{Fore.MAGENTA + Style.BRIGHT}   ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝██║██████╔╝  {Fore.CYAN + Style.BRIGHT}║
{Fore.CYAN + Style.BRIGHT}║{Fore.MAGENTA + Style.BRIGHT}   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═════╝   {Fore.CYAN + Style.BRIGHT}║
{Fore.CYAN + Style.BRIGHT}╠══════════════════════════════════════════════════════════════════════════╣
{Fore.CYAN + Style.BRIGHT}║{Fore.GREEN + Style.BRIGHT}                    𝐀𝐔𝐓𝐎𝐌𝐀𝐓𝐈𝐎𝐍 𝐒𝐔𝐈𝐓𝐄  •  𝐌𝐔𝐋𝐓𝐈-𝐀𝐂𝐂𝐎𝐔𝐍𝐓               {Fore.CYAN + Style.BRIGHT}║
{Fore.CYAN + Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════╝
{Fore.YELLOW + Style.BRIGHT}                         [ V2.0 • Enhanced Anti-Detection ]                       
        """)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.txt"
        try:
            with open(filename, 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            self.log(f"Loaded {Fore.GREEN}{len(accounts)}{Fore.WHITE} accounts", Fore.GREEN, symbol="✓")
            return accounts
        except Exception as e:
            self.log(f"Failed To Load Accounts: {e}", Fore.RED, symbol="✗")
            return None

    def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"File {filename} Not Found", Fore.RED, symbol="✗")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log("No Proxies Found", Fore.YELLOW, symbol="!")
                return

            self.log(f"Proxies Loaded: {Fore.CYAN}{len(self.proxies)}{Fore.WHITE}", Fore.GREEN, symbol="✓")
        
        except Exception as e:
            self.log(f"Failed To Load Proxies: {e}", Fore.RED, symbol="✗")
            self.proxies = []

    def generate_user_agents(self, count=50):
        ua = FakeUserAgent()
        self.user_agents = [ua.random for _ in range(count)]
        self.log(f"Generated {Fore.MAGENTA}{len(self.user_agents)}{Fore.WHITE} random user agents", Fore.MAGENTA, symbol="🔄")

    def get_random_user_agent(self):
        if not self.user_agents:
            self.generate_user_agents()
        return random.choice(self.user_agents)

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
        
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None

    def print_question(self):
        print(f"\n{Fore.CYAN + Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.YELLOW + Style.BRIGHT}                    𝐂𝐎𝐍𝐅𝐈𝐆𝐔𝐑𝐀𝐓𝐈𝐎𝐍  𝐒𝐄𝐓𝐓𝐈𝐍𝐆𝐒                    {Fore.CYAN + Style.BRIGHT}║")
        print(f"{Fore.CYAN + Style.BRIGHT}╠══════════════════════════════════════════════════════════════════════════╣")
        
        while True:
            try:
                print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.WHITE + Style.BRIGHT}  [1] {Fore.GREEN}Run With Proxy Rotation{Fore.WHITE + Style.BRIGHT}                           {Fore.CYAN + Style.BRIGHT}║")
                print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.WHITE + Style.BRIGHT}  [2] {Fore.YELLOW}Run Without Proxy{Fore.WHITE + Style.BRIGHT}                                   {Fore.CYAN + Style.BRIGHT}║")
                print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.MAGENTA + Style.BRIGHT}─"*70 + f"{Fore.CYAN + Style.BRIGHT}║")
                proxy_choice = int(input(f"{Fore.CYAN + Style.BRIGHT}║{Fore.CYAN + Style.BRIGHT}  {Fore.WHITE + Style.BRIGHT}Select Mode {Fore.GREEN}[1/2]{Fore.WHITE + Style.BRIGHT}: {Style.RESET_ALL}").strip())

                if proxy_choice in [1, 2]:
                    proxy_type = (
                        f"{Fore.GREEN}With Proxy Rotation" if proxy_choice == 1 else 
                        f"{Fore.YELLOW}Without Proxy"
                    )
                    print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.WHITE + Style.BRIGHT}  Selected: {proxy_type}{Style.RESET_ALL}{' '*(48-len(proxy_type))}{Fore.CYAN + Style.BRIGHT}║")
                    break
                else:
                    print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.RED + Style.BRIGHT}  Invalid choice! Please enter 1 or 2.{' '*28}{Fore.CYAN + Style.BRIGHT}║")
            except ValueError:
                print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.RED + Style.BRIGHT}  Invalid input! Enter a number (1 or 2).{' '*24}{Fore.CYAN + Style.BRIGHT}║")

        rotate_proxy = False
        if proxy_choice == 1:
            while True:
                rotate = input(f"{Fore.CYAN + Style.BRIGHT}║{Fore.WHITE + Style.BRIGHT}  Rotate invalid proxies? {Fore.GREEN}[y/n]{Fore.WHITE + Style.BRIGHT}: {Style.RESET_ALL}").strip().lower()

                if rotate in ["y", "n"]:
                    rotate_proxy = rotate == "y"
                    status = f"{Fore.GREEN}Enabled" if rotate_proxy else f"{Fore.RED}Disabled"
                    print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.WHITE + Style.BRIGHT}  Proxy Rotation: {status}{Style.RESET_ALL}{' '*(39)}{Fore.CYAN + Style.BRIGHT}║")
                    break
                else:
                    print(f"{Fore.CYAN + Style.BRIGHT}║{Fore.RED + Style.BRIGHT}  Invalid! Enter 'y' or 'n'.{' '*38}{Fore.CYAN + Style.BRIGHT}║")
        
        delay_choice = input(f"{Fore.CYAN + Style.BRIGHT}║{Fore.WHITE + Style.BRIGHT}  Add random delay between accounts? {Fore.GREEN}[y/n]{Fore.WHITE + Style.BRIGHT}: {Style.RESET_ALL}").strip().lower()
        random_delay = delay_choice == "y"
        
        print(f"{Fore.CYAN + Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════╝\n")
        
        return proxy_choice, rotate_proxy, random_delay
    
    def ensure_ok(self, response):
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}:{response.text}")
    
    async def check_connection(self, proxy_url=None):
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        try:
            response = await asyncio.to_thread(
                requests.get, 
                url="https://api.ipify.org?format=json", 
                proxies=proxies, 
                timeout=30, 
                impersonate="chrome120"
            )
            self.ensure_ok(response)
            ip_data = response.json()
            self.log(f"Connected via IP: {Fore.CYAN}{ip_data.get('ip', 'Unknown')}", Fore.GREEN, symbol="✓")
            return True
        except Exception as e:
            self.log(f"Connection Failed: {str(e)[:50]}...", Fore.RED, symbol="✗")
        
        return None
    
    async def auth_nonce(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/auth/nonce"
        data = json.dumps({"walletAddress": address})
        headers = {
            **self.HEADERS[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(random.uniform(1.0, 2.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.post, 
                    url=url, 
                    headers=headers, 
                    data=data, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                self.ensure_ok(response)
                self.log(f"Nonce fetched successfully", Fore.GREEN, symbol="✓")
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Fetch Nonce Failed: {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def auth_authenticate(self, account: str, address: str, message: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/auth/authenticate"
        data = json.dumps(self.generate_payload(account, address, message))
        headers = {
            **self.HEADERS[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(random.uniform(1.0, 2.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.post, 
                    url=url, 
                    headers=headers, 
                    data=data, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Login Failed: {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def user_data(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/user"
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}"
        }
        await asyncio.sleep(random.uniform(0.5, 1.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.get, 
                    url=url, 
                    headers=headers, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Failed to fetch user data: {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def apply_ref(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/referral/apply"
        data = json.dumps({"referralCode": self.REF_CODE})
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(random.uniform(0.5, 1.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.post, 
                    url=url, 
                    headers=headers, 
                    data=data, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                if response.status_code == 400: 
                    self.log(f"Referral already applied", Fore.YELLOW, symbol="!")
                    return None
                self.ensure_ok(response)
                self.log(f"Referral applied successfully", Fore.GREEN, symbol="✓")
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Apply Ref Failed: {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def training_progress(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/training/progress"
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}"
        }
        await asyncio.sleep(random.uniform(0.5, 1.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.get, 
                    url=url, 
                    headers=headers, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Failed to fetch progress data: {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def scrape_huggingface(self, endpoint: str, limit: int, proxy_url=None, retries=5):
        url = f"{self.HF_API}/api/{endpoint}"
        params = {"limit": limit, "sort": "lastModified", "direction": -1}
        await asyncio.sleep(random.uniform(0.5, 1.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.get, 
                    url=url, 
                    params=params, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                self.ensure_ok(response)
                self.log(f"Scraped {Fore.CYAN}{limit}{Fore.WHITE} {endpoint} from HuggingFace", Fore.GREEN, symbol="✓")
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Failed to scrape {endpoint} data: {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def submit_training(self, address: str, training_data: dict, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/training"
        data = json.dumps(training_data)
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(random.uniform(1.0, 2.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.post, 
                    url=url, 
                    headers=headers, 
                    data=data, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Submit Failed: {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def task_lists(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/tasks"
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}"
        }
        await asyncio.sleep(random.uniform(0.5, 1.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.get, 
                    url=url, 
                    headers=headers, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"Failed to fetch tasks data: {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def complete_task(self, address: str, task_id: str, title: str, recurements: dict, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/api/tasks"
        data = json.dumps({"taskId": task_id,"data": recurements})
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(random.uniform(1.0, 2.5))
        for attempt in range(retries):
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            try:
                response = await asyncio.to_thread(
                    requests.post, 
                    url=url, 
                    headers=headers, 
                    data=data, 
                    proxies=proxies, 
                    timeout=120, 
                    impersonate=random.choice(["chrome120", "chrome110", "edge110", "safari15"])
                )
                if response.status_code == 400:
                    self.log(f"{title}: Already Completed", Fore.YELLOW, symbol="!")
                    return False
                self.ensure_ok(response)
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(f"{title}: Not Completed - {str(e)[:50]}...", Fore.RED, symbol="✗")

        return None
    
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            if proxy:
                self.log(f"Using Proxy: {Fore.CYAN}{proxy[:50]}...", Fore.BLUE, symbol="🌐")

            is_valid = await self.check_connection(proxy)
            if is_valid: return True

            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(address)
                self.log(f"Rotating to new proxy...", Fore.YELLOW, symbol="🔄")
                await asyncio.sleep(2)
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

            self.log(f"Login Successful", Fore.GREEN, symbol="🔓")
            return True

    async def process_accounts(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        print(f"\n{Fore.CYAN + Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════╗")
        self.log(f"Processing Account: {Fore.MAGENTA}{self.mask_account(address)}", Fore.CYAN, symbol="👤")
        print(f"{Fore.CYAN + Style.BRIGHT}╠══════════════════════════════════════════════════════════════════════════╣")
        
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

            self.log(f"Account Points: {Fore.YELLOW}{total_points}", Fore.WHITE, symbol="⭐")

            progress = await self.training_progress(address, proxy)
            if progress:
                self.log(f"Training Progress", Fore.CYAN, symbol="📊")

                models_completed = progress.get("daily", {}).get("models", {}).get("completed")
                models_limit = progress.get("daily", {}).get("models", {}).get("limit")
                models_remaining = progress.get("daily", {}).get("models", {}).get("remaining")

                self.log(f"Models: {Fore.GREEN}{models_completed}{Fore.WHITE}/{Fore.CYAN}{models_limit}", Fore.WHITE, symbol="🤖")
                if models_remaining > 0:
                    models = await self.scrape_huggingface("models", models_remaining, proxy)
                    if models:
                        for model in models:
                            model_name = model["id"]
                            model_url = f"{self.HF_API}/{model['id']}"

                            training_data = {
                                "fileName": model_name,
                                "fileUrl": model_url,
                                "fileType": "model",
                                "recaptchaToken": ""
                            }

                            self.log(f"Submitting Model {Fore.CYAN}{models_completed+1}{Fore.WHITE} of {Fore.CYAN}{models_limit}", Fore.BLUE, symbol="⬆️")

                            submit = await self.submit_training(address, training_data, proxy)
                            if submit:
                                self.log(f"Model Submitted: {Fore.GREEN}{model_name[:30]}...", Fore.GREEN, symbol="✓")
                            models_completed+=1
                else:
                    self.log(f"Models: Daily Limit Reached", Fore.YELLOW, symbol="⏸️")

                datasets_completed = progress.get("daily", {}).get("datasets", {}).get("completed")
                datasets_limit = progress.get("daily", {}).get("datasets", {}).get("limit")
                datasets_remaining = progress.get("daily", {}).get("datasets", {}).get("remaining")

                self.log(f"Datasets: {Fore.GREEN}{datasets_completed}{Fore.WHITE}/{Fore.CYAN}{datasets_limit}", Fore.WHITE, symbol="📁")
                if datasets_remaining > 0:
                    datasets = await self.scrape_huggingface("datasets", datasets_remaining, proxy)
                    if datasets:
                        for dataset in datasets:
                            dataset_name = dataset["id"]
                            dataset_url = f"{self.HF_API}/datasets/{dataset['id']}"

                            training_data = {
                                "fileName": dataset_name,
                                "fileUrl": dataset_url,
                                "fileType": "dataset",
                                "recaptchaToken": ""
                            }

                            self.log(f"Submitting Dataset {Fore.CYAN}{datasets_completed+1}{Fore.WHITE} of {Fore.CYAN}{datasets_limit}", Fore.BLUE, symbol="⬆️")

                            submit = await self.submit_training(address, training_data, proxy)
                            if submit:
                                self.log(f"Dataset Submitted: {Fore.GREEN}{dataset_name[:30]}...", Fore.GREEN, symbol="✓")
                            datasets_completed+=1
                else:
                    self.log(f"Datasets: Daily Limit Reached", Fore.YELLOW, symbol="⏸️")

            tasks = await self.task_lists(address, proxy)
            if tasks:
                self.log(f"Available Tasks", Fore.CYAN, symbol="📋")
                for task in tasks:
                    task_id = task.get("id")
                    title = task.get("title")
                    type = task.get("type")
                    recurements = task.get("requirements")
                    reward = task.get("points")

                    if type == "SOCIAL_TWEET":
                        recurements = self.generate_tweet_id(x_handle)

                    complete = await self.complete_task(address, task_id, title, recurements, proxy)
                    if complete:
                        self.log(f"{title}: Completed +{Fore.YELLOW}{reward}{Fore.WHITE} points", Fore.GREEN, symbol="✅")
            
            print(f"{Fore.CYAN + Style.BRIGHT}╚══════════════════════════════════════════════════════════════════════════╝")
    
    async def main(self):
        try:
            self.generate_user_agents()
            accounts = self.load_accounts()
            if not accounts: return

            proxy_choice, rotate_proxy, random_delay = self.print_question()

            while True:
                self.welcome()
                self.log(f"Total Accounts: {Fore.CYAN}{len(accounts)}", Fore.WHITE, symbol="📊")

                use_proxy = True if proxy_choice == 1 else False
                if use_proxy: self.load_proxies()

                for idx, account in enumerate(accounts, start=1):
                    if account:
                        address = self.generate_address(account)
                        
                        if not address:
                            self.log(f"Invalid Private Key", Fore.RED, symbol="⚠️")
                            continue

                        self.HEADERS[address] = {
                            "Accept": "*/*",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Cache-Control": "no-cache",
                            "Origin": "https://prelaunch.humanoidnetwork.org",
                            "Pragma": "no-cache",
                            "Referer": "https://prelaunch.humanoidnetwork.org/",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "same-origin",
                            "User-Agent": self.get_random_user_agent()
                        }
                        
                        await self.process_accounts(account, address, use_proxy, rotate_proxy)
                        
                        if random_delay and idx < len(accounts):
                            delay = random.uniform(3.0, 8.0)
                            self.log(f"Delaying for {Fore.YELLOW}{delay:.1f}s{Fore.WHITE} before next account...", Fore.BLUE, symbol="⏳")
                            await asyncio.sleep(delay)

                self.log(f"Cycle Completed - All accounts processed", Fore.GREEN, symbol="🎉")
                
                delay = 24 * 60 * 60
                while delay > 0:
                    formatted_time = self.format_seconds(delay)
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[{Fore.MAGENTA}⏰{Fore.CYAN}] Next cycle in {Fore.GREEN}{formatted_time}{Fore.CYAN}...{' '*20}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1)
                    delay -= 1
                print()

        except Exception as e:
            self.log(f"Unexpected Error: {str(e)[:100]}", Fore.RED, symbol="💥")
            raise e

if __name__ == "__main__":
    try:
        bot = Humanoid()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN + Style.BRIGHT}[{Fore.RED}✗{Fore.CYAN}] {Fore.YELLOW}Bot terminated by user{Style.RESET_ALL}")
