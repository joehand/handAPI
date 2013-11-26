from ..api_keys import Github_Key
from ...extensions import oauth


class GitHubAPI():
    # Setup
    # ----------------------------
    oauth_type = 'oauth2'
    oauth_app = oauth.remote_app(
        'github',
        consumer_key=Github_Key['key'],
        consumer_secret=Github_Key['secret'],
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )