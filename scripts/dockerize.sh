#!/bin/sh

mkdir -p test-reports
rm -f test-reports/dockerize.log

echo "### Dockrizing the Python/Flask app strated ###" >> test-reports/dockerize.log
docker -v >> test-reports/dockerize.log

echo "Listing all the Docker Containers" >> test-reports/dockerize.log
docker ps -a >> test-reports/dockerize.log

echo "List of available Docker images" >> test-reports/dockerize.log
docker images >> test-reports/dockerize.log

echo "Clear out the local instances of Docker" >> test-reports/dockerize.log
docker system prune -a -f >> test-reports/dockerize.log

echo "Building the Docker Image" >> test-reports/dockerize.log
docker build -t docker_flask_app:latest . >> test-reports/dockerize.log

echo "List of available Docker images" >> test-reports/dockerize.log
docker images >> test-reports/dockerize.log

echo "Start running the Docker Image build" >> test-reports/dockerize.log
docker run -d -p 5000:5000 docker_flask_app:latest >> test-reports/dockerize.log

echo "Running Docker Containers" >> test-reports/dockerize.log
docker ps >> test-reports/dockerize.log

echo "Calling the test-script.sh for testing the Flask app running in Docker" >> test-reports/dockerize.log
sleep 10
chmod 777 ./scripts/test-script.sh
sh ./scripts/test-script.sh
cat ./test-reports/test_script.log >> test-reports/dockerize.log

echo "Stopping the running Docker container" >> test-reports/dockerize.log
docker kill $(docker ps -q) >> test-reports/dockerize.log

echo "Login to DockerHub" >> test-reports/dockerize.log
docker login >> test-reports/dockerize.log

echo "Re-tag the Docker Image with the username/key" >> test-reports/dockerize.log
docker tag docker_flask_app jai6016/carthage_docker_app >> test-reports/dockerize.log

echo "Inspecting the Docker container" >> test-reports/dockerize.log
docker inspect docker_flask_app >> test-reports/dockerize.log

echo "Publishing the Docker Image on DockerHub" >> test-reports/dockerize.log
docker push jai6016/carthage_docker_app >> test-reports/dockerize.log

echo "Clear out the local instances of Docker" >> test-reports/dockerize.log
docker system prune -a -f >> test-reports/dockerize.log
