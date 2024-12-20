from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_timed_image_urls
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getImagePromptsTimed
import argparse
import utility.script.script_generator as script_generator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video from a template and topic. The templates are: facts, mens, travel")
    parser.add_argument("script_type", type=str, help="The template for the video")
    parser.add_argument("image_style", type=str, help="The style of images to generate")
    parser.add_argument("topic", type=str, help="The specific topic for the video")
    parser.add_argument("captions", type=str, help="Whether to render captions in the video, 'yes', 'no', or 'both'")
    # to run the script, use the following command:
    # python app.py --script_type whatif --image_style cartoon --topic "There was no such thing as crime"

    args = parser.parse_args()
    script_type = args.script_type
    style = args.image_style
    topic = args.topic
    captions = args.captions
    audio_file_name = "audio_tts.wav"

    response = script_generator.generate_script(script_type, topic)
    print("script: {}".format(response))

    asyncio.run(generate_audio(response, audio_file_name))

    timed_captions = generate_timed_captions(audio_file_name)
    print(timed_captions)

    timed_image_prompts = getImagePromptsTimed(response, timed_captions, style)
    timed_generated_image_urls = None
    if timed_image_prompts is not None:
        sorted(timed_image_prompts, key=lambda x: x['s'])
        print("sorted timed_image_prompts is: ", timed_image_prompts)
        timed_generated_image_urls = generate_timed_image_urls(timed_image_prompts, style)
        print("timed_generated_image_urls is:", timed_generated_image_urls)
        videos = get_output_media(audio_file_name, timed_captions, timed_generated_image_urls, topic.replace(" ", "").replace("?", ""), captions)
        print(videos)
    else:
        print("Error in timed_image_prompts, returned none")