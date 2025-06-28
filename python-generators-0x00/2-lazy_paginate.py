from seed import connect_to_prodev
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, create_engine
from models import User


def paginate_users(page_size, offset):
    
    engine = connect_to_prodev()
    Session = sessionmaker(bind=engine)

    with Session() as session:
        # "SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        stmt = select(User).limit(page_size).offset(offset)
        return session.scalars(stmt).all()
    


def lazy_paginator(page_size):
    
    offset  = 0
    while True:
        page = paginate_users(page_size, offset)
        
        if not page:
            break

        for user in page:
            yield {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'age': user.age
            }
        offset += page_size



if __name__ == '__main__':
    for user in lazy_paginator(20):
        print(user)