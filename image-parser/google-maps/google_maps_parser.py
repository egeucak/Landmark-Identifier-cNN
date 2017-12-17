from googleplaces import GooglePlaces
import requests
import os
from selenium import webdriver
import win32api
from win32api import keybd_event
import time
import win32con
import win32clipboard

def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def right_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def type(keyCode):
    keybd_event(keyCode, 0, 0, 0)
    time.sleep(0.1)
    keybd_event(keyCode, 0, win32con.KEYEVENTF_KEYUP, 0)

def type_combo(keyCodes):
    for keyCode in keyCodes:
        keybd_event(keyCode, 0, 0, 0)
        time.sleep(0.1)

    for keyCode in reversed(keyCodes):
        keybd_event(keyCode, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)

def find_photographs_in_page():
    type_combo([17,70]) #ctrl + f
    type(70) #f
    type(79) #o
    type(84) #t
    type(79) #o
    type(27) #esc
    type(13) #enter

def scroll_down(): #More like spam spacebar
    win32api.SetCursorPos((21,202))
    left_click()
    time.sleep(0.1)

    for i in range(150):
        keybd_event(32, 0, 0, 0) #spacebar
        time.sleep(0.1)
    keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)

def get_HTML():
    right_click()
    time.sleep(0.4)

    win32api.SetCursorPos((95,433)) #inspect
    time.sleep(0.4)

    left_click()
    time.sleep(0.4)

    win32api.SetCursorPos((755,273)) #move to html
    time.sleep(0.4)

    right_click()
    time.sleep(0.4)

    win32api.SetCursorPos((877,361)) #copy
    time.sleep(0.4)

    win32api.SetCursorPos((920,361)) #copy outerHTML
    time.sleep(0.4)

    left_click()
    time.sleep(0.4)

    win32api.SetCursorPos((1035,146)) #close 'inspect' window
    time.sleep(0.4)

    left_click()
    time.sleep(0.4)

def resize_image_URL(url, var,rescale):

    multiplier = var
    if (url.split('.')[1]=='googleusercontent'):

        splits, end_parts, sizes =[],[],[]
        base, end = '', ''
        if('-k-no' in url): #https://lh5.googleusercontent.com/p/AF1QipOrs1d-8Tuo8b5LFPT1GBlj0vxFyQ_YnBcWFpVN=w203-h100-k-no-pi-0-ya68.49999-ro-0-fo100

            splits = url.split('=')
            edited_part_size = len(splits[-1])
            base = url[:-edited_part_size] #https://lh5.googleusercontent.com/p/AF1QipOrs1d-8Tuo8b5LFPT1GBlj0vxFyQ_YnBcWFpVN=
            end = splits[-1] #s528-k-no-pi1.328078-ya6.151398-ro-5.470948-fo100
            end_parts = end.split('k-no') #[s528-,-pi1.328078-ya6.151398-ro-5.470948-fo100]
            sizes = end_parts[0].split('-') #[s528,]

        elif('-no/' in url): #https://lh3.googleusercontent.com/-n2-czYORotg/Uu4FGTy46bI/AAAAAAAACVs/Vey6l6AIT5E/w579-h388-no/04.jpg

            splits = url.split('/')
            edited_part_size = len(splits[-1])+len(splits[-2])+1
            base = url[:-edited_part_size] #https://lh3.googleusercontent.com/-n2-czYORotg/Uu4FGTy46bI/AAAAAAAACVs/Vey6l6AIT5E/
            end = splits[-2]+'/'+splits[-1] # w579-h388-no/04.jpg
            end_parts = end.split('no/') #[w579-h388-,04.jpg]
            sizes = end_parts[0].split('-') #[w579,h388,]

        new_sizes = ''

        for i in range(len(sizes)-1):
            current_int = int(sizes[i][1:])

            if (rescale==True):
                multiplier = var/current_int
                rescale=False

            new_size = sizes[i][0]+str(int(current_int*multiplier))
            new_sizes+=new_size+'-'

        if('-k-no' in url):
            url = (base+new_sizes+'k-no')+''.join(end_parts[1:])
        elif('-no/' in url):
            url = (base+new_sizes+'no/')+''.join(end_parts[1:])

    return url

def download_image(name, url):
    url = resize_image_URL(url,1000,True)
    img_data = ''
    try:
        img_data = requests.get(url).content
        with open(name, 'wb') as handler:
            handler.write(img_data)
    except Exception as e:
        print(e)

def getURL(keyword,city_name): #Search for keyword and get the urls of all results.
    query_result = google_places.text_search(keyword+' '+city_name)
    urls=[]
    names=[]
    for place in query_result.places:
        place.get_details()
        urls.append(place.url)
        names.append(place.name)
        print(place.url)
    return urls,names

def search(): #This is obsolete. Use search2()
    with open('C:/Users/Mavi/Documents/GitHub/land-mark-identifier/locations/izmir.txt','r') as file:
        content = file.read().splitlines()
        browser = webdriver.Chrome()

        for keyword in content:
            browser.get('https://www.google.com/maps/place/'+keyword+' Izmir')
            time.sleep(2)
            find_photographs_in_page()
            time.sleep(1)
            scroll_down()
            time.sleep(1)
            get_HTML()
            time.sleep(1)
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            text_file = open('Izmir '+keyword+'.txt', "w")
            text_file.write(data)
            text_file.close()

    while 1==1:
        pass

def search2(keyword,city_name,URLs,names):
    i = 0
    for url in URLs:
        print('Downloading landscape ',names[i])
        browser.get(url)
        time.sleep(3.5)
        find_photographs_in_page()
        time.sleep(3.5)
        scroll_down()
        time.sleep(3.5)
        get_HTML()
        time.sleep(1)
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        text_file = open(city_name+' '+keyword+' '+names[i]+' '+str(i)+'.txt', "w") #copies HTML code to text files.
        text_file.write(data)
        text_file.close()
        i+=1

def find_and_downlad_URLs(location): #Reads text files and downloads the images it contains

    time_begin = time.time()
    count=1
    for text_file in os.listdir(location):
        if (len(text_file.split('.'))>1): #could be done in one line
            if(text_file[-3:]=='txt'):

                time_file_begin= time.time()

                file = open(location+text_file, 'r')
                file_name = text_file[:-4]

                content = file.read()
                contents = content.split("url(&quot;")

                os.makedirs(location+file_name, exist_ok=True)

                temp_name=0
                print('Now downloading ',file_name,' ',round(count*100/295,3),'%',' Total time spent: ',round(time_file_begin-time_begin,3),sep='')
                #for alt_content in contents[1:]:
                i = 1
                while i < len(contents):
                    alt_content = contents[i]
                    temp = alt_content.split("&quot")
                    try:
                        if(temp[0][:2]=='//'): #Some urls don't have http: in front of them
                            download_image(location+file_name+'/'+str(temp_name)+'.jpg','http://'+temp[0][2:])
                        else:
                            download_image(location+file_name+'/'+str(temp_name)+'.jpg',temp[0])
                        temp_name+=1
                        i+=2 #to avoid duplication
                    except Exception as e:
                        print (e)
                count+=1

#key = 'AIzaSyCRqdrW3oUqp9PsDNGZgsfok7OPhPJc-Qs'
#key = 'AIzaSyDccVp9m30qGfIYNqLlM7G2gg7e-dpIc4g'
#key = 'AIzaSyCVI6RvruxGGFK_7huHg_lh1IybOZvgeSA'
key = 'AIzaSyAWvXrxYXLpqG_2o0KxQueH8UMGZWGUZyc'
#key = 'AIzaSyDWUruDOgB_PMrT-OsP0QywOD7t6mTVDi0'
#key = 'AIzaSyCB8eNS_Ben6IYO_Z7073EvI2LGqwXlPqA'
google_places = GooglePlaces(key)

def mainHTML(): #To get HTMLs
    location = 'C:/Users/Mavi/Documents/GitHub/land-mark-identifier/locations/'

    browser = webdriver.Chrome() #move this out of function if you want to run mainHTML()

    for text_file in os.listdir(location):
        if (len(text_file.split('.'))>1):
            if(text_file.split('.')[1]=='txt'):
                file = open(location+text_file, 'r')
                content = file.read().splitlines()
                city_name = text_file[:-4]
                print('In city ',city_name)
                for keyword in content:
                    print('Searched for landscape ',keyword)
                    URLs, names = getURL(keyword,city_name)
                    search2(keyword,city_name,URLs,names)


#search()
find_and_downlad_URLs('C:/Users/Mavi/PycharmProjects/wc/photographs/')
