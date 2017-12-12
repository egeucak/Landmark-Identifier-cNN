from googleplaces import GooglePlaces
import os
import requests

def download_image(name, url):
    img_data = requests.get(url).content
    with open(name, 'wb') as handler:
        handler.write(img_data)

def search(keyword):
    query_result = google_places.text_search(keyword)
    return query_result

def download_photos(query_result):
    for place in query_result.places:
        try:
            print(os.path.dirname(place.name))
            os.makedirs(place.name, exist_ok=True)
            # Returned places from a query are place summaries.
            print ("Downloading",place.name)
            for photo in place.photos:
                photo.get(maxheight=4000, maxwidth=4000)
                fileName = place.name+'/'+photo.filename
                download_image(fileName,photo.url)
        except Exception as e:
            print(e)

#key = 'AIzaSyCRqdrW3oUqp9PsDNGZgsfok7OPhPJc-Qs'
#key = 'AIzaSyDccVp9m30qGfIYNqLlM7G2gg7e-dpIc4g'
#key = 'AIzaSyCVI6RvruxGGFK_7huHg_lh1IybOZvgeSA'
#key = 'AIzaSyAWvXrxYXLpqG_2o0KxQueH8UMGZWGUZyc'
#key = 'AIzaSyDWUruDOgB_PMrT-OsP0QywOD7t6mTVDi0'
key = 'AIzaSyCB8eNS_Ben6IYO_Z7073EvI2LGqwXlPqA'
google_places = GooglePlaces(key)

with open('C:/Users/Mavi/Documents/GitHub/land-mark-identifier/locations/istanbul.txt','r') as file:
    content = file.read().splitlines()
    for keyword in content:
        download_photos(search(keyword))
