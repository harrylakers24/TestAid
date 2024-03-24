from hardcoded_dom import *
from constants import *

def first_screenshot_prompt_obj(encoded_image, prompt):
    return {
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
                    "text": "This is the landing page of the website. " + prompt
                },
            ],
        }

def first_assistant_prompt_obj(dom):
    return {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": f"""
                            Here is the DOM of the landing page of the website.
                            {dom}
                        """
            }
        ]
    }

def first_dom_prompt_obj():
    return {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
                                Given the DOM.

                                Please provide the first action to take to continue navigating through the site and complete the intended task of finding the ticket price for the event.
                                
                                {{
                                "selector": "(CSS selector for the element to interact with)",
                                "action": "(Selenium action to take, e.g. click, type, etc.)",
                                "value": "(Value to input if the action involves typing or selecting, otherwise null)",
                                "complete": false,
                                "explanation": "(Brief description of the purpose/explanation behind this action as a user using the website for the first time)"
                                }}

                                Don't return anything but the JSON.
                            """
                },
            ]
        }

def cont_from_screenshot_prompt_obj(image_data):
    return {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": 'image/png',
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": f"""
                                Here is the updated screenshot of the webpage after taking the previous action.

                                The DOM is the same as before.

                                Based on the new state of the webpage given in the image, please provide the next best action to continue navigating through the site and complete the intended task.

                                {{
                                "selector": "(CSS selector for the element to interact with)",
                                "action": "(Selenium action to take, e.g. click, type, etc.)",
                                "value": "(Value to input if the action involves typing or selecting, otherwise null)",
                                "complete": false,
                                "explanation": "(Brief description of the purpose/explanation behind this action as a user using the website for the first time)"
                                }}

                                If there are no more relevant actions to take on the current page, suggest navigating back to the previous page or to a different section of the website with JSON still.

                                Don't return anything but the JSON.
                            """
                },
            ],
        }


def cont_from_explanation_obj(explanation):
    return {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": explanation
                },
            ]
        }