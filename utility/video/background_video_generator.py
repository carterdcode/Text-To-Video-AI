import os 
import requests
from utility.utils import log_response,LOG_TYPE_PEXEL
from g4f.client   import Client
from g4f.Provider import (
    PollinationsAI, # flux-pro
    Blackbox, # flux
    Blackbox2, # flux
    Airforce, # flux-pro
    RetryProvider
)

client = Client(
    image_provider = RetryProvider([
        PollinationsAI, # flux-pro
        Blackbox, # flux
        Blackbox2, # flux
        Airforce, # flux-pro
    ])
)

def generate_image(image_prompt):
    response = client.images.generate(
        model = "flux",
        prompt=image_prompt,
        response_format="url")
    try :
        image_url = response.data[0].url
        log_response(LOG_TYPE_PEXEL,image_prompt,response.json())
    except Exception as e:
        print("Error in response",e)

    log_response(LOG_TYPE_PEXEL,image_prompt,response.json())
    
    return image_url


def combine_images(image_prompts):
    image_urls = []
    for prompt in image_prompts:
        image_urls.append(generate_image(prompt))
    return image_urls
    

def generate_video_url(timed_video_prompts):
    print("timed_video_prompts:", timed_video_prompts)  # Debugging statement to print the input
    timed_image_urls = []
    used_links = []
    for item in timed_video_prompts:
        if not isinstance(item, list) or len(item) != 2:
            print(f"Skipping invalid item: {item}")
            continue
        (t1, t2), prompt_list = item
        if not isinstance(prompt_list, list):
            print(f"Skipping invalid prompt list: {prompt_list}")
            continue
        url = None
        for prompt in prompt_list:
            url = generate_image(prompt)
            if url:
                used_links.append(url.split('.hd')[0])
                break
        timed_image_urls.append([[t1, t2], url])
    return timed_image_urls
