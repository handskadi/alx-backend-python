from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from models import Base, User
import csv

def connect_db():
    try:
        engine = create_engine('mysql+pymysql://alx_user:alx_password@192.168.96.2:3306/ALX_prodev')
        print("connection successful") 
    except Exception as e:
        print(f"Error while connecting to database: {e}")  

    return engine        


def create_database(connection):
    try:
        engine, _ = connection
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev'")
            )
            
            if not result.fetchone():
                conn.execute(text("CREATE DATABASE ALX_prodev"))
                print("Database ALX_prodev created successfully")
            else:
                print("Database ALX_prodev is present")
                
    except Exception as e:
        print(f"Error creating database: {e}")
 



def connect_to_prodev(): 
    try:
        engine = create_engine('mysql+pymysql://alx_user:alx_password@192.168.96.2:3306/ALX_prodev')
        print("connection successful")
        return engine
    except Exception as e:
        print(f"Error while connecting to database: {e}")
        return None


def create_table(connection):
    try:
        Base.metadata.create_all(bind=connection)
        print("Table user_data created successfully")
    except Exception as e:
        print("Error while creating table")



def insert_data(connection, data):
    try:
        Session = sessionmaker(bind=connection)
        session = Session()

        with open(data, 'r') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                existing_user = session.query(User).filter_by(email=row['email']).first()
                
                if existing_user:
                    print(f"Skipping duplicate: {row['email']}")
                    continue     

                try:
                    new_user = User(
                        name=row['name'],
                        email=row['email'],
                        age=float(row['age'])
                    )
                    
                    session.add(new_user)
                    
                except ValueError as e:
                    print(f"Skipping row due to error: {e} - Row: {row}")
                    continue
            
            session.commit()
            print(f"Successfully inserted users records")
            
    except Exception as e:
        session.rollback()
        print(f"Error during data insertion: {e}")
    finally:
        session.close()
            




if __name__ == "__main__":
    engine = connect_to_prodev()
    if engine:
        create_table(engine)

    insert_data(engine, 'python-generators-0x00/user_data.csv')
