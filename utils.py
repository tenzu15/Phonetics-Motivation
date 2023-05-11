import pandas as pd 
import argparse
import re

parser = argparse.ArgumentParser(description='Generate poems using chatgpt')

parser.add_argument('--input', type = str, default = None)

args = parser.parse_args()

def get_scores(file):
    fluency, grammar, rhythm, emotion,creativity =[], [], [], [], []
    df = pd.read_csv(file, header=None)
    temp_list = df[1].tolist()
    for temp in temp_list:
        scores = re.findall(r'\d+', temp)
        if len(scores)==5:i = 1
        else:i=2
        fluency.append(scores[0*i])
        creativity.append(scores[1*i])
        grammar.append(scores[2*i])
        emotion.append(scores[4*i])
        rhythm.append(scores[3*i])
    df['fluency'] = fluency
    df['emotion'] = emotion
    df['grammar'] = grammar
    df['rhythm'] = rhythm
    df['creativity'] = creativity
    
    return df
    
def main():
    
    scored_df = get_scores(args.input)
    scored_df.to_csv(args.input, index=False)
    
    
if __name__ == '__main__':
    main()