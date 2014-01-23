from flask.ext.security import current_user

from ..api_keys import Fitbit_Key
from ...extensions import oauth

class FitbitAPI():
    # Setup
    # ----------------------------

    oauth_type = 'oauth1'
    api_version = '1' #Current FitBit API Version

    oauth_app = oauth.remote_app(
        'fitbit',
        base_url='https://api.fitbit.com',
        request_token_url='http://api.fitbit.com/oauth/request_token',
        access_token_url='http://api.fitbit.com/oauth/access_token',
        authorize_url='http://www.fitbit.com/oauth/authorize',
        consumer_key=Fitbit_Key['key'],
        consumer_secret=Fitbit_Key['secret'],
    )

    def change_header(uri, headers, body):
        oauth_token = current_user.get('services')['fitbit']['oauth_token_secret']

        auth = headers.get('Authorization')
        if auth:
            print auth
            auth = auth + ', oauth_token="%s"' %oauth_token
            headers['Authorization'] = auth
        
        print uri
        print headers
        print body

        return uri, headers, body

    oauth_app.pre_request = change_header