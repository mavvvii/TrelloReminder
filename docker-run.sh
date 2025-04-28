#!/bin/bash

compose="docker-compose -f"

dev="docker-compose.dev.yaml"
prod="docker-compose.yaml"

build_dev(){
  ${compose} ${dev} build
}

start_dev(){
  ${compose} ${dev} up
}

stop_dev(){
  ${compose} ${dev} down
}

build_prod(){
  ${compose} ${prod} build
}

start_prod(){
  ${compose} ${prod} up
}

stop_prod(){
  ${compose} ${prod} down
}

case "$1" in
    build-dev) build_dev ;;
    start-dev) start_dev ;;
    stop-dev)  stop_dev ;;
    build-prod) build_prod ;;
    start-prod) start_prod ;;
    stop-prod) stop_prod ;;
    *)
        echo "Użycie: $0 {build-dev|start-dev|stop-dev|build-prod|start-prod|stop-prod}"
        exit 1
esac