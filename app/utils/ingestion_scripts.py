import json


def load_projects():
    json_file = './data/projects.json'
    file_length = (len(open(json_file, 'r').readlines()))
    with open(json_file, 'r') as f:
        for i in range(file_length):
            text = f.readline()
            json_text = json.loads(text)
            return json_text


def load_person():
    json_file = './data/people.json'
    file_length = (len(open(json_file, 'r').readlines()))
    with open(json_file, 'r') as f:
        for i in range(file_length):
            text = f.readline()
            json_text = json.loads(text)
            return json_text
