from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\PAVILION-15\\Desktop\\Vehicle Detection\\chromedriver.exe"

wd = webdriver.Chrome(PATH)

# def get_url_from_search():

search_topic = "Eicher Motors Bus in jpg"

search_topic = search_topic.replace(" ", "+")


def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    # url = "https://www.google.com/search?q=Bus+images&sxsrf=ALiCzsaHyNoQ3buSgIzVT8x1ccxl_kAJHA:1658422165831&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjF0tOAuIr5AhU9oGMGHf-lD1EQ_AUoAXoECAEQAw"
    # wd.get(url)
    url = wd.get("https://www.google.com/search?tbm=isch&q=" + search_topic + "&source" + str(1))

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)


urls = get_images_from_google(wd, 4, 25)

print(urls)

for i, url in enumerate(urls):
    # if "jpg" in url:
    try :
        download_image("", url, str(i) + ".jpg")
    except:
        continue
# if "png" in url:
# 	download_image("", url, str(i) + ".png")

wd.quit()

