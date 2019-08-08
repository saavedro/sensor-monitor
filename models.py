from app import db

class Measurement(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "Measurement(sensor='{}', timestamp='{}', value='{}')".format(
                self.sensor, self.timestamp, self.value)
                
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
