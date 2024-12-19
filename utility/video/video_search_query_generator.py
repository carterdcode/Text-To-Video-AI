import json
import re
import requests
from g4f.client   import Client
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

log_directory = ".logs/gpt_logs"

prompt1 = """# Instructions
Given the following video script and timed captions, create 12 descriptive prompts to be used for image generation. Each prompt must be at maximum 120 characters.
The prompts should be related to the input. If a caption is vague or general, you may choose something similar or take context from surrounding words.
Ensure that the prompts are equally distributed throughout the video and are relevant to the content.

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

Here are some examples of good prompts:
'Long shot of an astronaut far away in a Martian landscape, under an otherworldly sky.' 
'Serene mountain lake at sunset, with snow-capped peaks reflected in crystal-clear water.'

IMPORTANT:
The output should be in JSON format, giving comma separated prompts:
["prompt 1 goes here", "prompt 2 goes here", ...]
Your response should be ONLY THE RESPONSE, no extra text or data. Remember you must create exactly 15 prompts each prompt is MAXIMUM 110 characters."""

prompt2 = """Using the following timed captions and list of prompts, please match each of the 12 of the prompts to the most relevant captions, and create suitable start and end times. Prompt start and end times do not have to exactly match the captions, the goal is to match the prompts to the captions as closely as possible and have 4-6 seconds between each prompt. 
It is vital that there is no time between the start and end times of the prompts, so if a prompt ends at 5 seconds, the next prompt should start at 5 seconds.

IMPORTANT:
The output should be in JSON format, giving a start time (s) and an end time (e) with one prompt (p):
[{"s":"starttimeinseconds","e":"endtimeinseconds","p":"prompt 1 goes here"},{"s":"starttimeinseconds.deciseconds","e":"endtimeinseconds.deciseconds","p":"prompt 2 goes here"},...]
Your response should be ONLY THE RESPONSE, no extra text or data. Remember you must match exactly 12 prompts to cover the entirety of the video. 
The final prompt should have an end timestamp that matches the final caption timestamp."""

def fix_json(json_str):
    print("Original JSON: ", json_str)
    json_str = json_str.strip()
   #remove ```json from the start of the string and ``` from the end of the string
    json_str = json_str.replace("```json", "").replace("```", "")
    # Replace typographical quotes with straight quotes
    json_str = json_str.replace("“", "\"").replace("”", "\"").replace("‘", "\"").replace("’", "\"")
    # Replace all " which has at least one letter directly before and after it with \'
    json_str = re.sub(r'(?<=[a-zA-Z])\"(?=[a-zA-Z])', "\'", json_str)
    # Ensure the JSON starts and ends with square brackets 
    if not json_str.startswith("["):
        json_str = "[" + json_str
    if not json_str.endswith("]"):
        json_str = json_str + "]"

    print("Fixed JSON String:", json_str)
    return json_str

def call_OpenAI(prompt, script,captions_timed):
    user_content = """Script: {}
Timed Captions:{}
""".format(script,"".join(map(str,captions_timed)))
    print("user_content is: ", user_content)

    payload = {
            "model": "gpt-4o",
            "temperature": 0.9,
            "messages": [{"role": "system", "content": prompt},
                         {"role": "user", "content": user_content}]
            }
    
    try: 
        response = requests.post("http://localhost:1337/v1/chat/completions", json=payload)
        #print("response is: ", response)
        #print("response.text is: ", response.text)
        message = response.json()["choices"][0]["message"]["content"]
    
    except Exception as e:  
        print("Error in response",e)
        return None
    


     # Check if the request was successful
    if response.status_code == 200:
        try: 
            print("CALL_OPENAI RETURNS response.choices[0].message.content WHICH IS:", message)
            return message
        except (KeyError, json.JSONDecodeError) as e:
            print("Unexpected response format or parsing error:", e)
            print("Response.text is: ", message)
            return None
    else:
        print("Request failed")
        return None
    

def getImagePromptsTimed(script, captions_timed):
    print("captions_timed is: ", captions_timed)
    print("script is: ", script)
    if captions_timed:
        content = call_OpenAI(prompt2, (call_OpenAI(prompt1,script, captions_timed).replace("'", '\'')), captions_timed).replace("'", '\'')
        # Get the end time of the last caption
        end_time = captions_timed[-1][0][1]
        print("end is: ", end_time)
    else:
        print("captions_timed is empty")
        return None
    try:
        out = [{"s": "0", "e": "0", "p": ""}] # Initialize the output with an empty prompt
        print("out initialised correctly")
        while float(out[-1]["e"]) < float(end_time):  # Loop until the last prompt ends at the end of the video
            try:
                out = json.loads(content)  # Try to parse JSON
                print("out structure: ", out)
                if len(out) > 1:
                    print("last prompt end time: ", out[-1]["e"])
                    return out
                else:
                    print("last prompt end time: ", out[0][0][1])
            except json.JSONDecodeError as e:
                print("error on json.loads(content)")
                print("getImagePromptsTimed had an exception ON LINE 158, namely:")
                print(e)
                print("trying to fix JSON")
                try:
                    content = fix_json(content.replace("```json", "").replace("```", "")).strip()  # Fix JSON if parsing fails
                    out = json.loads(content)  # Try to parse fixed JSON
                    print("fixing JSON worked")
                    print("returning out: ", out)
                    return out
                except json.JSONDecodeError as e:
                    print("Failed to parse JSON after fixing: \n", content, "\n")
                    print("getImagePromptsTimed returned None ON LINE 170, namely:")
                    print(e)
                    return None  # Return None if parsing fails again
        print("content returned by getImagePromptsTimed is: ", content)
        return out  # Return the final content
    except Exception as e:
        print("getImagePromptsTimed returned None because of an exception ON LINE 152, namely:")
        print(e)
        print("out is: ", out)
        return None  # Return None if any other exception occurs

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
