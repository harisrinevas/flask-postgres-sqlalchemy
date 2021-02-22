import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils.ingestion_scripts import *
# from utils.DBorm import PersonModel, ProjectModel, db_string
from sqlalchemy import create_engine
from utils.GlobalConfig import get_logger
import os
from utils.curd import Session, load_person, load_projects
from utils.DBorm import PersonModel, ProjectModel
import time

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
s = Session()


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
    """

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
    s.add(new_project)
    s.commit()
    return new_project


def query_project_data(request_id):
    projects = s.query(ProjectModel).get(request_id)
    results = [
        {
            "project_name": projects.project_name,
            "date_posted": projects.date_posted,
            "department": projects.department,
            "description": projects.description,
            "skills": projects.skills
        }]

    return results


def insert_person_data(data):
    new_person = PersonModel(first_name=data['first_name'],
                             last_name=data['last_name'],
                             email=data['email'],
                             address=data['address'],
                             skills=data['skills'])
    s.add(new_person)
    s.commit()
    return new_person


def query_person_data(request_id):
    person = s.query(PersonModel).get(request_id)

    results = [
        {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "email": person.email,
            "address": person.address,
            "skills": person.skills
        }]
    return results

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
        results = query_project_data(request_id)
        return {"count": len(results), "projects": results,  "message": "success"}


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

