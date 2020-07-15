sudo docker build -t fastapi .
heroku login
heroku container:login
heroku container:push web --app fastapi-template
heroku container:release web --app fastapi-template
