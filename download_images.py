# based on https://github.com/BBarbosa/tflearn-image-recognition-toolkit/blob/
#                 4a0528dcfb206b1e45997f2fbc097aafacfa0fa0/scripts/html_link_parser.py
import re
import argparse

# Taken from: https://gist.github.com/Diyago/83919fcaa9ca46e4fcaa632009ec2dbd

import html5lib
from PIL import Image
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os


def html_url_parser(url, save_dir, show=False, wait=False):
    """
    HTML parser to download images from URL.
    Params:\n
    `url` - Image url\n
    `save_dir` - Directory to save extracted images\n
    `show` - Show downloaded image\n
    `wait` - Press key to continue executing
    """

    website = urlopen(url)
    html = website.read()

    soup = BeautifulSoup(html, "html5lib")  # this may require `html5lib` to be installed

    for i, link in enumerate(soup.find_all('a', href=True)):
        if (i == 0):
            continue

        img_url = link['href']

        try:
            if os.path.isfile(save_dir + "img-%d.png" % i) == False:
                print("[INFO] Downloading image from URL:", link['href'])
                image = Image.open(urlopen(img_url))
                image.save(save_dir + "img-%d.png" % i, "PNG")
                if (show):
                    image.show()
            else:
                print('skipped')
        except KeyboardInterrupt:
            print("[EXCEPTION] Pressed 'Ctrl+C'")
            break
        except Exception as image_exception:
            print("[EXCEPTION]", image_exception)
            continue

        if (wait):
            key = input("[INFO] Press any key to continue ('q' to exit)... ")
            if (key.lower() == 'q'):
                break


# ///////////////////////////////////////////////////
#                   Main method
# ///////////////////////////////////////////////////
if __name__ == "__main__":

    URL_TRAIN_IMG = "https://www.cs.toronto.edu/~vmnih/data/mass_roads/train/sat/index.html"
    URL_TRAIN_GT = "https://www.cs.toronto.edu/~vmnih/data/mass_roads/train/map/index.html"

    URL_TEST_IMG = "https://www.cs.toronto.edu/~vmnih/data/mass_roads/valid/sat/index.html"
    URL_TEST_GT = "https://www.cs.toronto.edu/~vmnih/data/mass_roads/valid/map/index.html"

    # Make directories
    os.makedirs('.data/training/raw', exist_ok=True)
    os.makedirs('.data/training/mask', exist_ok=True)
    os.makedirs('.data/validation/raw', exist_ok=True)
    os.makedirs('.data/validation/mask', exist_ok=True)

    # Training
    html_url_parser(url=URL_TRAIN_IMG, save_dir="./.data/training/raw/")
    html_url_parser(url=URL_TRAIN_GT, save_dir="./.data/training/mask/")

    # Test
    html_url_parser(url=URL_TEST_IMG, save_dir="./.data/validation/raw/")
    html_url_parser(url=URL_TEST_GT, save_dir="./.data/validation/mask/")

    print("[INFO] All done!")