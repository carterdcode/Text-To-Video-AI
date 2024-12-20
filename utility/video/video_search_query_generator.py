import json
import re
import os
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
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
log_directory = ".logs/gpt_logs"

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

def getImagePromptsTimed(script, timed_captions, style):
    print("~~~~~~getImagePromptsTimed called with script: ~~~~~~~~", script, " ~~~~~AND TIMED_CAPTIONS:~~~~ ", timed_captions, " ~~~~STYLE: ~~~~~", style)
    with open(os.path.join(BASE_DIR, "image_prompts.json"), "r") as file:
            data = json.load(file)
            match_prompt = data.get("match_prompt", {}).get("prompt", "Prompt not found")
    if style == "cartoon":
        image_gen_prompt = data.get("cartoon_prompt", {}).get("prompt", "Prompt not found")
    elif style == "real":
        image_gen_prompt = data.get("real_prompt", {}).get("prompt", "Prompt not found")
    else:
        print("Invalid image style provided. Please provide a valid style: cartoon or real.")
        return None
    if not script:
        print("getImagePromptsTimed returned None because script is empty")
        return None
    if not timed_captions:
        print("getImagePromptsTimed returned None because timed_captions is empty")
        return None
    else:
        try:
            user_content = "#SCRIPT: " + script
            create_prompts_response = requests.post("http://localhost:1337/v1/chat/completions", json={
                "model": "gpt-4o","temperature": 0.9, "messages": [{"role": "system", "content": image_gen_prompt},
                                                                                          {"role": "user", "content": user_content}]})
            
            list_of_prompts = create_prompts_response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("getImagePromptsTimed returned None because of an exception, namely:")
            print(e)
            return None
        try:
            user_content ="#LIST OF PROMPTS: " + list_of_prompts + "#TIMED CAPTIONS: " + " ".join([caption[1] for caption in timed_captions])
            timed_prompts_response = requests.post("http://localhost:1337/v1/chat/completions", json={
                "model": "gpt-4o", "temperature": 0.9, "messages": [{"role": "system", "content": match_prompt},
                                                                                          {"role": "user", "content": user_content}]})
            timed_prompts = timed_prompts_response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("getImagePromptsTimed returned None because of an exception, namely:")
            print(e)
            return None
        
        end_time = timed_captions[-1][0][1]
        out = [{"s": "0", "e": "0", "p": ""}]
        while float(out[-1]["e"]) < float(end_time):  # Loop until the last prompt ends at the end of the video
            try:
                print("timed_prompts: ", timed_prompts)
                out = json.loads(timed_prompts)  # Try to parse JSON
                print("out structure: ", out)
                if len(out) > 1:
                    print("last prompt end time: ", out[-1]["e"])
                    return out
                else:
                    print("last prompt end time: ", out[0][0][1])
            except json.JSONDecodeError as e:
                print("error on json.loads(timed_prompts)")
                print("getImagePromptsTimed had an exception ON LINE 82, namely:")
                print(e)
                print("trying to fix JSON")
                try:
                    timed_prompts = fix_json(timed_prompts.replace("```json", "").replace("```", "")).strip()  # Fix JSON if parsing fails
                    out = json.loads(timed_prompts)  # Try to parse fixed JSON
                    print("fixing JSON worked")
                    print("returning out: ", out)
                    return out
                except json.JSONDecodeError as e:
                    print("Failed to parse JSON after fixing: \n", timed_prompts, "\n")
                    print("getImagePromptsTimed returned None ON LINE 95, namely:")
                    print(e)
                    return None  # Return None if parsing fails again
        print("content returned by getImagePromptsTimed is: ", timed_prompts)
        return out  # Return the final content

    

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
