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


def find_matching_person(db_engine, s, skills_list):
    skills_list = ','.join("'"+str(skill)+"'" for skill in skills_list)
    query = """
        select id, count(distinct matching_skill) as matches
        from (
            select id, matching_skill
            from person,
            lateral unnest(skills) matching_skill
            where matching_skill in (""" + skills_list + """) 
            ) s
        group by 1
        having count(distinct matching_skill) > 0
        order by 2 desc
        limit 5
    """

    result = db_engine.execute(query)
    result_set = []
    for r in result:
        result_set.append(r[0])
    result_list = get_person_list(s, result_set)
    return result_list


def get_person_list(s, id_list):
    person_list = []
    for person_id in id_list:
        person_list.append(query_person_data(s, person_id))
    return person_list


def get_project_skills(s, project_id):
    project = s.query(ProjectModel).get(project_id)
    if project is not None:
        return project.skills
    else:
        return None


def insert_project_data(s, data):
    new_project = ProjectModel(project_name=data['project_name'],
                               date_posted=data['date_posted'],
                               department=data['department'],
                               description=data['description'],
                               skills=data['skills'])
    s.add(new_project)
    s.commit()
    return new_project


def query_project_data(s, request_id):
    projects = s.query(ProjectModel).get(request_id)
    if projects is not None:
        results = [
            {
                "project_name": projects.project_name,
                "date_posted": projects.date_posted,
                "department": projects.department,
                "description": projects.description,
                "skills": projects.skills
            }]
        return results
    else:
        return None


def insert_person_data(s, data):
    new_person = PersonModel(first_name=data['first_name'],
                             last_name=data['last_name'],
                             email=data['email'],
                             address=data['address'],
                             skills=data['skills'])
    s.add(new_person)
    s.commit()
    return new_person


def query_person_data(s, request_id):
    person = s.query(PersonModel).get(request_id)
    if person is not None:
        results = [
            {
                "first_name": person.first_name,
                "last_name": person.last_name,
                "email": person.email,
                "address": person.address,
                "skills": person.skills
            }]
        return results
    else:
        return None
