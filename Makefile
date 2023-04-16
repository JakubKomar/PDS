# Monitoring of BitTorrent Traffic in LAN
# PDS project
# Academic year 2022/2023
# autor: Bc. Jakub Komárek

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
MAIN = main.py
 
.PHONY: all build run pack clean  create_env clean_env

all: build

build:create_env

pack: 
	zip -r 222161.zip main.py packetsParse.py README.md doc.pdf Makefile requirements.txt logs/*

run:
	$(PYTHON) $(MAIN) $(ARGS)

create_env:
	python3 -m venv $(VENV) 
	$(PYTHON) -m pip install  -r requirements.txt

clean_env:
	rm -rf $(VENV)

clean: clean_env
	if [ -d "cert" ]; then rm -r "cert"; fi  &\
	rm -rf 222161.zip
