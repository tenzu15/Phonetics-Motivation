import csv
import json
import torch
import argparse
import transformers
import pandas as pd
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument("--device_id", type = int, default = 4)
parser.add_argument("--input_file", type = str, default = 'homophones.csv')
parser.add_argument("--output_file", type = str, default = 'homophone_output_alpaca.csv')
parser.add_argument("--model_path", type = str, default = "/home/asuvarna31/recover_weights_alpaca_7b")

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
  
    for i in tqdm(range(len(input_words))):
        try:
            #prompt = f'Give the phonetic transcription of \'{input_words[0][i]}\' in IPA in American English'
            prompt = f'Are {input_words[0][i]} and {input_words[1][i]} homophones ? Please answer Yes or No.'
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