import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils.ingestion_scripts import *
from sqlalchemy import create_engine
from utils.GlobalConfig import get_logger
import os
from utils.curd import *
import time


logger = get_logger()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db_engine = create_engine(db_string)
s = Session()

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
            new_person = insert_person_data(s, data)
            return {"id": new_person.id,
                    "message": f"{new_person.first_name} has been created successfully"}
        else:
            return {"error": "message not in JSON format"}

    elif request.method == 'GET':
        request_data = request.get_json()
        request_id = request_data['id']
        results = query_person_data(s, request_id)
        if results is not None:
            return {"count": len(results), "persons":results, "message": "success"}
        else:
            return {"message": "No matching person found"}


@app.route('/project', methods=['GET', 'POST'])
def handle_project():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_project = insert_project_data(s, data)
            return {"id": new_project.id,
                    "message": f"{new_project.project_name} has been created successfully"}
        else:
            return {"error": "message not in JSON format"}

    elif request.method == 'GET':
        request_data = request.get_json()
        request_id = request_data['id']
        results = query_project_data(s, request_id)
        if results is not None:
            return {"count": len(results), "projects": results,  "message": "success"}
        else:
            return {"message": "No matching project"}


@app.route('/get_match', methods=['GET'])
def match_project_with_person():
    if request.method == 'GET':
        if request.is_json:
            data = request.get_json()
            project_id = data['id']
            matching_person=[]
            skill_list = get_project_skills( s, project_id)
            if skill_list is not None:
                matching_person = find_matching_person(db_engine, s, skill_list)
            if skill_list is not None or matching_person == []:
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

