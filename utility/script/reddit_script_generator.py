import os
import json
from utility.video.video_search_query_generator import fix_json
from g4f.client import Client
from g4f.Provider import (
    Blackbox, # 4o
    DarkAI, #4o
    Liaobots, # 4o
    RetryProvider
)

client = Client(
    provider=RetryProvider([
        Blackbox, # 4o
        DarkAI, #4o
        Liaobots, # 4o
    ])
)

model = "gpt-4o"
messages = []
def generate_reddit_script(topic):


    # Load the prompts from the prompts.json file and select the appropriate prompt 
    # based on the template given when calling the function
    #open current directory and read the script_prompts.json file
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    print("Current directory: ", BASE_DIR)
    with open(os.path.join(BASE_DIR, "script_prompts.json"), "r",encoding='utf-8') as file:
        data = json.load(file)
        prompt = data.get("reddit_story_prompt", {}).get("prompt", "Prompt not found")
        example1 = data.get("reddit_story_prompt", {}).get("example1", "Prompt not found")
        example2 = data.get("reddit_story_prompt", {}).get("example2", "Prompt not found")
        print("Prompt is: ", prompt + " " + example1 + " " + example2)

    messages.append({"role": "user", "content": prompt})
    messages.append({"role": "user", "content": example1})
    messages.append({"role": "user", "content": example2})
    messages.append({"role": "user", "content": "The topic is: " + topic})

    #TODO: Convert to client call instead of requests to allow retry and block ChatGPTEs
    # Send the POST request to the chat completions endpoint 
    try:
        # Get GPT's response
        response = client.chat.completions.create(
            messages=messages,
            model=model
        )
        content = response.choices[0].message.content       
        print ("res.choices", response.choices)
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
            script = json.loads(content)["story"]
            return script
        except Exception as e:
            print("Failed to parse JSON after fixing: \n", content, "\n")               
            print("generate_script returned None because of an exception, namely:")
            print(e)
            return None
