import json
import re
from utility.utils import log_response,LOG_TYPE_GPT
import requests
from g4f.client   import Client
from g4f.Provider import (
    Blackbox, # 4o
    ChatGptEs, # 4o
    DarkAI, #4o
    Liaobots, # 4o

    RetryProvider
)

client = Client(
    image_provider = RetryProvider([
        Blackbox, # 4o
        ChatGptEs, # 4o
        DarkAI, #4o
        Liaobots, # 4o
    ])
)

model = "gpt-4o"

log_directory = ".logs/gpt_logs"

prompt = """# Instructions

Given the following video script and timed captions, create between 8 and 12 descriptive prompts based on the input text to be used for image generation. The prompts should be relevant to the input but you are free to be creative. If a caption is vague or general, you may choose something similar which fits or take context from surrounding words. Ensure that the prompts for each time period are strictly consecutive and cover the entire length of the video. Each prompt should cover exactly 6-10 seconds. The output should be in JSON format, like this: [[[t1, t2], ["prompt1"]], [[t2, t3], ["prompt2"]], ...]. Please handle all edge cases, such as overlapping time segments and vague or general captions.

For example, if the caption is 'Only 12 astronauts have walked on the Moon, all part of NASA's Apollo missions.', the prompt could be 'Long shot of an astronaut far away in a Martian landscape, under an otherworldly sky.' 

Important Guidelines:

Use only English in your prompts.
Each image prompt must depict something visual.
Use descriptive words like “eerie forest”, “serene seascape”, or “futuristic metropolis” to set the mood and feeling.
Don’t just say “beach” or “forest”. Give more detail and specify the geological location. Like "a tropical beach in the Bahamas with palm trees swaying in the breeze".
Mention materials like “glistening marble floors,” “rustic wooden beams,” or “crystal-clear water”
Describe your subject in detail. Shape, size, how things are positioned e.g. “twisted branches of ancient trees” or a “sleek, curved spacecraft.”
Mention colors you want, like “warm hues of a sunset” or “cool metal sheen of a cyberpunk city.” 
['Walking along the beach'] <= BAD, because it doesn't depict something visually and is not descriptive
['A long shot of a deer grazing in the midground during the day, vibrant wildflowers in the foreground, and a mountain range stretching across the background.'] <= GOOD, because it is descriptive and depicts something visual.
['Car', 'Car driving', 'Car racing', 'Car parked'] <= BAD, because it's 4 strings.
['A charming log cabin in the forest on a beautiful, sunny day.'] <= GOOD, because it's 1 string.
['Un chien', 'une voiture rapide', 'une maison rouge'] <= BAD, because the text query is NOT in English.


Remember you must create a minimum of 8 and maximum of 12 prompts.
Your response should be ONLY THE RESPONSE, no extra text or data. 
  """

def fix_json(json_str):
    print("Original JSON: ", json_str)
    json_str = json_str.strip()
   
    # Replace typographical quotes with straight quotes
    json_str = json_str.replace("“", "\"").replace("”", "\"").replace("‘", "\"").replace("’", "\"")

    # Replace all " which has at least one letter directly before and after it with \'
    json_str = re.sub(r'(?<=[a-zA-Z])\"(?=[a-zA-Z])', "\'", json_str)
    # Ensure the JSON starts and ends with square brackets 
    if not json_str.startswith("["):
        json_str = "[" + json_str
    if not json_str.endswith("]"):
        json_str = json_str + "]]]"

    print("Fixed JSON String:", json_str)
    return json_str

def getImagePromptsTimed(script, captions_timed):
    end = captions_timed[-1][0][1]  # Get the end time of the last caption
    try:
        out = [[[0, 0], ""]]  # Initialize output
        while out[-1][0][1] != end:  # Loop until the end time matches
            content = call_OpenAI(script, captions_timed).replace("'", '\'')  # Call OpenAI and clean content
            try:
                out = json.loads(content)  # Try to parse JSON
            except json.JSONDecodeError as e:
                print("error on line 78")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~content: \n", content, "\n", "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("getImagePromptsTimed had an exception, namely:")
                print(e)
                print("trying to fix JSON")
                content = fix_json(content.replace("```json", "").replace("```", "")).strip()  # Fix JSON if parsing fails
                try:
                    out = json.loads(content)  # Try to parse fixed JSON
                    print("fixing JSON worked")
                except json.JSONDecodeError as e:
                    print("Failed to parse JSON after fixing: \n", content, "\n")
                    print("getImagePromptsTimed returned None because of an exception, namely:")
                    print(e)
                    return None  # Return None if parsing fails again
        print("content returned by getImagePromptsTimed is: ", content)
        return content  # Return the final content
    except Exception as e:
        print("out is: ", out)
        print("getImagePromptsTimed returned None because of an exception:")
        print(e)
        return None  # Return None if any other exception occurs

def call_OpenAI(script,captions_timed):
    user_content = """Script: {}
Timed Captions:{}
""".format(script,"".join(map(str,captions_timed)))
    print("user_content is: ", user_content)
    
    payload = {
        "model": model,
        "temperature": 0.9,
        "messages": [{"role": "system", "content": prompt},
                     {"role": "user", "content": user_content}]
    }
    
    response = requests.post("http://localhost:1337/v1/chat/completions", json=payload)
    #response_text = re.sub('\s+', ' ', response.text).strip()
    

     # Check if the request was successful
    if response.status_code == 200:
        try: 
            response_json = response.json()
            print("response text: ", response_json)
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, json.JSONDecodeError) as e:
            print("Unexpected response format or parsing error:", e)
            print("Response.text is: ", response.text)
            return None
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response:", response.text)
        return None

def merge_empty_intervals(segments):
    merged = []
    i = 0
    while i < len(segments):
        interval, url = segments[i]
        if url is None:
            # Find consecutive None intervals
            j = i + 1
            while j < len(segments) and segments[j][1] is None:
                j += 1
            
            # Merge consecutive None intervals with the previous valid URL
            if i > 0:
                prev_interval, prev_url = merged[-1]
                if prev_url is not None and prev_interval[1] == interval[0]:
                    merged[-1] = [[prev_interval[0], segments[j-1][0][1]], prev_url]
                else:
                    merged.append([interval, prev_url])
            else:
                merged.append([interval, None])
            
            i = j
        else:
            merged.append([interval, url])
            i += 1
    
    return merged
