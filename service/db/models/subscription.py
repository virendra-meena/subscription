from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configure custom logging format
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()

# Replace the placeholders with your actual values
host = 'localhost'
database_name = 'test_subscription_db'
user = 'root'
password = 'salesforce123'

# Create the SQLAlchemy engine with echo=True to enable logging
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database_name}', echo=True)
Base.metadata.create_all(engine)

class Subscription(Base):
    __tablename__ = 'subscription'

    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)
    status = Column(Enum('active', 'inactive'))


# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
