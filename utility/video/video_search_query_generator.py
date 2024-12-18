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

prompt = """# Instructions

Given the following video script and timed captions, select a total of 12 time frames and create descriptive prompts to be used for image generation. 
The prompts should be related to the input. If a caption is vague or general, you may choose something similar, take context from surrounding words or discard it entirely. 
Ensure that the prompts for each timeframe you choose are strictly consecutive and cover the entire length of the video. 
Each prompt should cover between 6-10 seconds, you can amend the times so that they are consecutive. 
Please handle all edge cases, such as overlapping time segments and vague or general captions.
If the caption is 'Only 12 astronauts have walked on the Moon, all part of NASA's Apollo missions.', the prompt could be 'Long shot of an astronaut far away in a Martian landscape, under an otherworldly sky.' 

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

IMPORTANT:
The output should be in JSON format, giving a start time (s) and an end time (e) with one prompt (p):
[{"s":"starttimeinseconds","e":"endtimeinseconds","p":"prompt 1 goes here"},{"s":"starttimeinseconds","e":"endtimeinseconds","p":"prompt 2 goes here"},...]
Your response should be ONLY THE RESPONSE, no extra text or data. Remember you must create exactly 12 prompts for the entire video.
  """

def fix_json(json_str):
    print("Original JSON: ", json_str)
    json_str = json_str.strip()
   
    # Replace typographical quotes with straight quotes
    json_str = json_str.replace("“", "\"").replace("”", "\"").replace("‘", "\"").replace("’", "\"")
    #remove all { and } from the string
    json_str = json_str.replace("{", "").replace("}", "")
    # Replace all " which has at least one letter directly before and after it with \'
    json_str = re.sub(r'(?<=[a-zA-Z])\"(?=[a-zA-Z])', "\'", json_str)
    # Ensure the JSON starts and ends with square brackets 
    if not json_str.startswith("["):
        json_str = "[" + json_str
    if not json_str.endswith("]"):
        json_str = json_str + "]"

    print("Fixed JSON String:", json_str)
    return json_str

def call_OpenAI(script,captions_timed):
    user_content = """Script: {}
Timed Captions:{}
""".format(script,"".join(map(str,captions_timed)))
    print("user_content is: ", user_content)
    
    #TODO: Convert to client call instead of requests to allow retry
    #response = requests.post("http://localhost:1337/v1/chat/completions", json=payload)

    payload = {
            "model": "gpt-4o",
            "temperature": 0.9,
            "messages": [{"role": "system", "content": prompt},
                         {"role": "user", "content": user_content}]
            }
    
    try: 
        response = client.chat.completions.create(
    )
        response_message_content = response.choices[0].message.content  
        print("response is: ",response)
    
    except Exception as e:  
        print("Error in response",e)
        return None
    


     # Check if the request was successful
    if response_message_content is not None:
        try: 
            print("response msg content: ", response_message_content)
            #load the response text as a JSON object
            #response_json = json.loads(fix_json("["+response_message_content+"]"))
            print("CALL_OPENAI RETURNS response.choices[0].message.content WHICH IS:", response_message_content)
            return response_message_content
        except (KeyError, json.JSONDecodeError) as e:
            print("Unexpected response format or parsing error:", e)
            print("Response.text is: ", response_message_content)
            return None
    else:
        print("Request failed")
        return None
    

def getImagePromptsTimed(script, captions_timed):
    print("captions_timed is: ", captions_timed)
    print("script is: ", script)
    if captions_timed:
        # Get the end time of the last caption
        end_time = captions_timed[-1][0][1]
        print("end is: ", end_time)
    else:
        print("captions_timed is empty")
        return None
    try:
        out = [ [[0, 0], [""]], [[0, 0], [""]] ] # Initialize the output with an empty prompt
        while out[-1][0][1] < float(end_time):  # Loop until the last prompt ends at the end of the video
            #out[-1] = last element of out 
            #out[-1][0] = first element of last element of out (i.e [starttime, endtime] of the last prompt)
            #out[-1][0][1] = endtime of the last prompt
            content = call_OpenAI(script, captions_timed).replace("'", '\'')  # Call OpenAI and clean content
            try:
                out = json.loads(content)  # Try to parse JSON
                print("out structure: ", out)
                if len(out) > 1:
                    print("last prompt end time: ", out[-1][0][1])
            except json.JSONDecodeError as e:
                print("error on json.loads(content)")
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
        print("getImagePromptsTimed returned None because of an exception, namely:")
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
