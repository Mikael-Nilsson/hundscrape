import requests
import pathlib
from bs4 import BeautifulSoup
from PIL import Image
import os
import io
import re
from datetime import date
import logging

from . import dogbox
from . import dogcsv


## return folder path on dropbox
def dropbox_path(shelter):
    return dogfolder() + "/" + shelter["name"] + "/" + date.today().strftime("%Y%m%d")


def dogfolder():
    tempFolder = os.environ['DROPBOX_DOGFOLDER']
    if not tempFolder:
        return 'no dropbox folder'
    else:
        return "/" + tempFolder


## finds filename part of url
def get_filename_from_url(url):
    slash = url.rfind("/") + 1
    surname = url.rfind(".")
    file_name = url[slash:surname]
    return file_name


## Gets source from web page.
#! This doesn't work with just any page, as it depends on how the page is built
def get_content_from_url(url):
    response = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
    page_content = response.content
    return page_content


## extracts image urls from web site content
def parse_image_urls(content, classes, location, source):
    soup = BeautifulSoup(markup=content, features="html.parser")
    results = []
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))
    return results


## downloads image from url to directory
def get_and_save_image_to_file(image_url, output_dir):
    response = requests.get(image_url, headers={"User-agent": "Mozilla/5.0"})
    image_content = response.content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert("RGB")
    filename = get_filename_from_url(image_url) + ".png"
    file_path = output_dir + '/' + filename
    # image.save(file_path, "PNG", quality=80)
    dogbox.upload_data(image_content, file_path)


## Saves all images from site on url
def download_dogs_from_shelter(shelter):

    image_urls = []

    outFolder = dropbox_path(shelter)

    for url in shelter["url"]:
        logging.debug("collecting dogs from " + url)
        print(url)
        content = get_content_from_url(url)
        url_list = parse_image_urls(
            content=content, classes=shelter["element_tree"]["classes"], location=shelter["element_tree"]["location"], source=shelter["element_tree"]["source"]
        )
        image_urls.extend(url_list)

    save_names_to_csv(image_urls, dogfolder() + "/" + shelter["outfile"])

    for image_url in image_urls:
        logging.debug(image_url)
        get_filename_from_url(image_url)
        get_and_save_image_to_file(
            # image_url, output_dir=pathlib.Path(outFolder),
            image_url, output_dir=outFolder,
        )


## adds current list of dog names to csv file
def save_names_to_csv(image_urls, dogfile):

    dogs, fields=dogbox.read_csv(dogfile, ",")

    dogNames = []
    for url in image_urls:
        dogNames.append(dogname_from_url(url))

    today = date.today().strftime("%Y%m%d")

    dogs = dogcsv.addDate(dogs, dogNames, today)
    fields.append(today)
    # dogcsv.write_csv_file(dogs, fields, dogfile, ',')
    dogbox.write_csv(dogs, fields, dogfile, ',')


## extracts dog name from image url
def dogname_from_url(stringToSearch):
    idx = 0
    newIdx = 0
    failsafe = 1000
    while newIdx != -1 and failsafe > 0:
        failsafe -=1
        newIdx = stringToSearch.find('/', idx+1)

        if not newIdx == -1:
            idx = newIdx

    dogName = ""

    try:
        fullName = stringToSearch[idx+1:len(stringToSearch)]
        dogIdSpan = re.search(r"-\d+x\d+", fullName)
        dogName = fullName[0:dogIdSpan.start()]
    except:
        print("error while trying to extract dogname")
        print(stringToSearch)
        if not fullName == "":
            print(fullName)
        if not dogIdSpan == "":
            print(dogIdSpan)

    return dogName
