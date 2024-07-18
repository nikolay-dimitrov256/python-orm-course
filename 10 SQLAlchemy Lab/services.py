from models import User
from main import Session

session = Session()

with session as session:
    user = User(username='mike', email='mike@johnson.com')
    session.add(user)
    session.commit()
