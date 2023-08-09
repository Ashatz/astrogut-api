from schematics import types as t, Model

class Reporter(Model):
    id = t.UUIDType(required=True, serialized_name='reporter_id')
    first_name = t.StringType(required=True)
    last_name = t.StringType(required=True)
    email = t.EmailType(required=True)
    birthday = t.DateTimeType(required=True)
    birth_location = t.GeoPointType(required=True)
    created = t.DateTimeType(required=True)
    last_updated = t.DateTimeType(required=True)