from __future__ import print_function

import urllib2
import requests
import os 
import json
import sys

# Local Libs
from utils import download, progress, dirExists, unsplashURL, getCollectionPhotos, calc_percentage

# Container 
photos = []

# Counters
count = 0
i = 0

# Collections
# collections = ["463870", "2254180"]
collections = ["463870"]
collection_folder = True

# Select picture quality
qualities = ["raw", "full", "regular", "small", "thumb"]
quality = qualities[0]


if dirExists("photos") == False:
    os.mkdir("photos")

if len(collections) == 0:
    print("No collections available")
    os._exit(1)

for collection in collections:
    current_page = 1
    collection_counter = 0
    is_curated = len(collection) <= 3 and len(collection) > 0

    if is_curated:
        collection_url = unsplashURL("collections/curated/" + collection)
    else:
        collection_url = unsplashURL("collections/" + collection)

    res = requests.get(collection_url)
    col = res.json()
    total_photos = col["total_photos"]
   
    if collection_folder and dirExists("photos/" + col["title"]) == False:
        os.mkdir("photos/" + col["title"])
        
    while total_photos != collection_counter:
        response = requests.get( getCollectionPhotos(is_curated, collection, current_page) )

        sys.stdout.write("\rGot: {0}".format(
            calc_percentage(collection_counter, total_photos)))
        sys.stdout.flush()

        if response.status_code != 200:
            break

        data = response.json()

        count += len(data)
        collection_counter += len(data)
        current_page += 1

        for photo in data:
            id = photo["id"]
            download_url = photo["urls"]["raw"]

            photos.append({
                "id": id,
                "url": download_url,
                "collection": {
                    "id": collection,
                    "title": col["title"]
                }
            })

    # Count 1 last time
    sys.stdout.write("\rGot: {0} items of {1}".format(
        collection_counter, total_photos))
    sys.stdout.flush()


for photo in photos:
    progressbar_size = 25
    i += 1
    if collection_folder:
        path = "photos/" + photo["collection"]["title"] + "/" + photo["id"] + ".jpg"
    else:
        path = "photos/" + photo["id"] + ".jpg"

    with open(path, "wb") as f:
        r = requests.get(photo["url"], allow_redirects=True, stream=True)
        total_length = r.headers.get('content-length')

        if total_length is None:
            f.write(r.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in r.iter_content(chunk_size=4096):
                dl += len(data)

                f.write(data)

                done = int(progressbar_size * dl / total_length)
                percentage = calc_percentage(done, progressbar_size)

                loading = "\r {5} - {3} of {4} - [{0}{1}] {2}".format("="*done, ' '*(progressbar_size-done), percentage, i, count, photo["collection"]["title"])

                sys.stdout.write(loading)
                sys.stdout.flush()



# download(photos, "photos")
