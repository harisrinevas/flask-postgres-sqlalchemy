from sqlalchemy import create_engine
from .DBorm import PersonModel, ProjectModel
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import json


db_name = "database"
db_user = "username"
db_password = "secret"
db_host = "db"
db_port = "5432"
db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_password, db_host, db_port, db_name)
project_json = './data/projects.json'
person_json = './data/people.json'

engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def load_person():
    with session_scope() as s:
        for person in get_json(person_json):
            new_person = PersonModel(**person)
            s.add(new_person)


def load_projects():
    with session_scope() as s:
        for project in get_json(project_json):
            new_project = ProjectModel(**project)
            s.add(new_project)


def get_json(json_file):
    file_length = (len(open(json_file, 'r').readlines()))
    json_list =[]
    with open(json_file, 'r') as f:
        for i in range(file_length):
            text = f.readline()
            json_text = json.loads(text)
            json_list.append(json_text)
    return json_list
