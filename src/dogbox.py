# from PIL import Image 
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.files import WriteMode
import io
import os

APP_KEY = "flwxwqoh3slg386"
APP_SECRET = "6c0gpgd7cnqyaui"
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

def upload_data(image, dropbox_path):    
    dbx.files_upload(image, dropbox_path, mode=WriteMode('overwrite'))