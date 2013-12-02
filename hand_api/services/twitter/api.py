from ..api_keys import Twitter_Key
from ...extensions import oauth


class TwitterAPI():
    # Setup
    # ----------------------------
    oauth_type = 'oauth1'
    
    oauth_app = oauth.remote_app('twitter',
        base_url='https://api.twitter.com/1.1/',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
        consumer_key=Twitter_Key['key'],
        consumer_secret=Twitter_Key['secret'],
    )

    def get_user_tweets(self, count=20, max_id=None, since_id=None):
        data = dict(count=count, max_id=max_id, since_id=since_id)
        return self.api_request('statuses/user_timeline.json', **data)

    def get_user_profile(self, user_id):
        data = dict(user_id=user_id)
        return self.api_request('users/show.json', **data)

    def api_request(self, url, **kwargs):
        if kwargs:
            resp = self.oauth_app.request(url, data=kwargs)
        else:
            resp = self.oauth_app.request(url)
        if resp.status == 200:
            return dict(error=False, data=resp.data)
        else:
            return dict(error=True, status=resp.status, message=resp.data['errors'])

