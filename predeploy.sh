docker-compose down; 
docker-compose up -d --build; 
docker exec -it $(docker ps -qf "name=python_pg_docker_app") python test_app.py