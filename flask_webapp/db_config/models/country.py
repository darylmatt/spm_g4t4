from app import db

class Country(db.Model):

    __tablename__ = 'country'

    country = db.Column(db.String(50), primary_key= True)


    def __init__(self,country):
       self.country = country
   
    def json(self):
        return self.country