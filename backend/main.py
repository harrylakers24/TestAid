import time
from telnetlib import EC

import anthropic
import base64
import os
import minify_html
import pyperclip
import requests
import base64
import json

from prompt_factory import *

from httpcore import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from constants import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv
load_dotenv()



# have a loop that keeps on going until we find the result from chatgpt

options = Options()
options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.ubcbiztech.com/produhacks-2024"

driver.get(url)

# Take a screenshot and save it to a file
driver.save_screenshot('produ_screenshot.png')

response = requests.get(url)
html_content = response.text

minified = minify_html.minify(html_content, minify_js=True, minify_css=True, ensure_spec_compliant_unquoted_attribute_values=True, keep_spaces_between_attributes=True)

# Sending image to chatgpt
# Step 1: Read the image
with open("produ_screenshot.png", "rb") as image_file:
    image_data = image_file.read()

# Step 2: Encode the image in base64
encoded_image = base64.b64encode(image_data).decode("utf-8")

client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

HAIKU_MODEL="claude-3-haiku-20240307"
SONNET_MODEL="claude-3-sonnet-20240229"
OPUS_MODEL="claude-3-opus-20240229"

# By now we have screenshot of landing page

messages=[]
messages.append(first_screenshot_prompt_obj(encoded_image, 'Please navigate and find the ticket price.'))
messages.append(first_assistant_prompt_obj(SHORTEN_PRODU_DOM))
messages.append(first_dom_prompt_obj())

# UNCOMMENT WHEN COMPLETE: ACTUAL RESPONSE
# message = client.messages.create(
#     model=SONNET_MODEL,
#     max_tokens=1024,
#     system=SYSTEM_PROMPT,
#     messages=messages
# )


MAX_LOOP = 2

while MAX_LOOP > 0:

    message = client.messages.create(
        model=SONNET_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages
    )

    # print(f"Loop {MAX_LOOP} plain text:{message.content[0].text}")
    
    response = json.loads(message.content[0].text)
    if response["complete"]:
        break

    # print the response and specify which loop
    print(f"Loop {MAX_LOOP}: {response}")

    # EXAMPLE_RESPONSE = {
    #     'selector': "a.nav-link-45.produhacks2024[href='#Tickets']",
    #     'action': 'click',
    #     'value': None,
    #     'complete': False,
    #     'explanation': 'Navigate to the Tickets section to find ticket price information'
    # }

    # Wait for a short period to ensure the page has loaded
    time.sleep(1)

    # Find the element using the CSS selector with the updated method
    element = driver.find_element(By.CSS_SELECTOR, response['selector'])

    # Click the element
    element.click()

    # Close the browser window after a short delay to observe the action
    time.sleep(1)  # This wait is optional, just to observe the click action

    # Take a screenshot and save it to a file
    screenshot_name = f'produ_screenshot_{MAX_LOOP}.png'
    driver.save_screenshot(screenshot_name)

    with open(screenshot_name, "rb") as image_file:
        image_data = image_file.read()

    # Step 2: Encode the image in base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    messages.append(cont_from_explanation_obj(response["explanation"]))
    messages.append(cont_from_screenshot_prompt_obj(encoded_image))

    # messages.append(response)
    MAX_LOOP -= 1

driver.quit()

# print(messages)
print(response)