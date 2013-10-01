import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    PROJECT = "hand_api"

    # Get app root path
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False

    SECRET_KEY = 'this_is_so_secret' #used for development, reset in prod

    # Bootstrap Config (https://github.com/mbr/flask-bootstrap#configuration-options)
    BOOTSTRAP_USE_CDN = True
    
    # MongoDB Config
    MONGODB_DB = 'hand_api'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    #FitBit API Info
    FIT_KEY = '3188c43331f644b092666ae08a2243a1'
    FIT_SECRET = 'cb4a576caad444918fd98548b6589e0a'

    #Twitter API Info
    TWITTER_KEY = 'gQpFjjs1SBGmeNgzTv90zw'
    TWITTER_SECRET = 'oZrFSZl1QIuidwTFVAp4c4tNrLdA1xvtQ16ixaI'

    #Readmill API Info
    READMILL_KEY = 'f630c55f8035847b01f1a8bedde5f1cb'
    READMILL_SECRET = '287c32ddbf35cde5931e85603a7745ec'

    #GITHUB 
    GITHUB_KEY = '99222755646dcc27b4e0'
    GITHUB_SECRET = '7ce8de9cdf25b3d271b787b5b7a19ec7ad8fcb41'


class ProductionConfig(Config):

    #MongoDB Info
    MONGODB_DB = 'app17531201'
    MONGODB_HOST = os.environ.get('MONGOHQ_URL')

class DevelopmentConfig(Config):
    DEBUG = True

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PANELS = (
        'flask.ext.debugtoolbar.panels.versions.VersionDebugPanel',
        'flask.ext.debugtoolbar.panels.timer.TimerDebugPanel',
        'flask.ext.debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask.ext.debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask.ext.debugtoolbar.panels.template.TemplateDebugPanel',
        'flask.ext.debugtoolbar.panels.logger.LoggingPanel',
        'flask.ext.mongoengine.panels.MongoDebugPanel'
    )

class TestingConfig(Config):
    TESTING = True