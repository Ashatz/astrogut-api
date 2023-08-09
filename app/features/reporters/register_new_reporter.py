from ...core import *
from ...domains import *

def handle(context: MessageContext):
    from datetime import datetime

    reporter = r.Reporter(context.data.to_primitive())

    # Verify that the reporter's date of birth is in the past.
    if reporter.birthday > datetime.now():
        raise AppError(context.errors.INVALID_REPORTER_BIRTHDAY.format_message(reporter.birthday))
    
    # Verify that the reporter's birth location contains valid coordinates.
    latitude = reporter.birth_location[0]
    longitude = reporter.birth_location[1]
    if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
        raise AppError(context.errors.INVALID_REPORTER_BIRTH_LOCATION.format_message(reporter.birth_location))
    
    reporter.created = int(datetime.utcnow().timestamp())
    reporter.last_updated = int(datetime.utcnow().timestamp()) 

    repo = context.services.reporter_repo()

    reporter = repo.add_reporter(reporter)

    return reporter