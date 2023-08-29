import csv
import json
import torch
import argparse
import transformers
import pandas as pd
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument("--device_id", type = int, default = 4)
parser.add_argument("--input_file", type = str, default = 'portmanteau.csv')
parser.add_argument("--output_file", type = str, default = 'portf1_output_alpaca.csv')
parser.add_argument("--model_path", type = str, default = "chavinlo/alpaca-native")

args = parser.parse_args()

model = transformers.AutoModelForCausalLM.from_pretrained(args.model_path, 
                                                            device_map = {"": torch.device(f"cuda:{args.device_id}")},
                                                            torch_dtype = torch.float16,
                                                            low_cpu_mem_usage=True)
tokenizer = transformers.AutoTokenizer.from_pretrained(args.model_path)

def get_input(input_file):
    df = pd.read_csv(input_file, header=None)
    return df

def main():

    input_words = get_input(args.input_file)
  
    for i in tqdm(range(500)):
        try:
            #prompt = f'Give the phonetic transcription of \'{input_words[0][i]}\' in IPA in American English'
            prompt = f"Instruction: Rhyme is a linguistic phenomenon characterized by the correspondence of sound between words or word terminations, which is especially noticeable when used at the end of lines in poetic compositions. It entails the repetition of similar auditory elements, frequently the same phonemes, found in the final emphasized syllables and any subsequent syllables of two or more words. Rhyme is characterized by a harmonious alignment of sound, with one word's auditory attributes harmonizing with another, creating a resonance that amplifies poetic expression. \n For example, Texit and exit rhyme with each other, so the answer is yes. But Texit and TexMex do not rhyme with each other, so the answer is No. \n Manny and Fanny rhyme with each other, so the answer is yes. But Manny and Manual do not rhyme with each other, so the answer is No.\n Input: Are {input_words[1][i]} and {input_words[2][i]} rhyming words ? Please answer Yes or No."
            inputs = tokenizer(prompt, return_tensors="pt")
            out = model.generate(inputs=inputs.input_ids.to(f"cuda:{args.device_id}"), max_new_tokens = 50, num_return_sequences=1, do_sample=True)
            output_texts = tokenizer.batch_decode(out, skip_special_tokens=True)
            print(output_texts)
            
            with open(args.output_file, 'a') as f:
                csvwriter = csv.writer(f)
                csvwriter.writerow([input_words[0][i], output_texts, input_words[2][i]])
        except:
            pass
            


    
if __name__ == '__main__':
    main()