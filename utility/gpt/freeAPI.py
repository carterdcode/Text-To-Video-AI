import os
import asyncio
import g4f 
from g4f import Client
import json

client = Client()
def generate_script_free(template, topic):
    facts_prompt = (
        """You are a seasoned content writer for a YouTube Shorts channel, specializing in facts videos. 
        Your fact shorts are concise, each lasting less than 50 seconds (approximately 140 words). 
        They are incredibly engaging and original. When a user requests a specific type of facts short, you will create it.

        For instance, if the user asks for:
        Weird facts
        You would produce content like this:

        Weird facts you don't know:
        - Bananas are berries, but strawberries aren't.
        - A single cloud can weigh over a million pounds.
        - There's a species of jellyfish that is biologically immortal.
        - Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.
        - The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.
        - Octopuses have three hearts and blue blood.

        You are now tasked with creating the best short script based on the user's requested type of 'facts'.

        Keep it brief, highly interesting, and unique.

        Stictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the script ..."}
        """
    )
    
    mens_motivation_prompt = (
        """You are a skilled content writer for a YouTube Shorts channel, specializing in creating concise and highly engaging scripts focused on men’s motivation. 
        Each script should last less than 50 seconds (approximately 140 words) and must inspire action, confidence, and growth. 
        Use bold, assertive language to connect with men striving to improve themselves in all aspects of life.  
        When a user requests a motivational topic, you will craft it to be relatable, impactful, and geared toward personal or professional growth.  

        For instance if the user asks for:  
        Discipline  
        You would produce content in a similar style to this:  

        Discipline:  
        - Motivation is temporary; discipline is what keeps you moving when the excitement fades.  
        - Every choice you make is a vote for the man you’re becoming—choose wisely.  
        - Small daily habits build the foundation of extraordinary success.  
        - You won’t always feel like it, but your future self will thank you for showing up anyway.  

        You are now tasked with creating the best short script based on the user’s motivational topic.  

        Strictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.  

        # Output  
        {"script": "Here is the script ..."}  
        """
    )

    travel_inspiration_prompt = (
        """You are a skilled content writer for a YouTube Shorts channel, specializing in creating concise and highly engaging scripts focused on travel inspiration. Each script should last less than 50 seconds (approximately 140 words) and must awaken the wanderlust of your audience. Highlight the magic of exploring new places, cultures, and experiences, while emphasizing practicality and motivation to travel.  

            When a user requests a travel topic, you will craft content that is adventurous, encouraging, and packed with value or fun facts.  

            For instance:  
            If the user asks for:  
            Hidden Destinations  
            You would produce content like this:  

            Hidden Destinations:  
            - Skip the tourist traps! Try Hallstatt, Austria—a charming lakeside village straight out of a fairytale.  
            - Ever heard of Chefchaouen, Morocco? It’s called the “Blue Pearl” for its stunning, blue-painted streets.  
            - In Canada, Fogo Island offers untouched nature and luxury stays—it’s a hidden gem waiting to be discovered.  
            - Japan’s Taketomi Island lets you experience traditional Ryukyu culture with no crowds.  

            You are now tasked with creating the best short script based on the user’s travel topic.  

            Strictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.  

            # Output  
            {"script": "Here is the script ..."}  
        """
    )
      
    if template == "facts":
        prompt = facts_prompt
    elif template == "mens":
        prompt = mens_motivation_prompt
    elif template == "travel":
        prompt = travel_inspiration_prompt
    else:
        prompt = facts_prompt

    prompt=prompt + "\n\n" + topic
    response = client(
        model="gpt-4o-mini",
        messages=[
        {
            "role": "user",
            "content": prompt         
            }
        ]

                )

    content = response['text']
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script