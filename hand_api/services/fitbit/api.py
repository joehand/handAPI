from ..api_keys import Fitbit_Key
from ...extensions import oauth

class FitbitAPI():
    # Setup
    # ----------------------------
    oauth_app = oauth.remote_app(
        'fitbit',
        base_url='https://api.fitbit.com',
        request_token_url='http://api.fitbit.com/oauth/request_token',
        access_token_url='http://api.fitbit.com/oauth/access_token',
        authorize_url='http://www.fitbit.com/oauth/authorize',
        consumer_key=Fitbit_Key['key'],
        consumer_secret=Fitbit_Key['secret'],
    )
