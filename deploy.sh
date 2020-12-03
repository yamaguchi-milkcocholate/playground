#!/bin/zsh

app=playground-d

heroku login
heroku container:login
docker build -t registry.heroku.com/$app/web .
docker push registry.heroku.com/$app/web
heroku container:release --app $app web