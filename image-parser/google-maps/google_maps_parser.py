import requests
import os
from selenium import webdriver

def download_image(name, url):
    img_data = requests.get(url).content
    with open(name, 'wb') as handler:
        handler.write(img_data)

def search():
    with open('C:/Users/Mavi/Documents/GitHub/land-mark-identifier/locations/izmir.txt','r') as file:
        content = file.read().splitlines()
        browser = webdriver.Chrome()
        for keyword in content:
            browser.get('https://www.google.com/maps/place/'+keyword+' Izmir')
    while 1==1:
        pass

def find_and_download_urls():
    with open('xd.txt','r') as file:
        content = file.read()
        contents = content.split("url(&quot;")
        os.makedirs(content, exist_ok=True)
        temp_name=0
        for alt_content in contents[1:]:
            temp = alt_content.split("&quot")
            try:
                download_image(str(temp_name)+'.jpg',temp[0])
                temp_name+=1
            except Exception as e:
                print (e)

search()
