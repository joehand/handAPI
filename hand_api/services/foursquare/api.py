from ..api_keys import Foursquare_Key
from ...extensions import oauth

class FoursquareAPI():
    # Setup
    # ----------------------------
    oauth_app = oauth.remote_app(
        'foursquare',
        base_url='https://api.foursquare.com/v2/',
        request_token_url=None,
        access_token_url='https://foursquare.com/oauth2/access_token',
        authorize_url='https://foursquare.com/oauth2/authenticate',
        consumer_key=Foursquare_Key['key'],
        consumer_secret=Foursquare_Key['secret'],
    )
