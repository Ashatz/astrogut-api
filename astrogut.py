from app import *
from app.constants import *


def load_container_config(builder: FlaskAppBuilder): 
    import os, yaml

    from app.core import ContainerConfiguration
    env = os.getenv(APP_ENV, DEFAULT_APP_ENV)
    config_file = APP_CONFIGURATION_FILE
    if env != DEFAULT_APP_ENV:
        config_file = CONFIG_FILE_FORMAT.format(env)

    with open(CONFIG_FILE_DIRECTORY.format(config_file)) as stream:
        loaded_config = yaml.safe_load(stream)
    
    try:
        env_config = loaded_config[CONFIGS]
    except:
        raise AppError('No configuration exists for environment: {}'.format(env))
    
    kafka_producer = env_config.pop('kafka_producer')

    raw_data = {
        'madblad': env_config,
        'kafka_producer': kafka_producer,
        'aws': {
            'region_name': os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        }
    }
    container_config = ContainerConfiguration(raw_data)
    container_config.validate()
    builder.set_container_config(container_config)

builder = FlaskAppBuilder()
builder.create_new_app('astrogut-api')
load_container_config(builder)

app = builder.build()
flask_app = app.flask_app

if __name__ == '__main__':
    flask_app.run(threading=True)