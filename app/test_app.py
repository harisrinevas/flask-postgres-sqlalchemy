from unittest import TestCase
import unittest
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils.ingestion_scripts import *
from sqlalchemy import create_engine
from utils.GlobalConfig import get_logger
import os
from utils.curd import *
from app import app
from flask_testing import TestCase
import requests
import responses

class UnitTestApp(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.app = app
        self.db_engine = create_engine(db_string)
        self.s = Session()

    def create_app(self):
        return app

    def test_person_bulk_load(self):
        self.s.query(PersonModel).delete()
        load_person()
        query = self.s.query(PersonModel).count()
        self.assertEqual(1000, query, "data has been loaded")
        self.s.close()

    def test_project_bulk_load(self):
        self.s.query(ProjectModel).delete()
        load_projects()
        query = self.s.query(ProjectModel).count()
        self.assertEqual(1000, query, "matching counts")
        self.s.close()

    def test_add_person(self):
        data = {
            "first_name": "Sherlock",
            "last_name": "Holmes",
            "email": "email",
            "address": "221B baker st",
            "skills": ["python", "postgres", "docker"]
        }
        new_person = insert_person_data(self.s, data)
        self.assertEqual( new_person.first_name, data["first_name"], "Match found")
        self.assertEqual(new_person.last_name, data["last_name"], "Match found")
        self.assertEqual(new_person.email, data["email"], "Match found")
        self.assertEqual(new_person.address, data["address"],  "Match found")
        self.assertEqual(new_person.skills, data["skills"],  "Match found")

    def test_add_project(self):
        data = {
            "project_name": "Finding Sherlock",
            "department": "Investigation",
            "description": "This is a test project",
            "date_posted": "12/25/2019",
            "skills": ["python", "postgres", "docker"]
        }
        new_project = insert_project_data(self.s, data)
        self.assertEqual(new_project.project_name, data["project_name"], "Match found")
        self.assertEqual(new_project.department, data["department"], "Match found")
        self.assertEqual(new_project.description, data["description"], "Match found")
        self.assertEqual(new_project.date_posted, data["date_posted"], "Match found")
        self.assertEqual(new_project.skills, data["skills"], "Match found")

    def test_get_project_skills(self):
        self.s.query(ProjectModel).delete()
        data = {
            "project_name": "Finding Sherlock",
            "department": "Investigation",
            "description": "This is a test project",
            "date_posted": "12/25/2019",
            "skills": ["python", "postgres", "docker"]
        }
        new_project = insert_project_data(self.s, data)
        project_skill = get_project_skills(self.s, new_project.id)
        self.assertEqual(project_skill, data["skills"], "project skill match")

    def test_find_matching_person(self):
        self.s.query(ProjectModel).delete()
        self.s.query(PersonModel).delete()
        data_project = {
            "project_name": "Finding Sherlock",
            "department": "Investigation",
            "description": "This is a test project",
            "date_posted": "12/25/2019",
            "skills": ["python", "postgres", "docker"]
        }
        new_project = insert_project_data(self.s, data_project)

        find_id = new_project.id

        data_person1 = {
            "first_name": "Sherlock",
            "last_name": "Holmes",
            "email": "email",
            "address": "221B baker st",
            "skills": ["python", "postgres", "docker"]
        }

        new_person1 = insert_person_data(self.s, data_person1)
        data_person2 = {
            "first_name": "Dr",
            "last_name": "Watson",
            "email": "email",
            "address": "221B baker st",
            "skills": ["C++", "Java", "cli"]
        }
        new_person2 = insert_person_data(self.s, data_person2)

        project_skill = get_project_skills(self.s, find_id)
        result_lists = find_matching_person(self.db_engine, self.s, project_skill)
        for result_list in result_lists[0]:
            self.assertEqual(result_list["first_name"], data_person1["first_name"],
                             "matching person found")
            self.assertNotEqual(result_list["first_name"], data_person2["first_name"],
                             "matching person found")
        self.assertEqual(len(result_lists), 1, "Match found")

    def test_get_project(self):
        self.s.query(ProjectModel).delete()
        data_project = {
            "project_name": "Finding Sherlock",
            "department": "Investigation",
            "description": "This is a test project",
            "date_posted": "12/25/2019",
            "skills": ["python", "postgres", "docker"]
        }
        new_project = insert_project_data(self.s, data_project)

        data = {
            "id": new_project.id
        }
        app_url = self.app.test_client()
        get_response = app_url.get('/project', json=data)
        self.assertEqual(get_response.status_code, 200, "match found")

    def test_get_person(self):
        self.s.query(PersonModel).delete()
        data_person = {
            "first_name": "Sherlock",
            "last_name": "Holmes",
            "email": "email",
            "address": "221B baker st",
            "skills": ["python", "postgres", "docker"]
        }
        new_person = insert_person_data(self.s, data_person)

        data = {
            "id": new_person.id
        }
        app_url = self.app.test_client()
        get_response = app_url.get('/person', json=data)
        self.assertEqual(get_response.status_code, 200, "match found")

    def test_post_person(self):
        self.s.query(PersonModel).delete()
        data_person = {
            "first_name": "Sherlock",
            "last_name": "Holmes",
            "email": "email",
            "address": "221B baker st",
            "skills": ["python", "postgres", "docker"]
        }
        app_url = self.app.test_client()
        get_response = app_url.post('/person', data=data_person)
        self.assertEqual(get_response.status_code, 200, "match found")

    def test_post_project(self):
        self.s.query(ProjectModel).delete()
        data_project = {
            "project_name": "Finding Sherlock",
            "department": "Investigation",
            "description": "This is a test project",
            "date_posted": "12/25/2019",
            "skills": ["python", "postgres", "docker"]
        }
        app_url = self.app.test_client()
        get_response = app_url.post('/project', data=data_project)
        self.assertEqual(get_response.status_code, 200, "match found")

    @classmethod
    def tearDown(cls) -> None:
        pass


if __name__=="__main__":
    unittest.main()
