import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv
load_dotenv()

import requests
from bs4 import BeautifulSoup
import base64


# have a loop that keeps on going until we find the result from chatgpt

options = Options()
options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.ubcbiztech.com/produhacks-2024"

driver.get(url)

# Take a screenshot and save it to a file
#driver.save_screenshot('produ_screenshot.png')






response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
print(soup.prettify())

# Close the browser window
driver.quit()

# Sending image to chatgpt
# Step 1: Read the image
with open("produ_screenshot.png", "rb") as image_file:
    image_data = image_file.read()

# Step 2: Encode the image in base64
encoded_image = base64.b64encode(image_data).decode("utf-8")


# Prepare the API request data
# Note: Replace 'YOUR_API_KEY' with your actual API key and adjust the 'data' dictionary according to the API's requirements.
headers = {
    "Authorization": os.environ["OPENAI_API_KEY"],
    "Content-Type": "application/json",
}

data = {
    "model": "gpt-3.5-turbo-0125",
    "messages": [{
        "role": "system",
        "content": "I want to find contact information, what do I click"
    }, {
        "role": "user",
        "content": encoded_image  # Or however the API expects the image data
    }]
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

# Step 5: Handle the response
if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code, response.text)

