import flickrapi
import requests
import os
from geopy.geocoders import Nominatim

flickr = flickrapi.FlickrAPI(api_key="81438abee2dcd6ccbaccf53858b03005",
                                 secret="e143afb94c64e1df")

def create_url(id, server, farm, secret):
    url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(farm, server, id, secret)
    return url

def flickr_download(keyword):
    geolocator = Nominatim()
    #location = geolocator.geocode(city)
    photos = flickr.walk(text = keyword,
                         #tags = keyword,
                         per_page=200,
                         sort="relevance",
                         safe_search = "moderate",
                         #accuracy=11,
                         #lat=location.latitude,
                         #lon=location.longitude
                         )
    os.makedirs("imagesEmpty/"+keyword, exist_ok=True)
    for count, photo in enumerate(photos):
        try:
            secret = photo.get('secret')
            id = photo.get('id')
            server = photo.get('server')
            farm = photo.get('farm')
            url = create_url(id, server, farm, secret)
            file_name = "imagesEmpty/{}/{}_{}.jpg".format(keyword, keyword, id)
            download_image(file_name, url)
        except Exception as e:
            print("Failed to download image")
            print(e)
        if count == 199: break

def download_image(name, url):
    img_data = requests.get(url).content
    with open(name, 'wb') as handler:
        handler.write(img_data)

def main():
	file = open("bos.txt").read().splitlines()
	for place in file:
		print("Downloading {}...".format(place))
		flickr_download(place)

main()
