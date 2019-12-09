from bs4 import BeautifulSoup
import cv2
import numpy as np
import urllib
import re
import requests
import json
import os
import glob
from pytube import YouTube

from io import BytesIO
from PIL import Image


UPLOAD_FOLDER = './deepfakes'

def download_video(link):
    yt = YouTube(link)
    yt.streams.filter(progressive=True).order_by('resolution').desc().first().download()

def getsizes(url):
    # get file size *and* image size (None if not known)
    try:
        image_raw = requests.get(url)
        image = Image.open(BytesIO(image_raw.content))
        width, height = image.size
    except:
        return -1, -1
    return width, height

def get_elements(page_link):
    try:
        if "youtube.com/" in page_link.lower():
            # videos
            os.chdir(UPLOAD_FOLDER)
            download_video(page_link)
            os.chdir('../')
            list_of_files = glob.glob(f'{UPLOAD_FOLDER}/*')
            latest_file = max(list_of_files, key=os.path.getctime)
            filepath = latest_file
            return [None, None, filepath]

        page_response = requests.get(page_link, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        
        paragraphs = page_content.find_all("p")
        clean_paragraphs = []

        # images
        if page_content.find('figure') != None:
            images = page_content.find('figure').find_all('img', src=True)
            figure = True
        else:
            images = page_content.find_all('img', src=True)
            figure = False

        clean_images = []

        for i, pg in enumerate(paragraphs):
            p = pg.text
            o = re.sub(r"\s+", " ", p)
            clean_paragraphs.append((i, o))
        print (len(clean_paragraphs), "paragraphs found.")

        for i, im in enumerate(images):
            viable = True

            url = im['src']
            url = url.strip('//')
            if 'http://' not in url and 'https://' not in url:
                url = 'http://' + url
            url.replace('&amp;', '&')

            if not figure and not url.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                viable = False 

            if viable and getsizes(url) >= (250, 250):
                clean_images.append((i, url))

        clean_images = list(set(clean_images))
        print (len(clean_images), "images found.")


        return [clean_paragraphs, clean_images, None]
    except Exception as e:
        print(e)
        return [None, None, None]

