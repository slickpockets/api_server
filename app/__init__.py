import os

from flask import Flask
from config import config as Config
import redis

from dotenv import dotenv_values
hack_config = dotenv_values(".env")
basedir = os.path.abspath(os.path.dirname(__file__))

db = redis.StrictRedis(
    host=hack_config['REDISURL'],
    password=hack_config['REDISPASS'],
    port=hack_config['REDISPORT'],
    db=hack_config['REDISDB'],
    decode_responses=True
)

def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app.config.from_object(Config[config_name])

    Config[config_name].init_app(app)

    from .default import default as default_blueprint
    app.register_blueprint(default_blueprint)

    from .redis import main as redis_blueprint
    app.register_blueprint(redis_blueprint, url_prefix='/redis')



    return app
