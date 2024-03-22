from os import getenv
from .models import DB, User, Tweet
import spacy
import not_tweepy as tweepy

API_KEY = getenv('TWITTER_API_KEY')
API_SECRET = getenv('TWITTER_API_SECRET')

TWITTER_AUTH = tweepy.OAuthHandler(API_KEY, API_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    """
    Gets twitter user and tweets from twitter DB
    Gets user by "username" parameter.
    """
    try:
        # gets back twitter user object
        twitter_user = TWITTER.get_user(username)
        # Either updates or adds user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, username=username)
        DB.session.add(db_user)  # Add user if don't exist

        # Grabbing tweets from "twitter_user"
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id
        )

        # check to see if the newest tweet in the DB is equal to the newest tweet from the Twitter API, if they're not equal then that means that the user has posted new tweets that we should add to our DB.
        if tweets[0].id != db_user.newest_tweet_id:
            db_user.newest_tweet_id = tweets[0].id

            # tweets is a list of tweet objects
            for tweet in tweets:
                # type(tweet) == object
                # Turn each tweet into a word embedding. (vectorization)
                tweet_vector = vectorize_tweet(tweet.full_text)
                db_tweet = Tweet(
                    id=tweet.id,
                    text=tweet.full_text,
                    vector=tweet_vector
                )
                db_user.tweets.append(db_tweet)
                DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        DB.session.commit()


nlp = spacy.load('my_model/')


def vectorize_tweet(text):
    return nlp(text).vector
