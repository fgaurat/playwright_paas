import sys
import argparse
import os
import base64
import requests
import urllib.parse
import unicodedata
import re
import random
from playwright.sync_api import Playwright, sync_playwright, expect
from pprint import pprint


def slugify(value):
    value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def run(playwright: Playwright,keyword="") -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")
    page.get_by_role("button", name="Tout accepter").click()
    page.get_by_role("combobox", name="Rech.").click()
    page.get_by_role("combobox", name="Rech.").fill(keyword)
    page.get_by_role("combobox", name="Rech.").press("Enter")
    page.wait_for_selector("#bres")
    page.wait_for_timeout(2000)
    
    
        
    for i in range(3):    
        print(f"Scrolling {i}")
        elements = page.query_selector_all("div[data-q]")
        page.wait_for_timeout(4000)
        for element in elements:
            element.click()
    print("Done")
    # page.wait_for_timeout(4000)

    page.wait_for_timeout(1000)
    elements = page.query_selector_all("div[data-q]")
    for element in elements:
        if element.query_selector("span"):
            # pprint(element)
            print(element.get_attribute('data-q'))
            # print(element.text_content())

    # Suggests
    # elements = page.query_selector_all("#bres a")
    # for element in elements:
    #     print(element.text_content())


    # page.locator("#bres a").get_by_role("link", name="Images").click()
    # elements = page.query_selector_all(".isv-r")

    # for i_elem,element in enumerate(elements):
    #     # a = element.query_selector_all(".islib")
    #     if element.query_selector("h3"):
            
    #         all_buttons = element.query_selector_all("[role='button']")
    #         for button in all_buttons:
    #             button.click()
    #             if button.get_attribute("href"):
    #                 url = button.get_attribute("href")
    #                 parsed_url = urllib.parse.urlparse(url)
    #                 captured_value = urllib.parse.parse_qs(parsed_url.query)
    #                 imgurl = captured_value["imgurl"][0]
    #                 try:
    #                     response = requests.get(imgurl,verify=False,timeout=10)
    #                     if response.status_code == 200:
    #                         slug_kw = slugify(keyword)
    #                         # slug_image = slugify(element.query_selector("h3").text_content())
    #                         slug_image =imgurl.split("/")[-1]
    #                         if "?" in slug_image:
    #                             slug_image = slug_image.split("?")[0]
    #                         if "." not in slug_image:
    #                             slug_image = slug_image + ".jpg"
                            
    #                         # make directory in ./images from keyword
    #                         if not os.path.exists(f"./images/{slug_kw}"):
    #                             os.makedirs(f"./images/{slug_kw}",exist_ok=True)
                            
    #                         filename = f"./images/{slug_kw}/{i_elem}_{slug_image}"
    #                         with open(filename, "wb") as fh:
    #                             fh.write(response.content)
    #                         # exif_delete(filename,filename)
    #                         print(f"Downloaded {filename}")
    #                         break
    #                 except Exception as e:
    #                     print(e)
    #                     continue


    context.close()
    browser.close()