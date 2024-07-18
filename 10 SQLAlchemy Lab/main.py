from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# '<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>'
CONNECTION_STRING = 'postgresql+psycopg2://postgres:admin@localhost:5432/sqlalchemy_lab'

engine = create_engine(CONNECTION_STRING)

Session = sessionmaker(bind=engine)