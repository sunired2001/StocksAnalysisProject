from textblob import TextBlob
import emoji
import tweepy
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from twitterkeys import CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET
import datetime

def twitterAuthenticate(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET):

    CONSUMER_KEY=CONSUMER_KEY
    CONSUMER_SECRET=CONSUMER_SECRET
    ACCESS_TOKEN=ACCESS_TOKEN
    ACCESS_TOKEN_SECRET=ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    return api;

#usernames = ["Benzinga","jimcramer","stockwits"]
#testing tweets
#usernames = ["ReformedBroker","awealthofcs","jasonzweigwsj","FANewsdesk"]

def give_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text


def get_all_tweets(screen_name,api):
    # Twitter only allows access to a users most recent 3240 tweets with   this method

    # authorize twitter, initialize tweepy
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []
    print("screen name", screen_name)
    # make initial request for most recent tweets (200 is the maximum   allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    count = 0
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        count += 1
    # new_tweets = api.user_timeline(screen_name = screen_name,count=30000)

    # save most recent tweets
    # alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one

    print("...%s tweets downloaded so far" % (len(alltweets)))

    stop_words = set(stopwords.words('english'))
    #keep stop words by removing from the list of stop words
    stop_words.remove('up')
    stop_words.remove('down')
    stop_words.remove('out')
    stop_words.remove('off')
    stop_words.remove('under')
    stop_words.remove('over')

    # transform the tweepy tweets into a 2D array

    outtweets = [[datetime.datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S').date(),
                 str.split(give_emoji_free_text(tweet.text.encode("utf-8")), 'https')[0]] for tweet in alltweets]

    #outtweets = [[tweet.created_at,
                  #str.split(give_emoji_free_text(tweet.text.encode("utf-8")), 'https')[0]] for tweet in alltweets]
    filteredlist = []
    #remove stop words
    for notweet in range(len(outtweets)):
        word_tokens = word_tokenize(str(outtweets[notweet][1]))
        filtered_sentence = [w for w in word_tokens if not w.upper() in [item.upper() for item in stop_words]]

        strf = ' '.join(filtered_sentence)
        filteredlist.append(strf)

    createddates = []
    tweets = []
    #replace tweet text with filtered stop words text
    for flist in range(len(filteredlist)):
        outtweets[flist][1] = filteredlist[flist]
    totaltweets = {}
    for flis in range(len(outtweets)):
        createddates.append(outtweets[flis][0])
        tweets.append(outtweets[flis][1])
    totaltweets["created_date"] = createddates
    totaltweets["tweets"] = tweets
    df = pd.DataFrame(totaltweets)

    calculatePolarities(df, screen_name)



def calculatePolarities(df, screen_name):
    dfcp = df.copy()

    tweetset = df["tweets"]
    polarit = []
    for tweet in tweetset:
        analysis = TextBlob(tweet)
        polarityval = analysis.sentiment.polarity
        # print("plo%d",polarityval)

        if (polarityval == 0):
            polarit.append("Neutral")
        elif (polarityval < 0):

            polarit.append("Negative")
        elif (polarityval > 0):

            polarit.append("Positive")

    dfcp["sentiment"] = polarit
    dfcp.to_csv('{0}_tweets.csv'.format(screen_name))

def tweetsOfGivenInvestor(investor):
    api=twitterAuthenticate(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    get_all_tweets(investor,api)
'''if __name__ == '__main__':
    api=twitterAuthenticate(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # pass in the username of the account you want to download
    usernames = ["Benzinga","jimcramer","stockwits","YahooFinance"]
    for x in usernames:
        get_all_tweets(x,api)'''
