venv: 
	python3 -m venv .venv
	@echo '~~~	To activate the venv, run:'
	@echo '	source .venv/bin/activate'

install:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

secret:
	@echo "SECRET_KEY=$(SECRET_KEY)" >> .env
	
secure:
	openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem



