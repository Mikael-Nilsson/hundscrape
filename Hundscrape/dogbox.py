# from PIL import Image
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.files import WriteMode
import io
import csv
import os
from io import StringIO

APP_KEY = os.getenv('DROPBOX_KEY', 'no dropbox key')
APP_SECRET = os.getenv('DROPBOX_SECRET', 'no dropbox secret')
auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)


# authorize_url = auth_flow.start()
# print("1. Go to: " + authorize_url)
# print("2. Click \"Allow\" (you might have to log in first).")
# print("3. Copy the authorization code.")
# auth_code = input("Enter the authorization code here: ").strip()

auth_code = os.getenv('DROPBOX_AUTH_TOKEN', 'no dropbox token')
dbx = dropbox.Dropbox(auth_code)
acct = dbx.users_get_current_account()
LOCALFILE = './dogs.csv'


def upload_file(local_path, dropbox_path):
    with open(local_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_path, mode=WriteMode('overwrite'))


def upload_data(data, dropbox_path):
    dbx.files_upload(data, dropbox_path, mode=WriteMode('overwrite'))


def read_data(dropbox_path):
    md, data = dbx.files_download(dropbox_path)
    return data.content

## Reads data from csv file on dropbox
def read_csv(dropbox_path, delimiter):
    lines = 0
    dogs = []

    _, data = dbx.files_download(dropbox_path)
    file = StringIO(data.content.decode())
    reader = csv.DictReader(file, delimiter=delimiter)
    fields = reader.fieldnames if reader.fieldnames is not None else []

    for row in reader:
        lines += 1
        dogs.append(row)

    print(f'read {lines} lines')
    return dogs, fields

## Writes data to csv file on dropbox
def write_csv(dogs, fields, path, delimiter):
    print('writing fields')
    print(fields)

    memFile = StringIO()
    writer = csv.DictWriter(memFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(dogs)
    test_str = memFile.getvalue()
    
    bitar = bytes(test_str, 'utf-8') 

    dbx.files_upload(bitar, path, mode=WriteMode('overwrite'))

