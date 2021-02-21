from app.app import db


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

