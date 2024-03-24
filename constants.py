from hardcoded_dom import *

SYSTEM_PROMPT="""Pretend you're a general user in a user study. What would you look at given a prompt from user
        and how would you achieve it? Please describe your process in detail as if you're in a user study."""

INITIAL_DOM_PROMPT = f"""Here is the current DOM of the webpage I'm on:
                        {SHORTEN_PRODU_DOM}

                        Based on this DOM, please provide the next best action to take using Selenium to navigate through the site and complete the intended task.

                        Return your response in the following JSON format without any additional context or explanation:

                        {{
                        "selector": "(CSS selector for the element to interact with)",
                        "action": "(Selenium action to take, e.g. click, type, etc.)",
                        "value": "(Value to input if the action involves typing or selecting, otherwise null)",
                        "complete": (true if the overall task is now complete, false if further actions are needed),
                        "explanation": "(Brief description of the purpose/explanation behind this action as a user using the website for the first time)"
                        }}

                        It's critical that the CSS selector for buttons is as precise as possible. Only include the "value" field if the action requires inputting or selecting a value.
                    """

