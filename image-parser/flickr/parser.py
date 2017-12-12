import flickrapi
import requests
import os
from geopy.geocoders import Nominatim

flickr = flickrapi.FlickrAPI(api_key="81438abee2dcd6ccbaccf53858b03005",
                                 secret="e143afb94c64e1df")

def create_url(id, server, farm, secret):
    url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(farm, server, id, secret)
    return url

def flickr_download(keyword, city):
    geolocator = Nominatim()
    location = geolocator.geocode(city)
    photos = flickr.walk(text = keyword,
                         tags = keyword,
                         per_page=200,
                         sort="relevance",
                         accuracy=11,
                         lat=location.latitude,
                         lon=location.longitude
                         )
    #os.makedirs("images/"+keyword, exist_ok=True)
    for count, photo in enumerate(photos):
        try:
            secret = photo.get('secret')
            id = photo.get('id')
            server = photo.get('server')
            farm = photo.get('farm')
            url = create_url(id, server, farm, secret)
            print(url)
            file_name = "images/{}/{}_{}.jpg".format(keyword, keyword, id)
            download_image(file_name, url)
        except Exception as e:
            print("Failed to download image")
            print(e)
        if count > 200: break

def download_image(name, url):
    img_data = requests.get(url).content
    with open(name, 'wb') as handler:
        handler.write(img_data)

def main():
    location = "../../locations"
    for text in os.listdir(location):
        city = text.split(".")[0]
        if text.split(".")[-1] == "txt":
            file = open(text).read().splitlines()
            for place in file:
                print("Downloading {}...".format(place))
                flickr_download(place, city)

main()