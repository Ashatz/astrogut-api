from schematics import types as t, Model

# Container configuration
class ContainerConfiguration(Model):
    astrology_api_url = t.StringType(required=True)


# Default container
class Container():
    
    def __init__(self, config: ContainerConfiguration):
        self.config = config