from ..api_keys import Foursquare_Key
from ...extensions import oauth

class FoursquareAPI():
    # Setup
    # ----------------------------
    oauth_type = 'oauth2'
    api_version = 'v2' #Current 4sq API Version
    
    oauth_app = oauth.remote_app(
        'foursquare',
        base_url='https://api.foursquare.com',
        request_token_url=None,
        access_token_url='https://foursquare.com/oauth2/access_token',
        authorize_url='https://foursquare.com/oauth2/authenticate',
        consumer_key=Foursquare_Key['key'],
        consumer_secret=Foursquare_Key['secret'],
    )

    def change_header(uri, headers, body):
        print uri
        print headers
        print body

        return uri, headers, body

    oauth_app.pre_request = change_header