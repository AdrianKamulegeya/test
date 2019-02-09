import tweepy
from clubfilehandler import ClubFileHandler


consumer_key = 'fanorpDFidIhsaLNzQFeSOCOG'
consumer_secret = 'i2ELm5Olc68yNFhIIZDNbeMEeqHB4coBde7PK2MELFbUgB6lU6'
access_token = '2887746393-2LkYKjiBCfo3uUaG34osy9YhM0BGCHHl7yPAc74'
access_token_secret = 'GL5szUVLnnFEIhOgEMNOLaBegNclSWmSfCU5ZZKjVGEZS'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user('TMrumours')

all_tweets = []

tweets = api.user_timeline(user.id, count=200)
all_tweets.extend(tweets) #saves 200 most recent tweets


oldest = all_tweets[-1].id - 1 #gets last tweet id from this call


while len(tweets) > 0:
    print "getting tweets before %s" % (oldest)

    # all subsiquent requests use the max_id param to prevent duplicates
    tweets = api.user_timeline(id=user.id, count=200, max_id=oldest)

    # save most recent tweets
    all_tweets.extend(tweets)

    # update the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1

    print "oldest ID now is... %s" % (oldest)

    print "...%s tweets downloaded so far" % (len(all_tweets))

print len(all_tweets)

fields = ['player', 'rumuoured_club']

handler = ClubFileHandler("transfer_rumours.csv", fields)
writer = handler.get_csv_writer()
writer.writeheader()

for tweet in all_tweets:
    try:
        text = tweet.text
        text = text.split(' http')[0]
        text = text.replace('?', '')
        text = text.encode('utf-8')
        print text

        if "interested" in text:
            data = text.split(' interested in ')
            club = data[0]
            player = data[1]
        elif "observing" in text:
            data = text.split(' observing ')
            club = data[0]
            player = data[1]
        elif " to " in text:
            data = text.split(' to ')
            player = data[0]
            club = data[1]

        writer.writerow({'player': player, 'rumuoured_club': club})
    except Exception as e:
        print tweet.text + " ---------- DIDNT WORK ----------"
        print (e)
    #print tweet.text



