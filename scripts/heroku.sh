#!/bin/sh

mkdir -p test-reports
rm -f test-reports/heroku_deployment.log

echo "### Deploying the Heroku app from DockerHub ###" >> test-reports/heroku_deployment.log
docker -v >> test-reports/heroku_deployment.log

echo "Login to DockerHub" >> test-reports/heroku_deployment.log
docker login >> test-reports/heroku_deployment.log

echo "Pull the published image from DockerHub" >> test-reports/heroku_deployment.log
docker pull jai6016/carthage_docker_app >> test-reports/heroku_deployment.log

echo "Re-tag the Docker Image with the heroku_docker_app tag" >> test-reports/heroku_deployment.log
docker tag jai6016/carthage_docker_app heroku_docker_app >> test-reports/dockerize.log

echo "Set the HEROKU_APP_KEY for access" >> test-reports/heroku_deployment.log
heroku -v >> test-reports/heroku_deployment.log
export HEROKU_API_KEY=c4a9906d-2b97-45b0-80eb-d11f8a9b15b6

echo "Destroy the Heroku app if exists" >> test-reports/heroku_deployment.log
heroku apps:destroy -a carthage-heroku-app -c carthage-heroku-app >> test-reports/heroku_deployment.log

echo "Create an an app on Heroku" >> test-reports/heroku_deployment.log
heroku apps:create -a carthage-heroku-app >> test-reports/heroku_deployment.log

echo "Login to Heroku registry" >> test-reports/heroku_deployment.log
heroku container:login >> test-reports/heroku_deployment.log

echo "Re-tag the heroku_docker_app with Heroku registry" >> test-reports/heroku_deployment.log
docker tag heroku_docker_app registry.heroku.com/carthage-heroku-app/web >> test-reports/heroku_deployment.log

echo "Push the Docker app to the Heroku" >> test-reports/dockerize.log
docker push registry.heroku.com/carthage-heroku-app/web >> test-reports/heroku_deployment.log

echo "Release the Docker container on Heroku" >> test-reports/heroku_deployment.log
heroku container:release web -a carthage-heroku-app >> test-reports/heroku_deployment.log