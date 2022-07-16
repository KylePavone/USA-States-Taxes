import requests
import threading
from time import sleep
from bs4 import BeautifulSoup
import fake_useragent


locker = threading.Lock()

def get_page():
    fake_header = fake_useragent.UserAgent().random
    header = {"user-agent": fake_header}
    url = "https://www.sale-tax.com/"
    response = requests.get(url, headers=header).text
    return response


def bs(page):
    soup = BeautifulSoup(page, "lxml")
    root = soup.find("table", class_="rate-table")
    return root


def get_state():
    state = bs(get_page()).find_all("strong")
    state_list = []
    for s in state:
        res = s.text
        state_list.append(res)
    return state_list


def get_state_rate():
    state_rate = bs(get_page()).find_all("td", class_="local-rate-range-col")
    rate_list = []
    for s_r in state_rate:
        res = s_r.text[0:6]
        rate_list.append(res.replace(" ", "%"))
    return rate_list


def thr_1():
    states = get_state()
    for state in states:
        with open("states.txt", "a") as file:
            locker.acquire()
            file.write(state + "\n")
            locker.release()
            sleep(2)
        print(f"{state} is written")


def thr_2():
    rates = get_state_rate()
    for rate in rates:
        with open("states.txt", "a") as file:
            locker.acquire()
            file.write(rate + "\n")
            locker.release()
            sleep(2)


first_thread = threading.Thread(target=thr_1, name="first_thread").start()
second_thread = threading.Thread(target=thr_2, name="second_thread").start()





















