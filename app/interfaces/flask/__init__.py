from functools import wraps

from flask import Flask

from ...core.constants import *
from ...core import *
from ...core.config import AppConfiguration

FLASK_APP_ERROR = 'errors'
FLASK_APP_MODULES = 'modules'
FLASK_APP_CONTAINER_CONFIG = 'container_config'
FLASK_APP_CONTAINER = 'container'

class FlaskAppContext(AppContext):

    _flask_app: Flask = None

    @property
    def flask_app(self):
        return self._flask_app

    def __init__(self, name: str, app_config: AppConfiguration, container_config: ContainerConfiguration, flask_app: Flask):
        self._flask_app = flask_app
        super().__init__(name, app_config, container_config)
        setattr(self._flask_app, FLASK_APP_ERROR, self.errors)
        setattr(self._flask_app, FLASK_APP_MODULES, self.modules)
        setattr(self._flask_app, FLASK_APP_CONTAINER_CONFIG, container_config)
        setattr(self._flask_app, FLASK_APP_CONTAINER, self.container)

    def run(self, **kwargs):
        self._flask_app.run(**kwargs)

class FlaskAppBuilder(AppBuilder):

    def build(self) -> FlaskAppContext:
        from flask import Flask
        from flask_cors import CORS

        from .error import register_error_handlers 
        from .routes import register_route_endpoints

        flask_app = Flask(__name__)    
        flask_app.config['SESSION_TYPE'] = 'filesystem'
        cors = CORS(flask_app)    

        register_error_handlers(flask_app)
        register_route_endpoints(flask_app)
        
        app_context = FlaskAppContext(
            self._current_session.name,
            self._current_session.app_config,
            self._current_session.container_config,
            flask_app)

        return app_context
    
def flask_api_message(func):
    @wraps(func)

    def wrapper(*args, **kwargs):
        import os
        from uuid import uuid4
        from flask import request, current_app

        try:
            message_id = str(uuid4())
            debug = os.environ.get(DEBUG, False)
            if debug == 'True':
                debug = True
            ip = request.environ['REMOTE_ADDR']
            module, feature = request.endpoint.split('.')
            routing_config = current_app.modules[module]['features'][feature]
            handler = FeatureHandler(routing_config)
            result = func(
                handler, 
                request, 
                current_app, 
                message_id=message_id, 
                ip=ip, 
                endpoint=request.endpoint, 
                debug=debug,
                **kwargs)
            return result
        except Exception as ex:
            raise ex

    return wrapper