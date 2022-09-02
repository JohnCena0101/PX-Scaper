#by github.com/Kuucheen
import re, os, time, threading, random, ctypes

try:
    import httpx, yaml
    from pystyle import Colors, Colorate, Center
except ImportError:
    os.system('python -m pip install httpx[http2]')
    os.system('python -m pip install pyyaml')
    os.system('python -m pip install pystyle')
    import httpx, yaml
    from pystyle import Colors, Colorate, Center

proxies = set([])
goodsites = set([])
sitelist = []
proxycount = 0
threadcount = 0
clearingcnt = ""
clearingproxy = ""
white = Colors.light_gray
color = Colors.StaticMIX((Colors.purple, Colors.blue))


def main():
    global threadcount, clearingcnt, sitelist, start

    with open("settings.yaml") as setting:
        settings = yaml.safe_load(setting.read())

    premades = settings["premades"]
    clearingcnt = settings["removewebsites"]
    clearingproxy = settings["removeproxyless"]
    threads = settings["threads"]

    terminal()

    os.system("cls")


    logo = """
 _     _ _______     ______                                     
(_)   | (_______)   / _____)                                    
 _____| |_         ( (____   ____  ____ _____ ____  _____  ____ 
|  _   _) |         \____ \ / ___)/ ___|____ |  _ \| ___ |/ ___)
| |  \ \| |_____    _____) | (___| |   / ___ | |_| | ____| |    
|_|   \_)\______)  (______/ \____)_|   \_____|  __/|_____)_|    
                                             |_|                
                    by github.com/Kuucheen
"""

    print(Colorate.Diagonal(Colors.DynamicMIX((Colors.dark_gray, Colors.StaticMIX((Colors.purple, Colors.blue)))), Center.XCenter(logo)))
    print("\n"*3)

    if premades == "?":
        premades = input(f"{white}[{color}^{white}] {color}Use premades [y/n] {white}>> {color}")
        if premades == "yes" or premades == "y":
            os.system("cls")
            print(Colorate.Diagonal(Colors.DynamicMIX((Colors.dark_gray, Colors.StaticMIX((Colors.purple, Colors.blue)))), Center.XCenter(logo)))
            print(Colorate.Diagonal(Colors.DynamicMIX((Colors.dark_gray, Colors.StaticMIX((Colors.purple, Colors.blue)))), Center.XCenter("\n[1] HTTP/S\t[2] SOCKS4\t[3] SOCKS5")))

            premades = input(f"\n\n{white}[{color}^{white}] {white}>> {color}")

        elif premades != "no" and premades != "n":
            print(f"{white}[{color}!{white}] {color}No option was choosen returning to home..")
            time.sleep(3)
            main()
            exit()

    elif premades != "1" and premades != "2" and premades != "3" and premades != "n":
        print(f"{white}[{Colors.red}!{white}] {Colors.red}Error{white} in settings.json at premades")
        input()
        exit()

    config = {"1": "premades/http.txt", "2": "premades/socks4.txt", "3": "premades/socks5.txt", "n": "sites.txt", "no": "sites.txt"}

    try:
        config = config[premades]
    except KeyError:
        print(f"{white}[{color}!{white}] {color}No option was choosen returning to home..")
        time.sleep(3)
        main()
        exit()


    os.system("cls")
    print(Colorate.Diagonal(Colors.DynamicMIX((Colors.dark_gray, Colors.StaticMIX((Colors.purple, Colors.blue)))), Center.XCenter(logo)))

    if clearingcnt == "?":

        clearingcnt = input(f"\n\n\n{white}[{color}^{white}] {color}Remove not connectable site [y/n] {white}>> {color}")

        if clearingcnt != "y" and clearingcnt != "ye" and clearingcnt != "yes" and clearingcnt != "n" and clearingcnt != "no":
            print(f"{white}[{color}!{white}] {color}No option was choosen returning to home..")
            time.sleep(3)
            main()
            exit()
    elif clearingcnt != "y" and clearingcnt != "ye" and clearingcnt != "yes" and clearingcnt != "n" and clearingcnt != "no":
        print(f"{white}[{Colors.red}!{white}] {Colors.red}Error{white} in settings.json at removewebsites")
        input()
        exit()
    
    if clearingcnt == "y" or clearingcnt == "ye" or clearingcnt == "yes":
        clearingcnt = True
    
    if clearingproxy == "?":

        clearingproxy = input(f"\n{white}[{color}^{white}] {color}Remove sites with no proxies [y/n] {white}>> {color}")

        if clearingproxy != "y" and clearingproxy != "ye" and clearingproxy != "yes" and clearingproxy != "n" and clearingproxy != "no":
            print(f"{white}[{color}!{white}] {color}No option was choosen returning to home..")
            time.sleep(3)
            main()
            exit()
    
    elif clearingproxy != "y" and clearingproxy != "ye" and clearingproxy != "yes" and clearingproxy != "n" and clearingproxy != "no":
            print(f"{white}[{Colors.red}!{white}] {Colors.red}Error{white} in settings.json at removeproxyless")
            input()
            exit()

    if clearingproxy == "y" or clearingproxy == "ye" or clearingproxy == "yes":
        clearingproxy = True

    if threads == "?":

        threads = input(f"\n{white}[{color}^{white}] {color}Threads {white}>> {color}")

    elif threads.isdigit() == False:
        print(f"{white}[{Colors.red}!{white}] {Colors.red}Error{white} in settings.json at threads")
        input()
        exit()

    try:
        threads = int(threads)
    except ValueError:
        print(f"{white}[{color}!{white}] {color}Thread needs a number")
        time.sleep(3)
        main()
        exit()
        
    if threads < 1:
        print(f"{white}[{color}!{white}] {color}Thread needs a number greater than 0")
        time.sleep(3)
        main()
        exit()
    
    print()
    start = time.time()

    with open(config) as sites:

        sitelist = sites.readlines()
        threading.Thread(target=terminalthread).start()

        while len(sitelist) > 0:
            if threadcount < threads:
                threading.Thread(target=scrape, args=[sitelist[0]]).start()
                threadcount += 1
                sitelist.pop(0)

        while threadcount > 0:
            terminal(f"| Waiting for threads to finish | active threads {threadcount} | Proxies {proxycount} | Time {time.time()-start:.2f}s")

        terminal()
        

    lenproxies = len(proxies)
    print(f"\n{white}[{color}^{white}] Removed {color}{proxycount-lenproxies} {white}Duplicates\n")
    print(f"{white}[{color}^{white}] Remaining Proxies: {color}{lenproxies}{white}\n")
    print(f"{white}[{color}^{white}] Writing {color}Proxies\n")

    with open("proxies.txt", "w") as output:

        for i in proxies:
            output.write(i.replace("\n", "") + "\n")
    
    if clearingcnt == True:

        print(f"{white}[{color}^{white}] Removing {color}not reachable Websites\n")

        with open(config, "w") as inp:

            for site in goodsites:
                inp.write(site + "\n")

    terminal()

    print(f"{white}[{color}^{white}] Finished in {color}{time.time()-start:.2f}s{white}!\n")
    print("You can now close the tab")

    input("")



def scrape(site: str):
    global proxies, threadcount, proxycount
    #random useragent by (idk dm me if you are the guy) but thank you helped me learn how to use httpx
    uas=['Mozilla/5.0 (X11; CrOS x86_64 14588.123.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.72 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.4; rv:101.0) Gecko/20100101 Firefox/101.0', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 'Mozilla/5.0 (Linux; Android 12; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36']
    site = site.replace("\n", "")
    finished = False
    localproxycount = 0
    try:
        with httpx.Client(http2=True,headers = {'accept-language': 'en','user-agent':random.choice(uas)},follow_redirects=True) as client:
            r = client.get(site, timeout=10).text
    except:
        print(f"{white}[{Colors.red}!{white}] Failed connecting to {color}{site}")
    else:
        print(f"{white}[{Colors.green}+{white}] Scraping {color}{site}")
        if clearingcnt == True:
            goodsites.add(site)
        pattern = r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\:[0-9]+$'
        if r.count(":") > 0 and r.count(".") > 2:
            for _ in range(r.count(":")):
                pos = r.find(":")
                if r[pos-1].isdigit() and r[pos+1].isdigit():
                    for port in range(5, 0, -1):
                        if finished == False:
                            for ip in range(15, 6, -1):
                                proxy = f"{r[pos-ip:pos]}{r[pos:pos+port]}"
                                if re.match(pattern, proxy):
                                    proxies.add(proxy)
                                    localproxycount = 1
                                    proxycount += 1
                                    finished = True
                                    break
                            
                        else:   
                            finished = False
                            break
                r = r.replace(":", "", 1)
    if site in goodsites and localproxycount == 0:
        print(f"{white}[{Colors.orange}!{white}] No proxies were found on {color}{site}")
        if clearingproxy == True:
            goodsites.remove(site)
    threadcount -= 1

def terminal(string:str = ""):
    ctypes.windll.kernel32.SetConsoleTitleW("KC Scraper | github.com/Kuucheen " + string)

def terminalthread():
    while len(sitelist) > 0:
        terminal(f"| Remaining sites {len(sitelist)} | active threads {threadcount} | Proxies {proxycount} | Time {time.time()-start:.2f}s")




main()