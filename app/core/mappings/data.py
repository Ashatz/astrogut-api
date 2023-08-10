from ..events import *

def register_reporter(context, request, app_context, **kwargs) -> RegisterReporter:
    return RegisterReporter(request.json)