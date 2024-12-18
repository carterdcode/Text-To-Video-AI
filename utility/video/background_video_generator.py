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
    ])
)

def generate_image(image_prompt):
    response = img_client.images.generate(
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
    image_prompts = []
    for [t1,t2], [prompt] in timed_video_prompts:
        # print the type of time_frame and prompt
        print("t1 is of type: ", type(t1), " t2 is of type: ", t2, " and prompt is of type: ", type(prompt))
        image_prompts.append(prompt)
    image_urls = combine_images(image_prompts)
    return image_urls

