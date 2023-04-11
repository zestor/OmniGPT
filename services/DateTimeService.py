from services.ServiceBase import ServiceBase
from datetime import datetime
import pytz
from pydantic import BaseModel

class DateTimeResponse(BaseModel):
    datetime: str

class DateTimeService(ServiceBase):
    def handle_request(self) -> DateTimeResponse:
        utc_timezone = pytz.UTC
        current_utc_datetime = datetime.now(utc_timezone)
        return DateTimeResponse(datetime=f"{current_utc_datetime}")

