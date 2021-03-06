import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    PROJECT = "hand_api"

    # Get app root path
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = True

    SECRET_KEY = 'this_is_so_secret' #used for development, reset in prod

    # MongoDB Config
    MONGODB_DB = 'hand_api'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'

class ProductionConfig(Config):

    DEBUG = False

    #MongoDB Info
    MONGODB_DB = 'app17531201'
    MONGODB_HOST = os.environ.get('MONGOHQ_URL')

class DevelopmentConfig(Config):

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