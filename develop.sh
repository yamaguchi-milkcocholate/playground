#!/bin/zsh

docker build -t web:latest .
docker stop local-playground
docker run -d --rm --name local-playground -e "PORT=8765" -p 8007:8765 web:latest