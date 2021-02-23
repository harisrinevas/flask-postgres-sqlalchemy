from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

#Base model for Person - Mapping to the person table
class PersonModel(Base):

    __tablename__ = "person"
    # column mapping
    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    email = Column(String())
    address = Column(String())
    skills = Column(String())

    def __init__(self, first_name, last_name, email, address, skills):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.skills = skills

    def __repr__(self):
        return "<Person(id= {" + str(self.id) + "}, first_name={"+self.first_name + "}, last_name={"\
                                      + self.last_name + "}, email={" + self.email + "})>"


#Base model for Person - Mapping to the project table
class ProjectModel(Base):

    __tablename__ = "project"
    # column mapping
    id = Column(Integer(), primary_key=True)
    project_name = Column(String())
    date_posted = Column(String())
    department = Column(String())
    description = Column(String())
    skills = Column(String())

    def __init__(self, project_name, date_posted, department, description, skills):
        self.project_name = project_name
        self.date_posted = date_posted
        self.department = department
        self.description = description
        self.skills = skills

    def __repr__(self):
        return "< Project( project_name={" + self.project_name + \
               " date_posted={" + self.date_posted + "} department={" + self.department + \
               "description={" + self.description + "} skills={" + self.skills + "}>"

