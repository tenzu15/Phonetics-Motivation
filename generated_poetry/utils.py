import pandas as pd 
import argparse
import re
#from rhymetagger import RhymeTagger

parser = argparse.ArgumentParser(description='Generate poems using chatgpt')

parser.add_argument('--input', type = str, default = None)

args = parser.parse_args()

def get_scores(file):
    fluency, grammar, rhythm, emotion,creativity =[], [], [], [], []
    df = pd.read_csv(file, header=None)
    temp_list = df[1].tolist()
    for temp in temp_list:
        scores = re.findall(r'\d+', temp)
        print(temp)
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

def get_rhyme_schemes(file, rt):
    df = pd.read_csv(file, header=None)
    rhyme, scheme = [], []
    for i in range(len(df)):
        #prompt = df[0][i].split('\n\n')[2]
        rhyme.append(df[0][i].split(' ')[-1]) #for poems dataset
        #rhyme.append(prompt.split(' ')[-1]) #for refined poems dataset
        #print(rhyme)
        poem = df[1][i].replace('\n\n', '\n').split('\n')
        scheme.append(rt.tag(poem, output_format=3))
        
    df['rhyme']= rhyme
    df['scheme'] = scheme
        
    return df 
        
    
    
def main():
    
    scored_df = get_scores(args.input)
    scored_df.to_csv('new_human_refined_score.csv', index=False)
    
    # rt = RhymeTagger()
    # rt.load_model(model='en')
    
    # rhy_df = get_rhyme_schemes(args.input, rt)
    # count = 0
    
    # for i in range(len(rhy_df)):
    #     rhy = rhy_df['rhyme'][i].replace('A', '1').replace('B', '2').replace('C','3')
    #     scheme = ''.join(str(x)for x in rhy_df['scheme'][i])
    #     if rhy == scheme[:4]:
    #         count+=1
            
    
    # rhy_df.to_csv('rhyme_eng_poems.csv', index=False)
        
    # print(count/len(rhy_df))
        
        
        
    
    
if __name__ == '__main__':
    main()