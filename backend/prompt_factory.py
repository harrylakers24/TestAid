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

def first_dom_prompt_obj(prompt):
    return {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
                                Given the DOM.
                                
                                Imagine you are a user testing a new website. You start on the page and your goal is to complete the intended prompt: {prompt}. Please provide detailed feedback on your experience as you navigate through the website.

                                Begin by describing your initial impressions of the page and any actions you take. As you proceed through the website, share your observations, thoughts, and feelings about the design, layout, and functionality of each page you encounter.

                                Highlight any positive aspects of the website that you appreciate, such as easy navigation, clear product information, or helpful features.

                                Also, point out any areas that could be improved or cause frustration, such as lack of filters, slow loading times, or confusing elements, lack of accessibility features. Provide specific suggestions on how these issues could be addressed to enhance the user experience.

                                Consider the overall user journey and whether the website effectively guides you towards completing your goal of finding and purchasing a product.

                                Lastly, offer any additional insights, recommendations, or questions you might have for the website developers if any.

                                Please be as descriptive and detailed as possible in your feedback, as if you were participating in a user testing interview. Your insights will be valuable in helping to improve the website's usability and user experience.

                                I won't be malicious, and will try to click the right buttons or places in order to complete the task.

                                Return your response in the following JSON format and nothing more in the response:

                                {{
                                "selector": "(CSS selector for the element to interact with)",
                                "action": "(Selenium action to take, e.g. click, type, etc.)",
                                "value": "(Value to input if the action involves typing or selecting, otherwise null)",
                                "complete": false,
                                "explanation": "(Brief explanation behind this action as a user using the website for the first time, be descriptive and clear on what you see and how you feel, the idea is to be as descriptive as possible to help the assistant understand the context and the action you are taking)"
                                }}

                                Don't return anything but the JSON.
                            """
                },
            ]
        }

def cont_from_screenshot_prompt_obj(image_data, prompt):
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

                                Based on the new state of the webpage given in the image, please provide the next best action and explanation to continue navigating through the site and complete the intended task like before.

                                Prompt: {prompt}

                                I won't be malicious, and will try to click the right buttons or places in order to complete the task.

                                Return your response in the following JSON format and nothing more in the response:

                                {{
                                "selector": "(CSS selector for the element to interact with)",
                                "action": "(Selenium action to take, e.g. click, type, etc.)",
                                "value": "(Value to input if the action involves typing or selecting, otherwise null)",
                                "complete": false,
                                "explanation": "(Brief explanation behind this action as a user using the website for the first time, be descriptive and clear on what you see and how you feel, the idea is to be as descriptive as possible to help the assistant understand the context and the action you are taking)"
                                }}

                                If there are no more relevant actions to take on the current page, return in JSON still.

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