import os
# os.environ["MODIN_ENGINE"] = "ray"  # Modin will use Ray
# os.environ["MODIN_ENGINE"] = "ray"  # Modin will use Dask
# os.environ["MODIN_OUT_OF_CORE"] = "true"
import pandas as pd
import numpy as np 
import seaborn as sns
import spacy
import glob
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

nlp = spacy.load("de_core_news_sm")
input_type = 'json'

# to_inspect = [filename.split('/')[1].split('_')[0] for filename in glob.glob("25022021_0010/*.json")]

def inspect(directory_glob=f'25022021_0010/*.{input_type}'): 
    to_inspect = {}
    for i, file in enumerate(glob.glob(directory_glob)):
        shortened_filename = file.split('/')[1].split('_')[0]
        to_inspect[i] = [shortened_filename, file]
    return to_inspect

def prepare_dataframe(filepath, filetype):
    input_type = filetype
    global current_df
    if input_type == 'csv':
        current_df = pd.read_csv(filepath)
    elif input_type == 'json':
        current_df = pd.read_json(filepath)
    else:
        print('An error occurred..')
    # dataframe
    current_df['doc'] = [nlp(message_text) for message_text in current_df.message_text]
    current_df['entities'] = [doc.ents for doc in current_df.doc]
    current_df['lemmatized'] = [[[token.lemma_.lower() for token in entity if not token.is_punct and not token.is_stop] for entity in row] for row in current_df.entities]
    print('Preparation finished..')
    return current_df     

def tokens_sum(current_df):
    current_df['tokens_sum'] = [len(tokens) for tokens in current_df.doc]
    g = sns.distplot(current_df.tokens_sum)

# https://stackoverflow.com/questions/9372463/extracting-strings-from-nested-lists-in-python
def flatten(input_list):
    output_list = []
    for element in input_list:
        if type(element) == list:
            output_list.extend(flatten(element))
        else:
            output_list.append(element)
    return output_list

def convert_list_to_string(org_list, seperator=' '):
    return seperator.join(org_list)

def generate_wordcloud(current_df, fontpath='/home/pauld/.local/src/ttf-symbola/Symbola.ttf'):

    from collections import Counter
     
    to_cloud = [row for row in current_df.lemmatized]
    to_cloud_flattened = flatten(to_cloud)

    for item in to_cloud_flattened:
        item.encode()

    # Convert list of strings to string
    to_cloud_corpus = convert_list_to_string(to_cloud_flattened)

    # Encode strings as utf-8
    to_cloud_dict = Counter(to_cloud_flattened)

    # https://github.com/gearit/ttf-symbola.git
    font_path = fontpath
    wordcloud = WordCloud(font_path=font_path, width=1600, height=800).generate_from_frequencies(to_cloud_dict)
    
    plt.figure(figsize=(24,24), facecolor='k')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

def views_forwards_by_week(current_df):
    by_datetime = current_df[['message_date', 'message_views', 'message_forwards']]

    from datetime import datetime
    dates = []

    for row in by_datetime.iterrows():
        date = row[1]['message_date'].split(' ')[0]
        dates.append(datetime.strptime(date, "%Y-%m-%d"))
    

    by_datetime['date'] = dates

    by_week = []

    for row in by_datetime.iterrows():
        week = row[1]['date'].isocalendar()[:2]
        by_week.append(week)

    by_datetime['week'] = by_week

    by_datetime.groupby('week')[['message_views', 'message_forwards']].sum()

    by_datetime.groupby('week')[['message_views', 'message_forwards']].sum().plot(
    kind='bar',
    figsize=(24, 12)
    )

def full_df(directory):
    list_df = []
    for f in glob.glob(f'{directory}/*.csv'):
        df = pd.read_csv(f, encoding='utf-8')
        df['heritage'] = os.path.basename(f)
        list_df.append(df)

    full_df = pd.concat(list_df, ignore_index=True)
    return full_df


def posts_by_time_of_date(current_df):
    pass



