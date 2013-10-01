from flask import current_app as APP

from ...extensions import db
from .api import TwitterAPI

from datetime import datetime

twitterAPI = TwitterAPI()

class Tweets(db.Document):
    user_ref = db.ReferenceField('User')
    max_id = db.IntField()
    min_id = db.IntField()
    last_update = db.DateTimeField(default=datetime.utcnow, required=True)
    tweets = db.SortedListField(db.ReferenceField('Tweet'))

    def get_old_tweets(self):
        APP.logger.info('fetching first tweets')
        tweets = twitterAPI.get_user_tweets(count=200)

        if tweets['error']:
            APP.logger.error('unable to fetch tweets')
            return

        self.min_id = tweets['data'][-1]['id']
        self.process_tweets(tweets['data'])

        while True:
            APP.logger.info('fetching tweets since')
            tweets = twitterAPI.get_user_tweets(count=200, max_id=self.min_id)
            if tweets['error']:
                APP.logger.error('unable to fetch tweets')
                break
            elif tweets['data'][-1]['id'] <= 50:
                APP.logger.info('no more tweets')
                self.process_tweets(tweets['data'])
                break

            APP.logger.info(len(tweets['data']))

            self.process_tweets(tweets['data'])


    def update_tweets(self):
        APP.logger.info('updating tweets')
        tweets = twitterAPI.get_user_tweets(count=200, since_id=self.max_id)

        if tweets['error']:
            APP.logger.error('unable to fetch tweets')
            return
        elif len(tweets['data']) == 0:
            APP.logger.info('no more tweets')
            return

        self.process_tweets(tweets['data'])

    def process_tweets(self, tweets):
        APP.logger.info('starting processing tweets')
        tweetRefs = []
        for tweet in tweets:
            tweet_id = str(tweet['id'])
            tweet.pop('id') #complains if you pass this into defaults
            tweet['user_ref'] = self.user_ref
            tweet = Tweet.objects.get_or_create(tweet_id = tweet_id, defaults=tweet)[0]
            tweetRefs.append(tweet.to_dbref())

        self.save()
        self.update(add_to_set__tweets=tweetRefs)

        self.max_id = Tweet.objects(user_ref=self.user_ref).order_by("-tweet_id").first()['tweet_id']
        self.min_id = Tweet.objects(user_ref=self.user_ref).order_by("tweet_id").first()['tweet_id'] 

        self.last_update = datetime.utcnow
        self.save()
        APP.logger.info('done processing tweets')


class Tweet(db.DynamicDocument):
    tweet_id = db.StringField(primary_key=True, required=True)
    user_ref = db.ReferenceField('User')

    meta = {
        'indexes': ['-tweet_id'],
        'ordering': ['-tweet_id']
    }