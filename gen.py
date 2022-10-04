import requests as rq
import os
import random
import time
from dotenv import load_dotenv
from imap_tools import MailBox, AND
from bs4 import BeautifulSoup
from colorama import Fore
from datetime import datetime
from string import ascii_letters, digits
from threading import Thread, Semaphore, Lock
from urllib.parse import unquote

load_dotenv()

CATCHALL = os.getenv('CATCHALL')
IMAPSERVER = os.getenv('IMAPSERVER')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
PROXYS = []
emaillock = Semaphore(15)
filelock = Lock()
dontcheck = 99999999999999999
discountcounter = {
    50:0,
    75:0,
    100:0 
}


def setTitle(discount=None):
    global discountcounter
    if discount:
        discountcounter[discount]+=1
    else:
        discountcounter = {
            50:0,
            75:0,
            100:0 
        }
    os.system(f"title 100%: {discountcounter[100]}  75%: {discountcounter[75]}  50%: {discountcounter[50]}")
            

def loadProxies():
    global PROXYS
    p = []
    with open("proxies.txt", "r") as file:
        for line in file.readlines():
            if len(line) != 0:
                line = line.replace('\n', '')
                p.append({
                    "http":f"http://{line}",
                    "https":f"http://{line}"
                })
    PROXYS = p


def log(text,color,taskid):
        print(color + f"[{datetime.now().strftime('%H:%M:%S')}] [Task {taskid}] " + str(text) + Fore.RESET)


def createBahncardVoucher(proxy):
    if "@" in CATCHALL:
        data = {
            'e': f'{CATCHALL.split("@")[0]}+{"".join(random.choices(ascii_letters+digits, k=random.randint(10,20)))}@{CATCHALL.split("@")[1]}',
            'k': '1',
            'g': '0',
        }
    else:
        data = {
            'e': f'{"".join(random.choices(ascii_letters+digits, k=random.randint(10,25)))}@{CATCHALL}',
            'k': '1',
            'g': '0',
        }
    response = rq.post('https://www.probebahncard.de/api/abschicken?TNB=Zustimmung', json=data, proxies=proxy, timeout=15)
    response.raise_for_status()
    return data["e"]

def fetchVerificationCodeFromEmail(email):
    with emaillock:
        attempts = 0
        while True:
            with MailBox(IMAPSERVER).login(EMAIL, PASSWORD) as mailbox:
                for message in mailbox.fetch(AND(to=email), reverse=True):
                    emailcontent = BeautifulSoup(message.html, 'html.parser')
                    link = emailcontent.find('a', {'title': 'E-Mail-Adresse verifizieren & eCoupon erhalten'})['href']
                    code = link.split("=")[1]
                    mailbox.delete(message.uid)
                    return unquote(code)
                if attempts == 40 or dontcheck < time.time():
                    raise Exception("Cant find the Email")
                time.sleep(1)
                attempts+=1


def submitVerificationCode(code, proxy):
    data = {
    'ig': code,
    }
    response = rq.post('https://www.probebahncard.de/api/confirmation', json=data, proxies=proxy, timeout=15)
    response.raise_for_status()
    return response.json()


def create(taskid):
    if len(PROXYS) != 0:
        proxy = random.choice(PROXYS)
    else:
        proxy = {}

    try:
        email = createBahncardVoucher(proxy)
    except Exception as e:
        log(e, Fore.RED, taskid)
        return

    log(f"Fetching verification code from {email} ....", Fore.BLUE, taskid)

    try:
        code = fetchVerificationCodeFromEmail(email)
    except Exception as e:
        log(e, Fore.RED, taskid)
        return

    log(f"Submiting verification code ({code}) to the Deutsche Bahn server", Fore.MAGENTA, taskid)

    try:
        voucher = submitVerificationCode(code, proxy)
    except Exception as e:
        log(e, Fore.RED, taskid)
        return

    log(f"Got the Voucher {voucher['e']} with a {voucher['g']}% discount", Fore.GREEN, taskid)
    with filelock:
        setTitle(int(voucher['g']))
        with open(f"codes/{voucher['g']}.txt", "a") as file:
            file.write(f"{voucher['e']}\n")

if __name__ == "__main__":
    while True:
        setTitle()
        vouchers = int(input("How many codes to you want to generate? "))
        if input("Do you want to use proxys? (y|n) ") == "y":
            loadProxies()
        else:
            PROXYS = []

        dontcheck = time.time()+180

        threadPool = []
        for task in range(1, vouchers+1):
            t = Thread(target=create, args=(task,))
            threadPool.append(t)
            t.start()

        while any(t.is_alive() for t in threadPool):
            time.sleep(1)

        print("--- Finished ---")
        if input("Do you want to generate more codes? (y|n) ") == "n":
            break
 
