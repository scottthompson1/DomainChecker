from expressvpn import connect, disconnect, connect_alias, random_connect
from requests import get
from bs4 import BeautifulSoup
import socket
import os
import csv
pages_dir = "data/pages/"

def vpn_connect(alias = None):
    print("Connecting to ExpressVPN")
    # no option, random connect
    if alias == None:
        random_connect()
    else:
        connect_alias(alias)
    print("Connected to ExpressVPN")


def get_page(index, url, country):
    # request page
    try:
        req = get(url)
    except:
        return -1

    # create directory if needed
    dir_path = pages_dir + str(index) + "/"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    # grab page text
    html_page = req.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = "".join(soup.find_all(text=True))

    # save page information
    file_path = dir_path + country + ".html"
    with open(file_path, "w") as f:
        f.write(text.encode("utf-8"))

    # return page length
    return len(req.text)


# before connecting
ip = get('https://api.ipify.org').text
print 'My public IP address is:', ip

# connect to VPN
vpn_connect(alias = "itmi")

# after connecting
ip = get('https://api.ipify.org').text
print 'My public IP address is:', ip

# initialize csv writer
results_csv = open('data/results.csv', "w")
csvwriter = csv.writer(results_csv, delimiter=',')
## write header
csvwriter.writerow(["index","country","length"])

# set country
country = "Italy"

# load in domains
urls_path = "top-1m_chunks/top-1m_chunkaa"
n = 100
with open(urls_path, "r") as f:
    for i in range(1,n):
        # grab url from chunk file
        line = f.readline()
        index, url = line.split(",")
        url = "http://" + url.replace("\r\n","")
        print([index,url])

        # get page
        page_len = get_page(index, url, country)
        csvwriter.writerow([index, country, page_len])

# get page test
# url = "https://play.hbogo.com/"
# page_len = get_page(1, url, "Italy")
# print(page_len)

# disconnect from VPN
disconnect()
