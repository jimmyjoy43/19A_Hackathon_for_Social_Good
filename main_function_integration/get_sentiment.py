def score_sentiment(filename):

    import requests
    from IPython.display import HTML
    import json
    import pandas as pd
    import numpy as np
    import re
    import time
    import pathlib

    subscription_key = '4320911358854cea8cd264be0e85f3ef'
    assert subscription_key
    text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.1/"

    language_api_url = text_analytics_base_url + "languages"
    #print(language_api_url)

    sentiment_api_url = text_analytics_base_url + "sentiment"
   # print(sentiment_api_url)

    
    #function to return tweet language and sentiment score     
       
    def language_and_sentiment(df):

        #Language
        id_count = 0
        documents = {'documents': []}

        #compile language document
        for text in df['clean_text']:        
            documents['documents'].append({'id': '{}'.format(id_count), 'text': text})
            id_count += 1

        #feed compiled doc to API    
        headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
        response  = requests.post(language_api_url, headers=headers, json=documents)
        languages = response.json()

        new_lang_dict = {}
        for entry in languages['documents']:
            new_lang_dict[entry['id']] = entry['detectedLanguages'][0]['iso6391Name']


        langs = []
        for i in range(0,len(df)):
            if str(i) in new_lang_dict.keys():
                langs.append(new_lang_dict[str(i)])
            else:
                langs.append(np.nan)



        #append languages to df
        df['language'] = langs


        ## Sentiment
        id_count = 0
        documents = {'documents': []}

        #compile sentiment document
        for text in df['clean_text']:
            documents['documents'].append({'id': '{}'.format(id_count), 'language': langs[id_count],
                                           'text': text})
            id_count += 1

        #feed compiled sentiment doc to API
        headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
        response  = requests.post(sentiment_api_url, headers=headers, json=documents)
        sentiments = response.json()

        new_sent_dict = {}
        for entry in sentiments['documents']:
            new_sent_dict[entry['id']] = entry['score']


        sents = []

        for i in range(0,len(df)):
            if str(i) in new_sent_dict.keys():
                sents.append(new_sent_dict[str(i)])
            else:
                sents.append(np.nan)



        df['sentiment'] = sents

        return df
    
    #function to clean tweet text

    def clean_tweet(row):
        text = re.sub('Retweeted.*\):','',row['full_text'])
        text = re.sub('(http.*$)','',text)
        text = re.sub('(pic.twitter.*$)','',text)
        text = re.sub('([@#][\w_-]+)','',text)
        text = re.sub('([@] [^ ]+)','', text)
        text = re.sub('([#] [^ ]+)','', text)
        text = re.sub('[^\w]', ' ', text)
        text = re.sub('(['  '.*])', ' ', text)
        return text
    
    
    def chunker(seq, size):
        return (seq[pos:pos + size].copy() for pos in range(0, len(seq), size))

####### change it below #######
       
    tweets = pd.read_csv(filename,error_bad_lines=False)
   
   # binary indicator of whether the tweet was a retweet
   # tweets['retweet'] = tweets['text'].apply(lambda x: re.sub(r'Retweeted.*\):','',x))

    #clean tweet text
    tweets['clean_text'] = tweets.apply(clean_tweet, axis=1)
    tweets = tweets[tweets['clean_text'].str.contains('([a-zA-Z]+)', regex=True)]

    chunk_dfs = []

    for i in chunker(tweets,500):
        
        chunk_dfs.append(language_and_sentiment(i))
        time.sleep(5)

    tweets_with_sent = pd.concat(chunk_dfs)
    

    filename = filename.split('/')[1]
    filename = filename.split('.')[0]
    
    
    save_path = 'sentiment_csvs/'
    save_file = (save_path + str(filename) + 'sent.csv')

    tweets_with_sent.to_csv(save_file)
    return tweets_with_sent

