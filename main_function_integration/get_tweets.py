def get_recent_tweets(search_term, time_period):

    import pandas as pd
    import json
    import tweepy
    import time
    import datetime

    ACCESS_TOKEN = '867046056-cvYtXPfzYSnftVl8wwExAc9LDm4XmF0CcOfJ7fZw'
    ACCESS_SECRET = 'MMLxDnE4dNO8BXQQ1RfelhJEi6n8S82H1DPXXeFlShQH7'
    CONSUMER_KEY = 'o2FVKVmYuOscIvDOgBoLwQdg2'
    CONSUMER_SECRET = 'jzbeDlSb5cJbfJEXERbR47JjaLpzC85u9nrquiMy4Ex7aFL9bD'

    # Setup tweepy to authenticate with Twitter credentials:

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Create the api to connect to twitter with your creadentials
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    # calculate start time of search (current time - time_period)

    current_time = pd.Timestamp.now(tz='UTC')
    start_time = current_time - datetime.timedelta(hours = time_period)


    # open file with records of prev searches

    search_params = pd.read_csv('search_param.txt',
                                infer_datetime_format = True,
                                parse_dates = ['start_time', 'end_time'])

    search_params.sort_values(by = 'end_time', ascending = False, inplace = True)
    search_params.index = range(len(search_params))

    # check if query in search_params, if start_time > START_TIME and start_time < END_TIME
    # if not, then search normally

    # if yes, load file and search with last_id
    query = search_term + ' -filter:retweets'
    found_flag = False
    end_id = 0

    i = 0
    while i < len(search_params):

        if ((search_params.loc[i]['query'] == query) &
            (search_params.loc[i]['start_time'] <= start_time) &
            (search_params.loc[i]['end_time'] > start_time)):

            found_flag = True
            end_id = search_params.loc[i]['end_id']
            filename = search_params.loc[i]['filename']

            print('Found existing data')
            i = 9999
        i += 1




    if found_flag:    
        json_tweets_old = pd.read_csv(filename,
                                      infer_datetime_format = True,
                                      parse_dates = ['datetime'])

    max_tweets = 20000
    query = search_term + ' -filter:retweets'

    searched_tweets = []
    last_searched_id = -1
    since_id = end_id

    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:

            new_tweets = api.search(q=query,
                                    count = count,
                                    max_id = str(last_searched_id - 1),
                                    since_id = since_id,
                                    tweet_mode = 'extended',
                                    since = str(start_time.date()),
                                    lang = 'es')


            if not new_tweets:
                
                break



            searched_tweets.extend(new_tweets)
            last_searched_id = new_tweets[-1].id

            if pd.to_datetime(new_tweets[-1]._json['created_at']) < start_time:
                print('Reached start time')
                break


        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break


    json_tweets = [i._json for i in searched_tweets]
    json_tweets_pd = pd.DataFrame(json_tweets)
    json_tweets_pd['datetime'] = pd.to_datetime(json_tweets_pd['created_at'])

    if found_flag:
        # append the old data below the new data

        json_tweets_pd = json_tweets_pd.append(json_tweets_old,  ignore_index = True, sort = True)



    # save data, update and save search params file

    time_start = json_tweets_pd['datetime'][len(json_tweets_pd)-1]
    time_end = json_tweets_pd['datetime'][0]

    end_id = json_tweets_pd['id'].max()
    filename = 'tweet_files/search_results_' + time_end.isoformat().replace(':','_') + '.txt'


    json_tweets_pd.to_csv(filename)


    last_ind = len(search_params)
    search_params.loc[last_ind] = [query, time_start, time_end, end_id, filename]

    search_params.to_csv('search_param.txt', index = False)
    
    return filename