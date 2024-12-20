
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utility.render.render_engine import get_output_media
if __name__ == "__main__":

    timed_generated_image_urls = [[['0', '5'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20bustling%20city%20with%20dinosaurs%20roaming%20freely%2C%20vibrant%20and%20lively%2C%20no%20text?width=1080&height=1920&seed=41438&nofeed=true&nologo=true&model=midjourney'], [['5', '10'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20T-Rex%20munching%20on%20a%20tree%20in%20a%20suburban%20neighborhood%2C%20playful%20and%20whimsical%2C%20no%20text?width=1080&height=1920&seed=30219&nofeed=true&nologo=true&model=midjourney'], [['10', '15'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20pterodactyls%20soaring%20overhead%20with%20gusts%20of%20wind%2C%20dynamic%20and%20colorful%2C%20no%20text?width=1080&height=1920&seed=40880&nofeed=true&nologo=true&model=midjourney'], [['15', '20'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20dino-proof%20buildings%20with%20high%20walls%20and%20reinforced%20structures%2C%20futuristic%20and%20sturdy%2C%20no%20text?width=1080&height=1920&seed=15739&nofeed=true&nologo=true&model=midjourney'], [['20', '25'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20humans%20riding%20on%20the%20backs%20of%20friendly%20herbivores%2C%20cheerful%20and%20adventurous%2C%20no%20text?width=1080&height=1920&seed=1993&nofeed=true&nologo=true&model=midjourney'], [['25', '30'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20giant%20dinosaur%20casting%20a%20shadow%20over%20a%20city%20street%2C%20dramatic%20and%20imposing%2C%20no%20text?width=1080&height=1920&seed=89546&nofeed=true&nologo=true&model=midjourney'], [['30', '35'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20scientists%20studying%20dinosaurs%20with%20equipment%20and%20notebooks%2C%20serious%20yet%20exciting%2C%20no%20text?width=1080&height=1920&seed=72613&nofeed=true&nologo=true&model=midjourney'], [['35', '40'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20vibrant%20dino-ecology%20lab%20filled%20with%20research%20and%20dino%20fossils%2C%20educational%20and%20intriguing%2C%20no%20text?width=1080&height=1920&seed=94651&nofeed=true&nologo=true&model=midjourney'], [['40', '45'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20food%20chain%20diagram%20featuring%20dinosaurs%20and%20humans%2C%20informative%20and%20engaging%2C%20no%20text?width=1080&height=1920&seed=31548&nofeed=true&nologo=true&model=midjourney'], [['45', '50'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20playful%20dino%20theme%20park%20with%20attractions%20and%20rides%2C%20fun%20and%20colorful%2C%20no%20text?width=1080&height=1920&seed=53359&nofeed=true&nologo=true&model=midjourney'], [['50', '55'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20serene%20forest%20with%20dinosaurs%20grazing%20peacefully%2C%20tranquil%20and%20lush%2C%20no%20text?width=1080&height=1920&seed=91025&nofeed=true&nologo=true&model=midjourney'], [['55', '60'], 'https://image.pollinations.ai/prompt/Cartoon%20style%2C%20a%20night%20scene%20with%20dinosaurs%20illuminated%20by%20city%20lights%2C%20magical%20and%20enchanting%2C%20no%20text?width=1080&height=1920&seed=70593&nofeed=true&nologo=true&model=midjourney']]
    audio_file_name = "audio_tts.wav"
    timed_captions = [((0, 0.48), 'What if'), ((0.48, 1.14), 'dinosaurs were'), ((1.14, 1.66), 'still alive?'), ((1.66, 3.24), 'Picture this,'), ((3.24, 3.92), 'a world where'), ((3.92, 4.76), 'dinosaurs roam'), ((4.76, 5.08), 'freely'), ((5.08, 5.92), 'alongside us,'), ((5.92, 6.52), 'their massive'), ((6.52, 7.32), 'shadows casting'), ((7.32, 7.86), 'over our'), ((7.86, 8.16), 'cities.'), ((8.16, 9.52), 'Imagine'), ((9.52, 9.94), 'stepping'), ((9.94, 10.6), 'outside your'), ((10.6, 11.12), 'door and'), ((11.12, 11.54), 'seeing a'), ((11.54, 12.32), 'T-Rex casually'), ((12.32, 12.84), 'munching on'), ((12.84, 13.62), 'a tree, while'), ((13.62, 14.48), 'pterodactyls'), ((14.48, 15.04), 'saw overhead,'), ((15.04, 15.58), 'their wings'), ((15.58, 16.44), 'creating gusts'), ((16.44, 16.9), 'of wind that'), ((16.9, 17.44), 'ruffle your'), ((17.44, 17.7), 'hair.'), ((17.7, 19.14), 'Our cities'), ((19.14, 19.52), 'would be'), ((19.52, 20.08), 'designed with'), ((20.08, 20.64), 'dino-proof'), ((20.64, 21.1), 'structures,'), ((21.1, 21.96), 'complete with'), ((21.96, 22.44), 'high walls'), ((22.44, 23.08), 'and reinforced'), ((23.08, 23.62), 'buildings.'), ((23.62, 25.42), 'Transportation'), ((25.42, 27.1), 'Forget cars,'), ((27.1, 27.6), 'we might'), ((27.6, 28.04), 'be riding'), ((28.04, 28.58), 'on the backs'), ((28.58, 29.14), 'of friendly'), ((29.14, 29.74), 'herbivores.'), ((29.74, 31.24), "But it wouldn't"), ((31.24, 31.82), 'be all fun'), ((31.82, 32.26), 'and games.'), ((32.26, 33.68), 'The food'), ((33.68, 34.2), 'chain would'), ((34.2, 34.58), 'be turned'), ((34.58, 35.3), 'upside down,'), ((35.3, 35.94), 'and humans'), ((35.94, 36.56), 'might find'), ((36.56, 37.26), 'themselves at'), ((37.26, 37.58), 'the bottom'), ((37.58, 38.16), 'of the menu'), ((38.16, 38.58), 'for some'), ((38.58, 38.88), 'of these'), ((38.88, 39.34), 'colossal'), ((39.34, 39.68), 'predators.'), ((39.68, 41.24), 'Scientists'), ((41.24, 41.7), 'would be'), ((41.7, 42.2), 'racing to'), ((42.2, 42.66), 'understand'), ((42.66, 43.26), 'these ancient'), ((43.26, 44.24), 'giants, leading'), ((44.24, 44.46), 'to'), ((44.46, 44.84), 'groundbreaking'), ((44.84, 45.92), 'discoveries and'), ((45.92, 46.6), 'perhaps even'), ((46.6, 47.14), 'a new field'), ((47.14, 47.64), 'of study,'), ((47.64, 48.52), 'dino ecology.'), ((48.52, 50.04), 'What do you'), ((50.04, 50.34), 'think?'), ((50.34, 51.56), 'Would you'), ((51.56, 52.06), 'dare to live'), ((52.06, 52.46), 'in a world'), ((52.46, 52.98), 'like this?'), ((52.98, 54.4), 'Comment your'), ((54.4, 54.96), 'idea for'), ((54.96, 55.3), 'the next'), ((55.3, 56.0), 'video below'), ((56.0, 56.52), 'and follow'), ((56.52, 56.88), 'for more'), ((56.88, 57.28), 'what if.')]
    topic = "What if dinosaurs were still alive"
    get_output_media(audio_file_name, timed_captions, timed_generated_image_urls, topic, "both")