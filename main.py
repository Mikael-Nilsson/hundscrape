
import io
import pathlib
import hashlib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from datetime import date
import os
import re

import dogcsv

chromePath = "chromedriver_win32\\chromedriver.exe"
# chromePath = "chromedriver_linux64/chromedriver"
shelters = [
    {   "name": "hundarutanhem",
        "url": [
            "https://hundarutanhem.se/hundarna/mellanstora-hundar/",
            "https://hundarutanhem.se/hundarna/stora-hundar/"
        ],
        "element_tree": {
            "classes": "polaroid", "location": "img", "source": "src"
        },
        "outfile": "hundarutanhem.csv"
    },
    {
        "name": "hundstallet",
        "url": ["https://hundstallet.se/soker-hem/"],
        "element_tree": {
            "classes": "small-12 medium-6 large-4 cell", "location": "img", "source": "src"
        },
        "outfile": "hundstallet.csv"
    }
]


# dogfile = 'dogs.csv'

## returns folder path
def outPath(shelter):
    return "hundar/" + shelter["name"] + "/" + date.today().strftime("%Y%m%d")


## downloads content of chosen url
def get_content_from_url(url):
    # add "executable_path=" if driver not in running directory
    driver = webdriver.Chrome(chromePath)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_content = driver.page_source
    driver.quit()  # We do not need the browser instance for further steps.
    return page_content


## extracts image urls from web site content
def parse_image_urls(content, classes, location, source):
    soup = BeautifulSoup(content)
    results = []
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))
    return results


## Saves urls as list in csv
def save_urls_to_csv(image_urls):
    df = pd.DataFrame({"links": image_urls})
    df.to_csv("links.csv", index=False, encoding="utf-8")


## downloads image from url to directory
def get_and_save_image_to_file(image_url, output_dir):
    response = requests.get(image_url, headers={"User-agent": "Mozilla/5.0"})
    image_content = response.content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert("RGB")
    filename = get_filename_from_url(image_url) + ".png"
    file_path = output_dir / filename
    image.save(file_path, "PNG", quality=80)


# finds filename part of url
def get_filename_from_url(url):
    slash = url.rfind("/") + 1
    surname = url.rfind(".")
    file_name = url[slash:surname]
    return file_name


# Saves all images from site on url
def save_images_from_shelter(shelter):

    image_urls = []

    outFolder = outPath(shelter)

    if not os.path.isdir(outFolder):
        os.mkdir(outFolder)

    ## TODO: This block will need to be updated for other dog shelters
    for url in shelter["url"]:
        print("collecting dogs")
        print(url)
        content = get_content_from_url(url)
        url_list = parse_image_urls(
            content=content, classes=shelter["element_tree"]["classes"], location=shelter["element_tree"]["location"], source=shelter["element_tree"]["source"]
        )
        image_urls.extend(url_list)

    save_urls_to_csv(image_urls)
    save_names_to_csv(image_urls, shelter["outfile"])

    for image_url in image_urls:
        print(image_url)
        get_filename_from_url(image_url)
        get_and_save_image_to_file(
            image_url, output_dir=pathlib.Path(outFolder),
        )


## adds current list of dog names to csv file
def save_names_to_csv(image_urls, dogfile):
    dogs, fields=dogcsv.readCsv(dogfile, ',')

    dogNames = []
    for url in image_urls:
        dogNames.append(dogname_from_url(url))

    today = date.today().strftime("%Y%m%d")
        
    dogs = dogcsv.addDate(dogs, dogNames, today)
    fields.append(today)
    dogcsv.writeCsv(dogs, fields, dogfile, ',')


## extracts dog name from image url
def dogname_from_url(stringToSearch):
    idx = 0
    newIdx = 0
    failsafe = 1000
    while newIdx != -1 and failsafe > 0:
        failsafe -=1
        newIdx = stringToSearch.find('/', idx+1)
        length = len(stringToSearch)-newIdx

        if not newIdx == -1:
            idx = newIdx

    fullName = stringToSearch[idx+1:len(stringToSearch)]

    # surNameIdx = fullName.find('.', len(fullName)-5) # not needed
    # firstName = fullName[0:surNameIdx]
    dogIdSpan = re.search(r"-\d+x\d+", fullName)

    dogName = fullName[0:dogIdSpan.start()]
    
    return dogName


def main():
    for shelter in shelters:
        save_images_from_shelter(shelter)



# if __name__ == "__main__":  #only executes if imported as main file
main()
