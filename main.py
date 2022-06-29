from selenium import webdriver
import requests as rq
import os
from bs4 import BeautifulSoup
import time

# Asking the user to enter the path to the chromedriver.exe file.
path = input("Enter Path: ")

# Asking the user to enter the url of the website from which the images are to be downloaded.
url = input("Enter URL: ")

output = "output"

# Takes a path to the chromedriver and a url and returns the html of the url:
def get_url(path, url):
    driver = webdriver.Chrome(executable_path=r"{}".format(path))
    driver.get(url)
    print("loading.....")
    res = driver.execute_script("return document.documentElement.outerHTML")
    return res

# Takes a response object and returns a list of image links:
def get_img_links(res):
    soup = BeautifulSoup(res, "lxml")
    imglinks = soup.find_all("img", src=True)
    return imglinks

# Downloads the image from the link and saves it in the output folder:
def download_img(img_link, index):
    try:
        extensions = [".jpeg", ".jpg", ".png", ".gif"]
        extension = ".jpg"
        for exe in extensions:
            if img_link.find(exe) > 0:
                extension = exe
                break
        img_data = rq.get(img_link).content
        with open(output + "\\" + str(index + 1) + extension, "wb+") as f:
            f.write(img_data)
        f.close()
    except Exception:
        pass

result = get_url(path, url)
time.sleep(60)
img_links = get_img_links(result)
if not os.path.isdir(output):
    os.mkdir(output)

for index, img_link in enumerate(img_links):
    img_link = img_link["src"]
    print("Downloading. Please wait a little longer...")
    if img_link:
        download_img(img_link, index)
print("Download complete!")