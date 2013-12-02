from ..api_keys import Readmill_Key
from ...extensions import oauth


class ReadmillAPI():
    # Setup
    # ----------------------------
    oauth_type = 'oauth2'

    oauth_app = oauth.remote_app('readmill',
        base_url='https://api.readmill.com/v2/',
        request_token_url=None,
        request_token_params={'scope':'non-expiring'},
        access_token_url='https://readmill.com/oauth/token',
        access_token_method='POST',
        authorize_url='https://readmill.com/oauth/authorize',
        consumer_key=Readmill_Key['key'],
        consumer_secret=Readmill_Key['secret']
    )

    # Readmill doesn't use standard Bearer header, change to OAuth
    def change_header(uri, headers, body):
        auth = headers.get('Authorization')
        if auth:
            auth = auth.replace('Bearer', 'OAuth')
            headers['Authorization'] = auth
        return uri, headers, body

    oauth_app.pre_request = change_header