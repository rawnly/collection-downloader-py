import sys
import os
import threading
import requests

class DownloadThread(threading.Thread):
    def __init__(self, queue, destfolder):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True

    def run(self):
        while True:
            photo = self.queue.get()
            try:
                self.download_photo(photo)
            except Exception, e:
                print "   Error: %s" % e
            self.queue.task_done()

    def download_photo(self, photo):
        # change it to a different way if you require
        name = photo["id"] + ".jpg"
        dest = os.path.join(self.destfolder, photo["collection"]["title"], name)
        url = photo["url"]

        print "[%s] Downloading %s -> %s" % (self.ident, url, dest)
        r = requests.get(url, allow_redirects=True)
        open(dest, "wb").write(r.content)
