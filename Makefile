PATH := ./env/bin:${PATH}
PY :=  $(VIRTUAL_ENV)/bin/python3

include .env.dev
export

SRC := src
DIST := dist
BUILD := build

.PHONY: env test all dev clean dev pyserve $(SRC) $(DIST) $(BUILD)

PYPIU = mhariri
PYPIP = password


ifeq ($(SSL), true)
PROTOCOL := HTTPS
else
PROTOCOL := HTTP
endif
URL := $(PROTOCOL)://$(HOST):$(PORT)

cert: # HTTPS server
		if [ ! -d "./certs" ]; then mkdir ./certs; fi
		if [ -f "./certs/openssl.conf" ] ; then \
		openssl req -x509 -new -config ./certs/openssl.conf -out ./certs/cert.pem -keyout ./certs/key.pem ;  else \
		openssl req -x509 -nodes -newkey rsa:4096 -out ./certs/cert.pem -keyout ./certs/key.pem -sha256 -days 365 ;fi


docker-up:
		docker compose -p $(PROJECT) -f ./config/compose.yaml up -d

docker-down:
		docker compose -p $(PROJECT) -f ./config/compose.yaml down

clean:
		rm -rf ./$(DIST)/* ./$(BUILD)/*

clcache: 
		rm -r ./__pycache__

env: 
		$(PY) -m venv env

check:
		$(PY) -m ensurepip --default-pip
		$(PY) -m pip install --upgrade pip setuptools wheel

test:
		echo $(PATH)
		$(PY) --version
		$(PY) -m pip --version

test-os:
		$(PY) -c 'import sys;print(sys.platform)'

pi: 
		$(PY) -m pip install $(filter-out $@,$(MAKECMDGOALS))
		$(PY) -m pip freeze > requirements.txt

piu:
		$(PY) -m pip install --upgrade $(filter-out $@,$(MAKECMDGOALS))
		$(PY) -m pip freeze > requirements.txt

pia: requirements.txt
		$(PY) -m pip install -r requirements.txt


build:
		$(PY) -m pip install --upgrade build
		$(PY) -m build

preview:
		twine upload -r testpypi -u $(PYPIU) -p $(PYPIP) --repository-url https://test.pypi.org/legacy/ dist/*  --verbose 

preview2:
		twine upload  --config-file .pypirc -r testpypi dist/*  --verbose 

publish:
		$(PY) -m pip install --upgrade twine
		$(PY) -m twine upload --config-file .pypirc --repository testpypi dist/* --verbose  

pylint:
		pylint --rcfile .pylintrc.dev $(SRC)

pylint-prod:
		pylint --rcfile .pylintrc.prod $(SRC)

sort:
		isort $(SRC)

format:
		black $(SRC)

type:
		mypy

type-prod:
		mypy --config-file .mypy.ini.prod
		
#  make g-commit "fixed: typo"
g-commit: format type pylint
		git commit -m "$(filter-out $@,$(MAKECMDGOALS))"

g-log:
		git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit


%: # https://www.gnu.org/software/make/manual/make.html#Automatic-Variables 
		@:


app:
		$(PY) $(SRC)/app.py
