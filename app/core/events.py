from schematics import types as t, Model

class RegisterReporter(Model):
    first_name = t.StringType(required=True)
    last_name = t.StringType(required=True)
    email = t.EmailType(required=True)
    birthday = t.DateTimeType(required=True)
    birth_location = t.GeoPointType(required=True)