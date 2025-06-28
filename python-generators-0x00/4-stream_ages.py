from seed import connect_to_prodev
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import User


def stream_user_ages():

    engine = connect_to_prodev()
    Session = sessionmaker(bind=engine)
    
  
    with Session() as session:    
        stmt = select(User.age)
        result = session.scalars(stmt)
        
        for age in result:
            yield age

def avg_user():
    ages = stream_user_ages()
    counter = 0
    avg = 0
    for age in ages:
        avg += age
        counter += 1

    print(f"Average age of users: {round(avg/counter, 2)}")



# for age in stream_user_ages():
#     print(age)


avg_user()
