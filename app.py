from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getImagePromptsTimed, merge_empty_intervals
import argparse
import utility.script.script_generator as script_generator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video from a template and topic. The templates are: facts, mens, travel")
    parser.add_argument("--template", type=str, help="The template for the video", default="facts")
    parser.add_argument("topic", type=str, help="The specific topic for the video")
    # to run the script, use the following command:
    # python app.py --template facts "The topic of the video"

    args = parser.parse_args()
    SAMPLE_TEMPLATE = args.template
    SAMPLE_TOPIC = args.topic
    SAMPLE_FILE_NAME = "audio_tts.wav"
    VIDEO_SERVER = "pexel"

    response = script_generator.generate_script(SAMPLE_TEMPLATE, SAMPLE_TOPIC)
    print("script: {}".format(response))

    asyncio.run(generate_audio(response, SAMPLE_FILE_NAME))

    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    print(timed_captions)

    print("CALLING getImagePromptsTimed USING script_generator.generate_script output: ", response)
    print("CALLING getImagePromptsTimed USING generate_timed_captions output: ", timed_captions)
    timed_video_prompts = getImagePromptsTimed(response, timed_captions)
    background_video_urls = None
    if timed_video_prompts is not None:
        background_video_urls = generate_video_url(timed_video_prompts)
        print(background_video_urls)
    else:
        print("No background video")
        

    merged_background_video_urls = merge_empty_intervals(background_video_urls)

    if merged_background_video_urls is not None:
        video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        print(video)
    else:
        print("No video")
