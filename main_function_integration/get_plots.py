def sentiment(df,hashtag):
    
    import matplotlib.pyplot as plt
    import pandas as pd


    df['datetime'] = pd.to_datetime(df.datetime)
    df = df.set_index('datetime')
    avg_sent_per_day = df.sentiment.resample('h').mean()
    count_sent_per_day = df.sentiment.resample('h').count()
    avg_sent_per_day.name = "Mean"
    count_sent_per_day.name = "Count"
    avg_sent_per_day.plot(color = 'blue', grid=False)
    plt.title(hashtag)
    plt.legend(loc='upper left')
    plt.xlabel('Hourly Change')
    count_sent_per_day.plot(color='red',grid=False,secondary_y=True)
    plt.legend(loc='upper right')
    return plt