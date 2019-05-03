def sentiment(df,hashtag):
    
    from matplotlib.pyplot import figure
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
    import pandas as pd
    
    
    # for duplicate index error
    cols = ['datetime','sentiment']
    df = df[cols]
    df['datetime'] = pd.to_datetime(df.datetime)
    df = df.set_index('datetime')

    plt.figure(num=None, figsize=(10, 5), dpi=80, facecolor='w', edgecolor='k')
    plt.rcParams.update({'font.size': 13})

    avg_sent_per_day = df.sentiment.resample('h').mean()
    count_sent_per_day = df.sentiment.resample('h').count()
    avg_sent_per_day.plot(color = 'blue', grid=False)
    plt.xlabel('Hour');
    plt.title(hashtag)
    count_sent_per_day.plot(color='red',grid=False,secondary_y=True)
    plt.xlabel('Hour');

    red_patch = mpatches.Patch(color='red', label='Count')
    blue_patch = mpatches.Patch(color='blue', label='Sentiment')

    plt.legend(handles=[red_patch, blue_patch],loc=9,frameon=False);
    return plt