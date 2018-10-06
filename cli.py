import click
import requests
import os 
import sys

from utils import unsplashURL, dirExists, getCollectionPhotos, calc_percentage

__author__ = "Oyetoke Toby"


@click.group()
def main():
    """
    Simple CLI for dwonload Unsplash collections
    """
    pass

@main.command()
@click.argument('id')
def get(id):
    """This return a particular book from the given id on Google Books"""
    url = unsplashURL("collections/%s" % id)
    
    r = requests.get(url)
    c = r.json()

    click.echo("{0} - {1} items".format(c["title"], c["total_photos"]))

@main.command()
@click.argument('id')
def download(id):
    """This download all photos of the given collection"""
    # Container
    photos = []

    # Counters
    count = 0
    i = 0
    current_page = 1

    is_curated = len(id) <= 3 and len(id) > 0

    if is_curated:
        collection_url = unsplashURL("collections/curated/%s" % id)
    else:
        collection_url = unsplashURL("collections/%s" % id)

    res = requests.get(collection_url)
    col = res.json()

    total_photos = col["total_photos"]

    if (dirExists(col["title"]) == False):
        os.mkdir(col["title"])
    
    while total_photos != count:
        response = requests.get( getCollectionPhotos(is_curated, id, current_page) )
        
        sys.stdout.write("\r Download preparation: {0}".format(calc_percentage(count, total_photos)))
        sys.stdout.flush()

        if response.status_code != 200:
            break

        data = response.json()

        count += len(data)
        current_page += 1

        for photo in data:
            photo_id = photo["id"]
            download_url = photo["urls"]["raw"]

            photos.append({
                "id": photo_id,
                "url": download_url,
                "collection": {
                    "id": id,
                    "title": col["title"]
                }
            })

    sys.stdout.write("\r Download preparation: {0}".format(calc_percentage(count, total_photos)))
    sys.stdout.flush()
    
    for photo in photos:
        progressbar_size = 25

        path = "%s/%s.jpg" % (photo["collection"]["title"], photo["id"])

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

                    loading = "\r {5} - {3} of {4} - [{0}{1}] {2}".format("="*done, ' '*(
                        progressbar_size-done), percentage, i, count, photo["collection"]["title"])

                    sys.stdout.write(loading)
                    sys.stdout.flush()

        i += 1



if __name__ == "__main__":
    main()
