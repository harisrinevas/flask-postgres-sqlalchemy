import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils.ingestion_scripts import *
# from utils.DBorm import PersonModel, ProjectModel, db_string
from sqlalchemy import create_engine
from utils.GlobalConfig import get_logger
import os

db_name = "database"
db_user = "username"
db_password = "secret"
db_host = "db"
db_port = "5432"
db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_password, db_host, db_port, db_name)
print(db_string)
logger = get_logger()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db_engine = create_engine(db_string)


def load_projects():
    json_file = './data/projects.json'
    file_length = (len(open(json_file, 'r').readlines()))
    with open(json_file, 'r') as f:
        for i in range(file_length):
            text = f.readline()
            json_text = json.loads(text)
            insert_project_data(json_text)


def load_person():
    json_file = './data/people.json'
    file_length = (len(open(json_file, 'r').readlines()))
    with open(json_file, 'r') as f:
        for i in range(file_length):
            text = f.readline()
            json_text = json.loads(text)
            insert_person_data(json_text)


def find_matching_person(skills_list):
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
        order by 2 desc
        limit 5
    """#.format(skills_list)

    # print("skill_list is: " + skills_list)

    result = db_engine.execute(query)
    result_set = []
    for r in result:
        result_set.append(r[0])
    result_list = get_person_list(result_set)
    return result_list


def get_person_list(id_list):
    person_list =[]
    for person_id in id_list:
        person_list.append(query_person_data(person_id))
    return person_list


def get_project_skills(project_id):
    query = 'select skills from project where id=' + str(project_id)
    result = db_engine.execute(query)
    result_set = []
    for r in result:
        if r != '':
            # skills_list = ','.join(str(skill) for skill in r)
            for record in r[0]:
                result_set.append(record)
    return result_set


def insert_project_data(data):
    new_project = ProjectModel(project_name=data['project_name'],
                               date_posted=data['date_posted'],
                               department=data['department'],
                               description=data['description'],
                               skills=data['skills'])
    db.session.add(new_project)
    db.session.commit()
    return new_project


def query_project_data(request_id):
    projects = ProjectModel.query.get(request_id)
    results = [
        {
            "project_name": projects.project_name,
            "date_posted": projects.date_posted,
            "department": projects.department,
            "description": projects.description,
            "skills": projects.skills
        }]

    # projects_all = ProjectModel.query.all()
    # results_all = [
    #     {
    #         "project_name": project_all.project_name,
    #         "date_posted": project_all.date_posted,
    #         "department": project_all.department,
    #         "description": project_all.description,
    #         "skills": project_all.skills,
    #         "id": project_all.id
    #     } for project_all in projects_all]
    return results


def insert_person_data(data):
    new_person = PersonModel(first_name=data['first_name'],
                             last_name=data['last_name'],
                             email=data['email'],
                             address=data['address'],
                             skills=data['skills'])
    db.session.add(new_person)
    db.session.commit()
    return new_person


def query_person_data(request_id):
    person = PersonModel.query.get(request_id)
    results = [
        {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "email": person.email,
            "address": person.address,
            "skills": person.skills
        }]
    return results


class PersonModel(db.Model):

    __tablename__ = "person"

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    address = db.Column(db.String())
    skills = db.Column(db.String())

    def __init__(self, first_name, last_name, email, address, skills):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.skills = skills

    def __repr__(self):
        return f"< Person {self.first_name}>"


class ProjectModel(db.Model):

    __tablename__ = "project"

    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String())
    date_posted = db.Column(db.String())
    department = db.Column(db.String())
    description = db.Column(db.String())
    skills = db.Column(db.String())

    def __init__(self, project_name, date_posted, department, description, skills):
        self.project_name = project_name
        self.date_posted = date_posted
        self.department = department
        self.description = description
        self.skills = skills

    def __repr__(self):
        return f"< Project {self.project_name}>"


@app.route('/')
def hello_world():
    return jsonify({"message": "hello world"})


@app.before_first_request
def ingest_data():
    if os.environ['LOAD_OPTION'] == "BULK_LOAD":
        load_projects()
        load_person()


@app.route('/person', methods=['GET', 'POST'])
def handle_person():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_person = insert_person_data(data)
            return {"message": f"{new_person.first_name} has been created successfully"}
        else:
            return {"error": "message not in JSON format"}

    elif request.method == 'GET':
        request_data = request.get_json()
        request_id = request_data['id']
        results = query_person_data(request_id)
        return {"count": len(results), "persons":results, "message": "success"}


@app.route('/project', methods=['GET', 'POST'])
def handle_project():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_project = insert_project_data(data)
            return {"message": f"{new_project.project_name}, {new_project.id} has been created successfully"}
        else:
            return {"error": "message not in JSON format"}

    elif request.method == 'GET':
        request_data = request.get_json()
        request_id = request_data['id']
        results, results_all = query_project_data(request_id)
        return {"count": len(results), "projects": results, "project_all": results_all, "message": "success"}


@app.route('/get_match', methods=['GET'])
def match_project_with_person():
    if request.method == 'GET':
        if request.is_json:
            data = request.get_json()
            project_id = data['id']
            skill_list = get_project_skills(project_id)
            matching_person = find_matching_person(skill_list)
            if matching_person == []:
                return {"message": "No suitable match for the project"}
            else:
                return {"message": matching_person}
        else:
            logger.info("the request received is not JSON")
            return {"error": "message not in JSON format"}
    else:
        return {"error": "Invalid request"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
