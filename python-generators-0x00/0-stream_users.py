from seed import connect_to_prodev
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import User

def stream_users():

    engine = connect_to_prodev()
    Session = sessionmaker(bind=engine)
    session = Session()

    with Session() as session:
        stmt = select(User)
        user_obj = session.scalars(stmt)
        for user in user_obj:  
            yield {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'age': user.age
            }



if __name__ == '__main__':
    from itertools import islice
    for user in islice(stream_users(), 6):
        print(user)



