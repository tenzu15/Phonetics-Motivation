import openai 
import os 
import argparse
import csv
import time
import config
import pandas as pd
from tqdm import tqdm

os.environ['OPENAI_KEY'] = config.gpt_4_key
openai.api_key = os.getenv('OPENAI_KEY')

parser = argparse.ArgumentParser(description='Get phonetic transcription from gpt in IPA')

parser.add_argument('--task', choices = ['phonemes', 'homophones', 'port'], default = 'port')
parser.add_argument('--gpt_version', choices=['text-davinci-003', 'gpt-3.5-turbo', 'gpt-4'], default='gpt-4')
parser.add_argument('--language', choices = ['english', 'hindi'], default = 'english')
parser.add_argument('--output', type = str, default = 'portf2_output_chatgpt.csv')

args = parser.parse_args()

def get_input(language):
    if language == 'english':
        df = pd.read_csv('portmanteau.csv', header=None)
    return df

def get_prompt_phoneme(task, word_1):
    if task == 'phoneme':
        prefix = 'Phonetic transcription is the use of phonetic symbols to represent speech sounds. Ideally, each sound in a spoken utterance is represented by a written phonetic symbol, so as to furnish a record sufficient to render possible the accurate reconstruction of the utterance. The International Phonetic Alphabet (IPA)  is a set of about a hundred alphabetic symbols (e.g. 1), a) together with a handful of non-alphabet symbols (e.g. the length mark :) and about thirty diacritics (e.g. those exemplified in S, d).'
        prompt = f'{prefix}\n\nGive the phonetic transcription of \'{word_1}\' in IPA in American English'
    return prompt
        
def get_prompt_rhyme(task, word_1):
    if task == 'rhymes':
        prefix = 'Rhyming words are words that have the same ending sound. In simpler terms, it can be defined as the repetition of similar sounds'
        prompt = f'{prefix}\n\nGive 5 words that rhyme with \'{word_1}\' '
    return prompt
    
def get_prompt_homophone(task, word_1, word_2):
    if task == 'homophones':
        prefix = 'In English, a homophone is a word that is pronounced exactly or nearly the same as another word but differs in meaning and is spelled differently. A homophone is a linguistic situation in which two words have the same pronunciation but have different spellings and meanings.'
        prompt = f'{prefix}\n\n  Are the words \'{word_1}\' and \'{word_2}\' homophones ? Please respond: \'Yes\' if they are homophones and \'No\' if they are not homophones.'
    return prompt

def get_prompt_port(task, word_1, word_2):
    if task == 'port':
        prefix = "Rhyme is a linguistic phenomenon characterized by the correspondence of sound between words or word terminations, which is especially noticeable when used at the end of lines in poetic compositions. It entails the repetition of similar auditory elements, frequently the same phonemes, found in the final emphasized syllables and any subsequent syllables of two or more words. Rhyme is characterized by a harmonious alignment of sound, with one word's auditory attributes harmonizing with another, creating a resonance that amplifies poetic expression. \n For example, Texit and exit rhyme with each other, so the answer is yes. But Texit and TexMex do not rhyme with each other, so the answer is No. \n Manny and Fanny rhyme with each other, so the answer is yes. But Manny and Manual do not rhyme with each other, so the answer is No."
        prompt = f'{prefix}\n\n  Are \'{word_1}\' and \'{word_2}\' rhyming words? Please respond: \'Yes\' if they are rhyming and \'No\' if they are not rhyming words.'
    return prompt
        
        
        

def main():
  
  df = get_input(args.language)
  count = 0
  
  for i in tqdm(range(500)): #range(len(df))
    loop_time = time.time()
    word_1 = df[1][i]
    word_2 = df[2][i]
    if args.task ==  'port':
        prompt = get_prompt_port(args.task, word_1, word_2)
    elif args.task == 'rhymes':
        prompt = get_prompt_rhyme(args.task, word_1)

    try:
        completion = openai.ChatCompletion.create(
                model=args.gpt_version, 
                messages = [
                {"role": "user", "content" : prompt}])

        poem = completion['choices'][0]['message']['content']
        print(poem)
            
        with open(args.output, 'a') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([prompt, poem, df[1][i]])
    except:
        print('Sleeping for error ....')
        time.sleep(40)
        count +=1
        
    if i % 50 == 0 and i != 0:
        print('Sleeping for time delay .....')
        time.sleep(40)


if __name__ == '__main__':
    main()
