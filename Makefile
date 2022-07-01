## REQUIRED
PROJECT_NAME := metrics-service

## REQUIRED
export APP := $(PROJECT_NAME)
export VERSION := $(if $(TAG),$(TAG),$(if $(BRANCH_NAME),$(BRANCH_NAME),$(shell git describe --tags --exact-match || git symbolic-ref -q --short HEAD)))
export REPO := docker.dcube.devmail.ru
export DOCKER_BUILDKIT=1
export NOCACHE := $(if $(NOCACHE),"--no-cache")

## REQUIRED
fastapi:
	docker build ${NOCACHE} --pull -f Dockerfile -t ${REPO}/${APP}:${VERSION} --ssh default --progress=plain --build-arg APP=${APP} --build-arg VERSION=${VERSION} --build-arg BUILD_NUMBER=${BUILD_NUMBER} .

## REQUIRED
push:
	docker push ${REPO}/${APP}:${VERSION}

## REQUIRED
build: fastapi
