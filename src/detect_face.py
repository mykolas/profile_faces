import cv2.cv as cv
import cv2
import sys
import os, os.path
import urllib2
import numpy
import json
import time
import socket

from cStringIO import StringIO
import PIL.Image as pil

total = 0
founded = 0

buff_data = []

def get_urls(search, start = 0):
    urls = []
    url ='https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+search+'&userip=INSERT-USER-IP&rsz=8&imgtype=face&start='+str(start)
    log("request to : "+url)
    request = urllib2.Request(url, None)
    response = urllib2.urlopen(request)
    results = json.load(response)
    if results['responseData'] == None:
        print(type(urls))
        print(urls)
        return urls
    results_arr = results['responseData']['results']
    if len(results_arr) != 0:
        for url in results_arr:
            urls.append(url['url'])
        log("\n".join(urls))
        urls = urls + get_urls(search, len(results_arr)+start)
    print(type(urls))
    print(urls)
    return urls

def download_img(url):
    log("downloading img from: " + url)
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    try:
        img_file = urllib2.urlopen(req)
        im = StringIO(img_file.read())
        source = pil.open(im).convert("RGB")
        bitmap = cv.CreateImageHeader(source.size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(bitmap, source.tostring())
        cv.CvtColor(bitmap, bitmap, cv.CV_RGB2BGR)
        return numpy.asarray(bitmap[:,:])
    except urllib2.HTTPError, err:
        #log("error: " + str(err.code))
        print("HTTPerror")
        return numpy.asarray([])

    except socket.timeout, e:
        # For Python 2.7
        print("timeout")
        return numpy.asarray([])

def process(img, out):
    global total
    global founded
    total = total + 1
    rects, img = detect(img)
    found_count = len(rects) 
    if found_count != 0 :
        founded += found_count
        #print("total: " + str(total))
        #print("founded: " + str(founded))
        #print("proc: " + str(founded/total*100))
        box(rects, img, out)

'''
def process(src, out):
    rects, img = detect(src)
    if len(rects) != 0 :
        box(rects, img, out)

def detect(path):
    img = cv2.imread(path)
    gray = img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cascade = cv2.CascadeClassifier("..\\cascades\\haarcascade_profileface.xml")
    rects = cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
    if len(rects) == 0:
        return [], img
    print("found")
    rects[:, 2:] += rects[:, :2]
    return rects, img
'''

def detect(img):
    gray = img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cascade = cv2.CascadeClassifier("..\\cascades\\haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
    if len(rects) == 0:
    #    print("not found")
        return [], img
    #print("found")
    #print(rects)
    #print(type(rects))
    rects[:, 2:] += rects[:, :2]
    return rects, img
def box(rects, img, out):
    global buff_data
    i = 0;
    if len(buff_data) > 500:
        print("clear")
        for filename, data in buff_data:
            cv2.imwrite(filename, data)
        buff_data = []
    for x1, y1, w, h in rects:
        print(len(buff_data))
        result = img[y1:h, x1:w]
        #cv2.imwrite(out+str(i)+".jpg", result)
        buff_data.append([out+str(i)+".jpg", result])
        #bufFilename.append(out+str(i)+".jpg")
        
        i = i + 1

def log(data):

    ''' 
    now = time.strftime("%c")

    file = open("..\\log.txt", "a")
    file.write(now + ":\n")
    file.write(data)
    file.write("\n")
    file.close()
    '''

def get_from_flickr_all():
    urls = []
    for i in range(15, 10000):
        get_from_flickr_one(i)
        log("downloaded block #" + str(i))
    

def get_from_flickr_one(i):
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=94e5d16ea5dd80ae5daeacb654816383&text=people&per_page=500&page=" + str(i) + "&format=json&nojsoncallback=1"
    urls = []
    request = urllib2.Request(url, None)
    response = urllib2.urlopen(request)
    results = json.load(response)
    #print(url)
    log("\n".join(results))
    if results['photos'] == None:
        return None
    if len( results['photos']['photo'] ) == 0:
        return None
    for result in results['photos']['photo']:
        tmp = 'http://farm' + str(result["farm"]) + '.static.flickr.com/' + str(result["server"]) + '/' + str(result["id"]) + '_' + str(result["secret"]) + '.jpg'
        #urls.append(tmp)
        result_downloaded = download_img(tmp)
        if result_downloaded.size != 0:
            log("writing file: " + str(result["id"]) + '_' + str(result["secret"]) + '.jpg')
            process(result_downloaded, "..\\detected_faces\\"+ str(result["id"]) + '_' + str(result["secret"]) + '.jpg')
            #cv2.imwrite("..\\test\\" + str(result["id"]) + '_' + str(result["secret"]) + '.jpg', result_downloaded)

    
def main():
    #test()
    #sys.exit("end")
    #urls = get_urls("profile+human+face")
    #for index, url in enumerate(urls):
    #    ext = url[-4:]
    #    result = download_img(url)
    #    if result.size != 0:
    #        log("writing file: " + str(index) + ".jpg")
    #        cv2.imwrite("..\\test\\" + str(index) + ".jpg", result)
    get_from_flickr_all()
    sys.exit("done")
    for root, _, files in os.walk("..\\test\\"):
        for f in files:
            process(os.path.join(root, f), "..\\result\\"+f)
if __name__ == "__main__":
    main()
