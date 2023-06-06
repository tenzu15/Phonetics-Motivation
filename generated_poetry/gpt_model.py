import openai 
import os 
import json
import backoff
from tqdm import tqdm

os.environ['OPENAI_KEY'] = "open_ai_key"
gpt_version = 'gpt-3.5-turbo'
openai.api_key = os.getenv('OPENAI_KEY')

prompt_suffix_1 = "Write a short poem that has not been written by someone before on : "

animals = ["कोकिला", "गौरैया", "मैना","कबूतर", "तोता", "बाज़","शेर" ]
nature = ["नदी", "सागर", "पहाड़", "बगीचा", "झील", "जंगल"]
animals_eng = ["nightingale","sparrow","mynah","pigeon","parrot","falcon","lion" ]

nature_eng = ["meadow", "garden", "lake", "forest"]

popular_words = ["दिल", "दुख", "देखो", "बात", "प्यार", "इश्क", "सिर", "जीवन", "घर", "आज", "रात", "आँखें", "होंठ", "चेहरा", "बाल", "कलाई", "गाल", "गुलाब", "चमेली", "कमल"]
popular_words_eng = ["heart", "sorrow", "look", "talk", "love", "love", "head", "life", "home", "today", "night", "eyes", " lips", "face", "hair", "wrist", "cheek", "rose", "jasmine", "lotus"]

emotions = ['angry', 'scary', 'sad', 'happy']
rhyme = ['ABAB', 'ABABBCBC', 'AAAA', 'AA BB CC', 'ABBA', 'ABCB']

poems = []

for word in tqdm(popular_words[13:]) :
    for rhy in rhyme :
        f = open('chatgpt_poems_hindi', 'a')
        chatgpt_poem = {}
        question = f"{word} पर एक छोटी कविता लिखें {rhy} तुकबंदी योजना का उपयोग करते हुए"
        
        chatgpt_poem['prompt'] = question
        

        completion = openai.ChatCompletion.create(
                    model=gpt_version, 
                    messages = [
                    {"role": "user", "content" : question}]
                )
        output = completion['choices'][0]['message']['content']
        chatgpt_poem['poem'] = output
        f.write(str(chatgpt_poem))
        f.write('\n')
        poems.append(chatgpt_poem)
        

json.dump(poems, open('hindi_poems', 'w'))



    
