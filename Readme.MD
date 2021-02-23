# Denstu Engineering Challenge

## Executing the code
1)Unzip the 'Dentsu_DE_Challenge.zip' file  and extract files

2)open docker terminal and navigate to the folder where docker-compose.yml is present

3) Either run using docker-compose up command or run the 'deploy.sh' script to bring the API server up

4) To run bring up the API server and run unit test run 'predeploy.sh' script 

5) To stop the server either use docker-compose down or run 'tear_down.sh' script


## Considerations and assumption
1) Code was developed with enabling the core functionality of the API (GET/POST for person,project and 
GET for person matching the project). The container is not reverse proxy or a production grade
 WSGI server 
 
2) Sufficient test coverage is provided in unit test scripts for core functionality but did not cover 
all probable scenarios

3) As this is not planned for prod grade work, Logging has not been enabled, Exception handling are not 
covered

4) API does not support POST with a json file