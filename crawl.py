import requests
import os, re
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from fpdf import FPDF
import time
import glob
from PIL import Image
import img2pdf


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")

    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
    
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    return urls

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    filename = os.path.join(pathname, str(url.split("/")[-1]).strip())

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    
    with open(filename, "wb") as f:
        print(filename)
        for data in progress.iterable:            
        # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

    
def go(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each image, download it
        download(img, path)


def main():
    createFND()
    # Using readlines()
    file1 = open('link.html', 'r')
    Lines = file1.readlines()
    file1.close

    link =""
    name =""

    for line in Lines:
        print(line)
        text = bs(line, "lxml")
        name=text.text.replace(":","").replace('/[^0-9\.]+/g', "")

        for a in text.find_all('a', href=True):
            link = a['href']
            print(link)

            full_name = "/Users/edwinagyemang/python_projects/crawler/DS/"+name

        go(link, full_name)
    #naarpdf()

def topdf():
    location = "/Users/edwinagyemang/python_projects/crawler/FS/"

    list_of_images = glob.glob("/Users/edwinagyemang/python_projects/crawler/DS/*")

    # create a file to store the pdfs
    if not os.path.isdir(location+"pdf"):
        os.makedirs(location+"pdf")
    

    for folder in list_of_images:

        try:
            with open(folder+"pdf","wb") as f:
                f.write(img2pdf.convert(glob.glob(folder+"/*")))
        except:
            print("something wrong with"+folder)
            file = open(location+"error.html", "w+")
            file.write(folder)
            file.close()

def naarpdf():
    time.sleep(10)
    list_of_images = glob.glob("/Users/edwinagyemang/python_projects/crawler/DS/*")
    for folder in list_of_images:

        # use a folder that you created (here it's imgs)
        dir_list = [x for x in list_of_images] 
            # add new pages with the image 
        for directory in dir_list:
            height= 960
            width= 1500
            pdf = FPDF(format=(height,width),unit="pt")
            pdf.set_auto_page_break(0)
            #print(directory)
            image_list=sorted(os.listdir(directory))
            for img in image_list:                
                pdf.add_page()
                try:
                    pdf.image(directory.replace("?","")+"/"+img)
                except RuntimeError:
                    print("something wrong with"+folder)
                    file = open("/Users/edwinagyemang/python_projects/crawler/FS/error.html", "w+")
                    file.write("something wrong with "+directory)
                    file.close()


            # save the output file
            print(directory.split("/")[-1])
            pdf.output("/Users/edwinagyemang/python_projects/crawler/FS/pdf/"+directory.split("/")[-1]+".pdf",'F')
            print("Adding all your images into a pdf file")
            print("Images pdf is created and saved it into the following path folder:\n",
       
            os.getcwd())

def editnames():
    downloaded = sorted(glob.glob("/Users/edwinagyemang/python_projects/crawler/DS/*"))
    for folder in downloaded:
        images = sorted(glob.glob(folder+"/*"))
        for img in images:
            print(folder)
            os.rename(img, folder+img.split("/")[-1])

def createFND():
    if not os.path.isdir("/Users/edwinagyemang/python_projects/crawler/DS/"):
        os.makedirs("/Users/edwinagyemang/python_projects/crawler/DS/")
    if not os.path.isdir("/Users/edwinagyemang/python_projects/crawler/FS/pdf/"):
        os.makedirs("/Users/edwinagyemang/python_projects/crawler/FS/pdf/")
    