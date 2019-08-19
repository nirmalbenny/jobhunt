import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
	SECRET_KEY = "1234567895"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG = True
	SIMPLEMDE_JS_IIFE = True
	SIMPLEMDE_USE_CDN = True

