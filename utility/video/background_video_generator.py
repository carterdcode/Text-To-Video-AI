import os 
import requests
from utility.utils import log_response,LOG_TYPE_PEXEL
from g4f.client   import Client
from g4f.Provider import (
    PollinationsAI, # flux-pro
    Blackbox, # flux
    Blackbox2, # flux
    Airforce, # flux-pro
    Blackbox, # 4o
    DarkAI, #4o
    Liaobots, # 4o
    RetryProvider

)

img_client = Client(
    provider = RetryProvider([
        PollinationsAI, # flux-pro
        Blackbox, # flux
        Blackbox2, # flux
        Airforce, # flux-pro
    ], shuffle=True)
)

def generate_image(image_prompt):
    response = img_client.images.generate(
        model = "flux",
        width = 1080,
        height = 1920,
        prompt=image_prompt,
        response_format="url")
    try :
        image_url = response.data[0].url
    except Exception as e:
        print("Error in response",e)

    log_response(LOG_TYPE_PEXEL,image_prompt,response.json())
    
    return image_url

def generate_timed_image_urls(timed_video_prompts):
    timed_image_urls = []
    for item in timed_video_prompts:
        start_time = item['s']
        end_time= item['e']
        prompt = item['p']
        print("Currently generating: ", prompt)
        timed_image_urls.append([[start_time, end_time],generate_image(prompt)])
        print("timed_image_urls is: ", timed_image_urls)
    return timed_image_urls

import concurrent.futures

def generate_images(image_prompts):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_prompt = {executor.submit(generate_image, prompt): prompt for prompt in image_prompts}
        image_urls = {}
        for future in concurrent.futures.as_completed(future_to_prompt):
            prompt = future_to_prompt[future]
            try:
                print("Currently generating: ", prompt)
                image_urls[prompt] = future.result()
            except Exception as e:
                print(f"Error generating image for prompt {prompt}: {e}")
    return image_urls

def generate_timed_image_urls(timed_video_prompts):
    prompts = [item['p'] for item in timed_video_prompts]
    image_urls = generate_images(prompts)
    
    timed_image_urls = []
    for item in timed_video_prompts:
        start_time = item['s']
        end_time = item['e']
        prompt = item['p']
        timed_image_urls.append([[start_time, end_time], image_urls.get(prompt)])
        print("timed_image_urls is: ", timed_image_urls)
    return timed_image_urls
