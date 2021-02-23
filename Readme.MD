# Denstu Engineering Challenge

## Executing the code
1) Unzip the 'Dentsu_DE_Challenge.zip' file  and extract files

2) open docker terminal and navigate to the folder where docker-compose.yml is present

3) Either run using docker-compose up command or run the 'deploy.sh' script to bring the API server up

4) To run bring up the API server and run unit test run 'predeploy.sh' script 

5) To stop the server either use docker-compose down or run 'tear_down.sh' script

6) By default the BULK_LOAD option is set in .env file, which means when the first API call is made 
all the records from the JSON files would be uploaded. API allows duplicate insert, hence the GET and POST action 
to add/ retreive data can be performed even after the bulk load. BULK_LOAD option is to support 
"Get match" API (to match people to projects) as soon as the server starts.

7) "Get match" API gets top 5 matches for the project



## Considerations and assumption
1) Code was developed with enabling the core functionality of the API (GET/POST for person,project and 
GET for person matching the project). The container is not reverse proxy or a production grade
 WSGI server 
 
2) Sufficient test coverage is provided in unit test scripts for core functionality but did not cover 
all probable scenarios

3) As this is not planned for prod grade work, Logging has not been enabled, Exception handling are not 
covered

4) API does not support POST with a json file

