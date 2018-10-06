import sys
import os
import threading
import requests
from Queue import Queue

# Local libs
from Download import DownloadThread

def download(photos, destfolder="photos", numthreads=4):
    queue = Queue()
    for photo in photos:
        queue.put(photo)

    for i in range(numthreads):
        t = DownloadThread(queue, destfolder)
        t.start()

    queue.join()

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


def dirExists(path):
    return os.path.isdir(path)


def unsplashURL(pathname, query=False):
    c_id = "4c29b3461e0cbb98c8f8cbb00fd13cffcfd7746f209b57097d1ffefa06fd352a"
    c_sec = "2b269ee625b6b60f35b1b7a01123bfcd7cc9201e2d8f5b568ced854a048fc569"

    if query:
        return "https://api.unsplash.com/" + pathname + "?client_id=" + c_id + "&client_secret=" + c_sec + "&" + query

    return "https://api.unsplash.com/" + pathname + "?client_id=" + c_id + "&client_secret=" + c_sec


def getCollectionPhotos(curated, collection, page=1):
    if curated:
        return unsplashURL("collections/curated/" + collection + "/photos") + "&page=" + str(page)

    return unsplashURL("collections/" + collection + "/photos") + "&page=" + str(page)


def calc_percentage(value, total):
    return "{0}%".format(round(100.00 * value / total, 2))
