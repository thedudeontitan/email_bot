import imaplib
import email
import webbrowser
import threading
import concurrent.futures
from email.header import decode_header
from operator import ipow
from time import sleep
import os
from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from config import users
from scrape import scrapeData

chromedriver_autoinstaller.install()
    
chrome_options = Options()

# driver = webdriver.Chrome(options=chrome_options)

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def get_link(acc):
    links = []
    while(True):
        status, messages = acc.select('Inbox')

        N = 1

        messages = int(messages[0])
        # print(messages)
        for i in range(messages, messages-N, -1):
            res, msg = acc.fetch(str(i), "(RFC822)")

            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    date = msg["Date"]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)
                    From, encoding = decode_header(msg.get("From"))[0]

                    if isinstance(From, bytes):
                        From = From.decode(encoding)

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                    if content_type == "text/html":
                        folder_name = clean(subject)+clean(date)

                        if not os.path.isdir(folder_name):
                            os.mkdir(folder_name)
                        
                        dirList = os.listdir()
                        filename = "index.html"
                        if(os.path.exists(os.path.join(folder_name, filename))):
                            pass
                        else:
                            filepath = os.path.join(folder_name, filename)
                            open(filepath, "w").write(body)
                            links = scrapeData(body)
                            # print(links)
                            
                            for i in links:
                                print(i)
                                # driver.get(i)
                                # driver.switch_to.new_window('window')
                                webbrowser.open_new(i)
                    print("="*100)

def logIN(user,password):
    imap_url = 'imap.gmail.com'
    acc = imaplib.IMAP4_SSL(imap_url)
    acc.login(user, password)
    print("login done")
    get_link(acc)

def main(a,b):
        try:
            logIN(a,b)
        except Exception as e:
            print(e)

executor = concurrent.futures.ProcessPoolExecutor(40)
futures = [executor.submit(main, i,users.get(i)) for i in users.keys()]
concurrent.futures.wait(futures)