from app import db
import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class Measurement(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, **kwargs):
        if 'timestamp' in kwargs:
            # Convenience function that allows using "YYYY-MM-DD HH:MM:SS" strings
            if isinstance(kwargs['timestamp'], str):
                kwargs['timestamp'] = datetime.datetime.strptime(kwargs['timestamp'], DATETIME_FORMAT)
        return super().__init__(**kwargs)

    def __repr__(self):
        return "Measurement(sensor='{}', timestamp='{}', value='{}')".format(
                self.sensor, self.timestamp, self.value)
                
    def serialize(self):
        serial_me = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # change datetime into str of agreed format
        serial_me['timestamp'] =  serial_me['timestamp'].strftime(DATETIME_FORMAT)
        return serial_me
        
