import whisper_timestamped as whisper
from whisper_timestamped import load_model, transcribe_timestamped
import re

def generate_timed_captions(audio_filename, model_size="base"):
    # Load the Whisper model with the specified size
    WHISPER_MODEL = load_model(model_size)
   
    # Transcribe the audio file to get timestamped words
    gen = transcribe_timestamped(WHISPER_MODEL, audio_filename, verbose=False, fp16=False)
   
    # Generate captions with timestamps
    return getCaptionsWithTime(gen)

def splitWordsBySize(words, maxCaptionSize):
    # Split words into captions of a specified maximum size
    halfCaptionSize = maxCaptionSize / 2
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption + ' ' + words[0]) <= maxCaptionSize:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption) >= halfCaptionSize and words:
                break
        captions.append(caption)
    return captions

def getTimestampMapping(whisper_analysis):
    # Create a mapping from word positions to their timestamps
    index = 0
    locationToTimestamp = {}
    for segment in whisper_analysis['segments']:
        for word in segment['words']:
            newIndex = index + len(word['text']) + 1
            locationToTimestamp[(index, newIndex)] = word['end']
            index = newIndex
    return locationToTimestamp

def cleanWord(word):
    # Remove unwanted characters from a word
    return re.sub(r'[^\w\s\-_"\'\']', '', word)

def interpolateTimeFromDict(word_position, d):
    # Interpolate the timestamp for a given word position
    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return value
    return None

def getCaptionsWithTime(whisper_analysis, maxCaptionSize=40, considerPunctuation=True):
    # Generate captions with timestamps from the Whisper analysis
    wordLocationToTime = getTimestampMapping(whisper_analysis)
    position = 0
    start_time = 0
    CaptionsPairs = []
    text = whisper_analysis['text']
    
    if considerPunctuation:
        # Split text into sentences and then into words
        sentences = re.split(r'(?<=[.!?]) +', text)
        words = [word for sentence in sentences for word in splitWordsBySize(sentence.split(), maxCaptionSize)]
    else:
        # Split text into words and clean them
        words = text.split()
        words = [cleanWord(word) for word in splitWordsBySize(words, maxCaptionSize)]
    
    for word in words:
        position += len(word) + 1
        end_time = interpolateTimeFromDict(position, wordLocationToTime)
        if end_time and word:
            CaptionsPairs.append(((start_time, end_time), word))
            print(f"{start_time} - {end_time}: {word}")
            start_time = end_time

    return CaptionsPairs
