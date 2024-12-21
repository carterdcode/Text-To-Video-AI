
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utility.render.render_engine import get_output_media
if __name__ == "__main__":

    timed_generated_image_urls = [[['0', '5'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20teenage%20boy%20nervously%20talking%20to%20his%20step-sister%2C%20serious%20and%20timid%2C%20--no%20text?width=1080&height=1920&seed=22244&nofeed=true&nologo=true&model=midjourney'], [['5', '10'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20bedroom%20with%20a%20bouquet%20of%20flowers%2C%20romantic%20and%20playful%2C%20--no%20text?width=1080&height=1920&seed=13339&nofeed=true&nologo=true&model=midjourney'], [['10', '15'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20teenaged%20step-sister%20looking%20surprised%2C%20confused%2C%20and%20aroused%2C%20sitting%20on%20a%20bed%2C%20--no%20text?width=1080&height=1920&seed=70563&nofeed=true&nologo=true&model=midjourney'], [['15', '20'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20blushing%20teenage%20boy%20holding%20a%20box%20of%20condoms%2C%20awkward%20and%20nervous%2C%20--no%20text?width=1080&height=1920&seed=8698&nofeed=true&nologo=true&model=midjourney'], [['20', '25'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20tense%20exchange%20between%20a%20boy%20and%20girl%20about%20protection%2C%20serious%20and%20passionate%2C%20--no%20text?width=1080&height=1920&seed=18626&nofeed=true&nologo=true&model=midjourney'], [['25', '30'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20the%20boy%20left%20alone%20in%20a%20bedroom%2C%20devastated%20and%20thoughtful%2C%20--no%20text?width=1080&height=1920&seed=8203&nofeed=true&nologo=true&model=midjourney'], [['30', '35'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20young%20couple%20in%20PJs%20on%20a%20couch%2C%20intimate%20and%20comfortable%2C%20--no%20text?width=1080&height=1920&seed=97242&nofeed=true&nologo=true&model=midjourney'], [['35', '40'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20boy%20planning%20the%20event%2C%20focused%20and%20excited%2C%20writing%20details%20on%20a%20notebook%2C%20--no%20text?width=1080&height=1920&seed=11468&nofeed=true&nologo=true&model=midjourney'], [['40', '45'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20an%20empty%20room%20after%20failed%20tryst%2C%20the%20boy%20alone%20and%20disheartened%2C%20--no%20text?width=1080&height=1920&seed=98266&nofeed=true&nologo=true&model=midjourney'], [['45', '50'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20regretful%20teenage%20boy%20laying%20in%20bed%2C%20pensive%20and%20dejected%2C%20--no%20text?width=1080&height=1920&seed=93284&nofeed=true&nologo=true&model=midjourney'], [['50', '55'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20the%20aftermath%20of%20a%20ruined%20carpet%2C%20tattered%20and%20messy%2C%20--no%20text?width=1080&height=1920&seed=12353&nofeed=true&nologo=true&model=midjourney'], [['55', '60'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20teenage%20step-siblings%20on%20a%20video%20call%2C%20smiling%20and%20laughing%2C%20--no%20text?width=1080&height=1920&seed=87766&nofeed=true&nologo=true&model=midjourney']]
    audio_file_name = "audio_tts.wav"
    timed_captions = [((0, 1.22), 'My parents got divorced'), ((1.22, 2.44), 'a few years back, but'), ((2.44, 3.5), 'remained on good terms'), ((3.5, 5.22), 'and even decided to cohabitate'), ((5.22, 6.28), 'for some time for the'), ((6.28, 7.24), 'ease of my two younger'), ((7.24, 7.62), 'sisters.'), ((7.62, 9.76), "That's how I ended up"), ((9.76, 11.04), 'living with my step-sister,'), ((11.04, 12.86), 'a tall, blonde, and absolutely'), ((12.86, 14.22), 'dreamy 16-year-old.'), ((14.22, 16.42), 'Amidst my teenage hormones'), ((16.42, 17.76), 'and urges for experiencing'), ((17.76, 18.94), 'everything life has to'), ((18.94, 20.02), 'offer, I thought it would'), ((20.02, 21.24), 'be the perfect opportunity'), ((21.24, 22.28), 'to act on my deepest'), ((22.28, 22.72), 'desires.'), ((22.72, 25.0), 'I had always nurtured'), ((25.0, 26.04), 'warm feelings for her'), ((26.04, 27.0), "and felt she'd be the"), ((27.0, 28.22), 'perfect person to take'), ((28.22, 29.32), 'that virginity late with,'), ((29.32, 30.36), 'being the rational and'), ((30.36, 31.7), 'mature individual I thought'), ((31.7, 32.12), 'I was.'), ((32.12, 34.22), 'One warm summer evening,'), ((34.22, 35.46), 'my parents had gone out'), ((35.46, 36.78), 'for a movie night, leaving'), ((36.78, 38.12), 'us at home with an instruction'), ((38.12, 39.42), 'to not exceed our bedtime.'), ((39.42, 41.48), 'With the entire house'), ((41.48, 42.84), 'seemingly empty, I seized'), ((42.84, 43.76), 'the moment to strike'), ((43.76, 44.92), 'up a conversation with'), ((44.92, 45.7), 'my step-sister.'), ((45.7, 47.84), 'We started talking about'), ((47.84, 49.0), 'her friends, her interest'), ((49.0, 50.44), 'in photography, and eventually'), ((50.44, 51.46), 'slipped into the topic'), ((51.46, 52.26), 'of her virginity.'), ((52.26, 54.34), 'Sensing an opening, I'), ((54.34, 55.58), 'boldly shared my interest'), ((55.58, 56.62), 'in being the first one'), ((56.62, 57.76), 'to rob her of that honor.'), ((57.76, 59.88), 'Much to my bewilderment'), ((59.88, 61.12), 'and despair, she eagerly'), ((61.12, 62.36), 'agreed in exchange for'), ((62.36, 63.34), 'a promise to take good'), ((63.34, 64.26), 'care of her afterward.'), ((64.26, 66.26), 'With excitement rushing'), ((66.26, 67.68), 'through my veins, I planned'), ((67.68, 68.64), 'our trist to the very'), ((68.64, 69.84), 'last detail, worrying'), ((69.84, 71.08), 'only about whether Id'), ((71.08, 72.18), 'last long enough to please'), ((72.18, 72.42), 'her.'), ((72.42, 74.36), 'As the pre-plan date'), ((74.36, 75.54), 'arrived, everything was'), ((75.54, 76.74), 'set for a cozy Netflix'), ((76.74, 77.48), 'and chill night.'), ((77.48, 79.74), 'She seemed nervous, but'), ((79.74, 80.82), 'excited as we changed'), ((80.82, 82.5), 'into our respective PJs.'), ((82.5, 84.32), 'When things were about'), ((84.32, 85.88), 'to get real, she sheepishly'), ((85.88, 86.86), 'asked me if we needed'), ((86.86, 87.94), 'to use any protection,'), ((87.94, 89.36), 'realizing why I had been'), ((89.36, 90.6), 'buying so many condoms'), ((90.6, 90.9), 'lately.'), ((90.9, 93.08), 'My face turned big red,'), ((93.08, 94.16), 'and I felt a sinking'), ((94.16, 95.14), 'feeling in the pit of'), ((95.14, 95.58), 'my stomach.'), ((95.58, 97.66), 'The entire carefully'), ((97.66, 98.92), 'constructed plan quickly'), ((98.92, 100.02), 'unraveled like a cheap'), ((100.02, 101.14), 'carpet, as it dawned'), ((101.14, 102.12), 'on her how little I had'), ((102.12, 103.16), 'considered the emotional'), ((103.16, 104.34), 'and physical implications'), ((104.34, 105.5), 'of what I was proposing.'), ((105.5, 107.56), 'Wanting to say face,'), ((107.56, 108.88), 'I quickly downplayed'), ((108.88, 109.96), 'the issue and clumsily'), ((109.96, 111.14), 'joked about the situation,'), ((111.14, 112.32), 'but her mind was made'), ((112.32, 112.54), 'up.'), ((112.54, 114.54), 'She decided she could'), ((114.54, 115.66), 'no longer partake in'), ((115.66, 116.56), 'the event and refuse'), ((116.56, 117.54), 'to stay in the room.'), ((117.54, 119.78), 'Devastated, I was left'), ((119.78, 120.8), 'alone to grapple with'), ((120.8, 121.9), 'the consequences of my'), ((121.9, 123.32), 'reckless fantasy, realizing'), ((123.32, 124.3), 'that I may have crossed'), ((124.3, 125.28), 'the line much further'), ((125.28, 126.4), 'than I had ever imagined.'), ((126.4, 129.14), 'Hashtag Tifu when I foolishly'), ((129.14, 130.52), 'underestimated the complexity'), ((130.52, 131.52), 'of human connections'), ((131.52, 133.08), 'and relationships, resulting'), ((133.08, 134.4), 'in a regrettable situation'), ((134.4, 135.7), 'that put my step-sisters'), ((135.7, 136.64), 'emotional well-being'), ((136.64, 138.26), 'at risk, ultimately betraying'), ((138.26, 139.32), 'the trust placed in me.')]
    topic = "What if animals could speak"
    get_output_media(audio_file_name, timed_captions, timed_generated_image_urls, topic, "no")