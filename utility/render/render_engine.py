from datetime import datetime
import os
import tempfile
import zipfile
import platform
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.config import change_settings
from effects import zoom_in_out_effect
import requests

def download_file(url, filename):
    with open(filename, 'wb') as f:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        f.write(response.content)

def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

def get_output_media(audio_file_path, timed_captions, timed_generated_image_urls, topic, captions):
    print("timed_generated_image_urls is: ", timed_generated_image_urls)
    print("timed_captions is: ", timed_captions)
    image_clips = []
    for [[start_time, end_time], image_url] in timed_generated_image_urls:
        # Download the image file
        image_filename = tempfile.NamedTemporaryFile(delete=False).name
        download_file(image_url, image_filename)
        
        # Create imageFileClip from the downloaded file
        image_clip = ImageClip(image_filename)
        image_clip = image_clip.set_start(start_time)
        image_clip = image_clip.set_end(end_time)
        image_clip.duration = float(end_time) - float(start_time)
        image_clip = zoom_in_out_effect(image_clip)
        image_clips.append(image_clip)
    
    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)
    text_clips = []
    for ((start_time, end_time), text) in timed_captions:
        print("text is:", text)
        text_clip = TextClip(text, fontsize=80, color="white", stroke_width=5, stroke_color="black", method="caption").set_start(start_time).set_end(end_time).set_position(("center", "bottom"))
        text_clips.append(text_clip)
    video_no_captions = CompositeVideoClip(image_clips)
    if audio_clips:
        audio = CompositeAudioClip(audio_clips)
        video_no_captions.duration = audio.duration
        video_no_captions.audio = audio
    if text_clips:
        video_with_captions = CompositeVideoClip([video_no_captions] + text_clips)

    #set name to date and time.mp4

    captions_output_file_name = datetime.now().strftime(f"C_%d_%m_%y_%H_%M_{topic}.mp4")
    output_file_name = datetime.now().strftime(f"NC_%d_%m_%y_%H_%M_{topic}.mp4")
    if captions == "yes":
        print("writing video to filepath ", captions_output_file_name)
        video_with_captions.write_videofile(captions_output_file_name, codec='libx264', audio_codec='aac', fps=25, preset='veryfast')
    elif captions == "no":
        print("writing video to filepath ", output_file_name)
        video_no_captions.write_videofile(output_file_name, codec='libx264', audio_codec='aac', fps=25, preset='veryfast')
    elif captions == "both":
        print("writing video to filepath ", captions_output_file_name)
        video_with_captions.write_videofile(captions_output_file_name, codec='libx264', audio_codec='aac', fps=25, preset='veryfast', threads=4)
        print("writing video to filepath ", output_file_name)
        video_no_captions.write_videofile(output_file_name, codec='libx264', audio_codec='aac', fps=25, preset='veryfast', threads=4)

    
    # Clean up downloaded files
    for (start_time, end_time), image_url in timed_generated_image_urls:
        image_filename = tempfile.NamedTemporaryFile(delete=False).name
        os.remove(image_filename)

    return [output_file_name, captions_output_file_name] if captions == "both" else [output_file_name]
