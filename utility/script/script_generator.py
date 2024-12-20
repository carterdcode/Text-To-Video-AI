import os
import json
from openai import OpenAI
import requests

from utility.video.video_search_query_generator import fix_json

model = "gpt-4o"

def generate_script(template, topic):

    # Load the prompts from the prompts.json file and select the appropriate prompt 
    # based on the template given when calling the function
    #open current directory and read the script_prompts.json file
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    print("Current directory: ", BASE_DIR)
    with open(os.path.join(BASE_DIR, "script_prompts.json"), "r") as file:
        data = json.load(file)
    if template == "facts":
        print("Template is facts")
        prompt = data.get("facts_prompt", {}).get("prompt", "Prompt not found")
        print("Prompt is: ", prompt)
    elif template == "mens":
            prompt = data.get("mens_motivation_prompt", {}).get("prompt", "Prompt not found")
    elif template == "travel":
            prompt = data.get("travel_prompt", {}).get("prompt", "Prompt not found")
    elif template == "what_if" or template == "whatif":
            prompt = data.get("what_if_prompt", {}).get("prompt", "Prompt not found")
    else:
        prompt = "Invalid template provided. Please provide a valid template: facts, mens, or travel."

    payload = {
        "model": "gpt-4o",
        "temperature": 0.9,
        "messages": [{"role": "system", "content": prompt},
                     {"role": "user", "content": topic}]
    }

    #TODO: Convert to client call instead of requests to allow retry and block ChatGPTEs
    # Send the POST request to the chat completions endpoint 
    response = requests.post("http://localhost:1337/v1/chat/completions", json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response text
        print("\n Response.text:\n" + response.text + "\n")
        
        try:
            content = response.json()["choices"][0]["message"]["content"]
            print("\n content:\n ", content)
            #remove \ and decode JSON string
            content =  content.replace("\\", "")
            script = json.loads(content)["script"]
            return script
        except Exception as e:
            print("Unexpected response format or parsing error:", e)
            print("Trying to fix json")
            fix_json(content)
            try:
                script = json.loads(content)["script"]
                return script
            except Exception as e:
                print("Failed to parse JSON after fixing: \n", content, "\n")
                print("generate_script returned None because of an exception, namely:")
                print(e)
                return None
    else:
        print(f"Request failed with status code {response.status_code}")
        print(" \n Response:", response.text + "\n")
        return None
        
