import spotlight
import json
import tweepy
from clubfilehandler import ClubFileHandler

consumer_key = 'fanorpDFidIhsaLNzQFeSOCOG'
consumer_secret = 'i2ELm5Olc68yNFhIIZDNbeMEeqHB4coBde7PK2MELFbUgB6lU6'
access_token = '2887746393-2LkYKjiBCfo3uUaG34osy9YhM0BGCHHl7yPAc74'
access_token_secret = 'GL5szUVLnnFEIhOgEMNOLaBegNclSWmSfCU5ZZKjVGEZS'

annotations_host = 'http://model.dbpedia-spotlight.org/en/annotate'
candidates_host = 'http://model.dbpedia-spotlight.org/en/candidates'

confidence_level = 0.0
support_level = -1

filters = {
    'types': "DBPedia:SoccerPlayer,DBPedia:SoccerClub"
}

nicknames = {"Heart FC" : "Heart of Midlothian F.C",
             "Spurs" : " Tottenham Hotspurs F.C.",
             "West Ham" : "West Ham United F.C.",
             "Wigan" : "Wigan Athletic F.C.",
             "Paris" : "Paris Saint-Germain F.C."
           }


def get_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth


def get_annotations(text):
    try:
        return spotlight.annotate(annotations_host, text, confidence=-confidence_level,
                                  support=support_level, filters=filters)
    except spotlight.SpotlightException:
        return "No annotations found"


def get_candidates(text):
    try:
        return spotlight.candidates(candidates_host, text, confidence=confidence_level,
                                    support=support_level)
    except spotlight.SpotlightException as e:
        return "No candidates"


def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def get_tweets():
    x = 0
    list_of_tweets = []

    while x < no_of_tweets:
        if no_of_tweets - x > 100:
            list_of_tweets.extend(api.statuses_lookup(tweets_ids[x:99 + x]))
        else:
            list_of_tweets.extend(api.statuses_lookup(tweets_ids[x:no_of_tweets - 1]))
        x += 100

    return list_of_tweets


def format_tweet(tweet):
    txt = tweet.text
    txt = txt.split(' http')[0]
    txt = txt.replace('?', '.')
    txt = txt.encode('utf-8').decode('utf-8')
    return txt


api = tweepy.API(get_twitter_api())
tweets_ids = load_json_file('old_ids.json')
no_of_tweets = len(tweets_ids)
print(no_of_tweets)

tweets = get_tweets()
print(len(tweets))

fields = ['player', 'club']
handler = ClubFileHandler("player_club_uri.csv", fields)
writer = handler.get_csv_writer()
writer.writeheader()

no_of_valid_tweets = 0

for tweet in tweets:
    tweet_text = format_tweet(tweet)
    annotations = get_annotations(tweet_text)

    if "No annotations found" not in annotations:
        print(tweet_text)
        if len(annotations) > 1:
            if (" to " in tweet_text) or (" trials " in tweet_text):
                player = annotations[0]['URI'].encode('utf-8')
                club = annotations[1]['URI'].encode('utf-8')
            else:
                player = annotations[1]['URI'].encode('utf-8')
                club = annotations[0]['URI'].encode('utf-8')
            print(player)
            print(club)
            writer.writerow({'player': player, 'club': club})
            no_of_valid_tweets += 1
        else:
            print("Not enough annotations found")

print(no_of_valid_tweets)