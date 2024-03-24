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

# Close the browser window
# driver.quit()

# Sending image to chatgpt
# Step 1: Read the image
with open("produ_screenshot.png", "rb") as image_file:
    image_data = image_file.read()

# Step 2: Encode the image in base64
encoded_image = base64.b64encode(image_data).decode("utf-8")


# Prepare the API request data
# Note: Replace 'YOUR_API_KEY' with your actual API key and adjust the 'data' dictionary according to the API's requirements.
# headers = {
#     "Authorization": os.environ["OPENAI_API_KEY"],
#     "Content-Type": "application/json",
# }

# data = {
#     "model": "gpt-3.5-turbo-0125",
#     "messages": [{
#         "role": "system",
#         "content": "I want to find contact information, what do I click"
#     }, {
#         "role": "user",
#         "content": encoded_image  # Or however the API expects the image data
#     }]
# }

# response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

# Step 5: Handle the response
# if response.status_code == 200:
#     print(response.json())
# else:
#     print("Error:", response.status_code, response.text)


client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

HAIKU_MODEL="claude-3-haiku-20240307"
SONNET_MODEL="claude-3-sonnet-20240229"

messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": 'image/png',
                        "data": encoded_image,
                    },
                },
                {
                    "type": "text",
                    "text": INITIAL_PROMPT
                },
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": 'Based on the information provided in the image, it appears that this is the landing page for the ProduHacks event organized by UBC BizTech. The image does not seem to have any direct contact information for BizTech. However, the navigation bar at the top of the page has several sections, including "About", "Schedule", "Tickets", "Testimonial", "Judges", and "Mentors". \n\nTo find how to contact BizTech, I would first click on the "About" section, as that is often where organizations provide their contact information. If the "About" section does not contain the contact details, I would then explore the other sections, such as "Judges" or "Mentors", as they may provide additional information about the organizers and how to get in touch with them.\n\nIf I still cannot find the contact information for BizTech after exploring the different sections, I would try to locate a "Contact" or "Get in Touch" page or link on the website. Alternatively, I may try searching for "UBC BizTech contact" or similar queries on the website to see if I can find the necessary information.' 
                },
            ]
        }]

MAX_LOOP = 1

while MAX_LOOP > 0:
    messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Here is the current DOM of the webpage I'm on:
                                    {SHORTEN_PRODU_DOM}

                                    Based on this DOM, please provide the next best action to take using Selenium to navigate through the site and complete the intended task.

                                    Return your response in the following JSON format without any additional context or explanation:

                                    {{
                                    "selector": "(CSS selector for the element to interact with)",
                                    "action": "(Selenium action to take, e.g. click, type, etc.)",
                                    "value": "(Value to input if the action involves typing or selecting, otherwise null)",
                                    "complete": (true if the overall task is now complete, false if further actions are needed),
                                    "intention": "(Brief description of the purpose/intention behind this action as a user using the website for the first time)"
                                    }}

                                    It's critical that the CSS selector for buttons is as precise as possible. Only include the "value" field if the action requires inputting or selecting a value.
                                """
                    }
                ]
            }
        )

    # message = client.messages.create(
    #     model=SONNET_MODEL,
    #     max_tokens=1024,
    #     system=SYSTEM_PROMPT,
    #     messages=messages
    # )
    #
    # response = json.loads(message.content[0].text)
    # if response["complete"]:
    #     break

    EXAMPLE_RESPONSE = {
        'selector': "a.nav-link-45.produhacks2024[href='#Tickets']",
        'action': 'click',
        'value': None,
        'complete': False,
        'intention': 'Navigate to the Tickets section to find ticket price information'
    }

    # Use the 'selector' value from the EXAMPLE_RESPONSE dictionary as the CSS selector
    message = EXAMPLE_RESPONSE['selector']

    # Wait for a short period to ensure the page has loaded
    time.sleep(3)

    # Find the element using the CSS selector with the updated method
    element = driver.find_element(By.CSS_SELECTOR, message)

    # Click the element
    element.click()

    # Close the browser window after a short delay to observe the action
    time.sleep(3)  # This wait is optional, just to observe the click action


    # messages.append(response)
    MAX_LOOP -= 1

EXAMPLE_RESPONSE = {'selector': "a.nav-link-45.produhacks2024[href='#Tickets']", 'action': 'click', 'value': None, 'complete': False, 'intention': 'Navigate to the Tickets section to find ticket price information'}

driver.quit()
