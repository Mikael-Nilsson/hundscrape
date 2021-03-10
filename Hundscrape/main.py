
import io
import pathlib
import hashlib
import requests
from bs4 import BeautifulSoup
from PIL import Image
from datetime import date
import os
import re

import logging
import azure.functions as func

# import dogcsv
# import dogbox

# chrome_path = "chromedriver_win32\\chromedriver.exe"
# # chrome_path = "chromedriver_linux64/chromedriver"
# shelters = [
#     {   "name": "hundarutanhem",
#         "url": [
#             "https://hundarutanhem.se/hundarna/mellanstora-hundar/",
#             "https://hundarutanhem.se/hundarna/stora-hundar/"
#         ],
#         "element_tree": {
#             "classes": "polaroid", "location": "img", "source": "src"
#         },
#         "outfile": "hundarutanhem.csv"
#     },
#     {
#         "name": "hundstallet",
#         "url": ["https://hundstallet.se/soker-hem/"],
#         "element_tree": {
#             "classes": "small-12 medium-6 large-4 cell", "location": "img", "source": "src"
#         },
#         "outfile": "hundstallet.csv"
#     }
# ]


# dogfolder = "/" + os.getenv('DROPBOX_DOGFOLDER', 'no dropbox folder')


# ## returns folder path
# def outPath(shelter):
#     return "/hundar/" + shelter["name"] + "/" + date.today().strftime("%Y%m%d")

# ## return folder path on dropbox
# def dropbox_path(shelter):
#     return dogfolder + "/" + shelter["name"] + "/" + date.today().strftime("%Y%m%d")


# ## extracts image urls from web site content
# def parse_image_urls(content, classes, location, source):
#     soup = BeautifulSoup(content)
#     results = []
#     for a in soup.findAll(attrs={"class": classes}):
#         name = a.find(location)
#         if name not in results:
#             results.append(name.get(source))
#     return results


# ## downloads image from url to directory
# def get_and_save_image_to_file(image_url, output_dir):
#     response = requests.get(image_url, headers={"User-agent": "Mozilla/5.0"})
#     image_content = response.content
#     image_file = io.BytesIO(image_content)
#     image = Image.open(image_file).convert("RGB")
#     filename = get_filename_from_url(image_url) + ".png"
#     file_path = output_dir + '/' + filename
#     # image.save(file_path, "PNG", quality=80)
#     dogbox.upload_data(image_content, file_path)


# # finds filename part of url
# def get_filename_from_url(url):
#     slash = url.rfind("/") + 1
#     surname = url.rfind(".")
#     file_name = url[slash:surname]
#     return file_name


# # Saves all images from site on url
# def download_dogs_from_shelter(shelter):

#     image_urls = []

#     outFolder = dropbox_path(shelter)

#     for url in shelter["url"]:
#         print("collecting dogs")
#         print(url)
#         content = get_content_from_url(url)
#         url_list = parse_image_urls(
#             content=content, classes=shelter["element_tree"]["classes"], location=shelter["element_tree"]["location"], source=shelter["element_tree"]["source"]
#         )
#         image_urls.extend(url_list)

#     save_names_to_csv(image_urls, dogfolder + "/" + shelter["outfile"])

#     for image_url in image_urls:
#         print(image_url)
#         get_filename_from_url(image_url)
#         get_and_save_image_to_file(
#             # image_url, output_dir=pathlib.Path(outFolder),
#             image_url, output_dir=outFolder,
#         )


# ## adds current list of dog names to csv file
# def save_names_to_csv(image_urls, dogfile):
#     dogs, fields=dogbox.read_csv(dogfile, ",")

#     dogNames = []
#     for url in image_urls:
#         dogNames.append(dogname_from_url(url))

#     today = date.today().strftime("%Y%m%d")

#     dogs = dogcsv.addDate(dogs, dogNames, today)
#     fields.append(today)
#     # dogcsv.write_csv_file(dogs, fields, dogfile, ',')
#     dogbox.write_csv(dogs, fields, dogfile, ',')


# ## extracts dog name from image url
# def dogname_from_url(stringToSearch):
#     idx = 0
#     newIdx = 0
#     failsafe = 1000
#     while newIdx != -1 and failsafe > 0:
#         failsafe -=1
#         newIdx = stringToSearch.find('/', idx+1)

#         if not newIdx == -1:
#             idx = newIdx

#     dogName = ""

#     try:
#         fullName = stringToSearch[idx+1:len(stringToSearch)]
#         dogIdSpan = re.search(r"-\d+x\d+", fullName)
#         dogName = fullName[0:dogIdSpan.start()]
#     except:
#         print("error while trying to extract dogname")
#         print(stringToSearch)
#         if not fullName == "":
#             print(fullName)
#         if not dogIdSpan == "":
#             print(dogIdSpan)


#     return dogName


# def main(event, context):
#     for shelter in shelters:
#         download_dogs_from_shelter(shelter)

#     return 0

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
             "Hey, an Azure function!",
             status_code=200
        )

if __name__ == "__main__":
    main(none)
