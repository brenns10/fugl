PHONY: run migrate test clean
run: PATH  := venv/bin/:$(PATH)
run: migrate venv
	venv/bin/python corvid/manage.py runserver

migrate: venv
	venv/bin/python corvid/manage.py makemigrations
	venv/bin/python corvid/manage.py migrate

test: migrate venv
	cd corvid && ../venv/bin/python manage.py test

coverage: migrate venv
	cd corvid && ../venv/bin/coverage run --source=corvid,main --omit=\*/migrations/\*,\*/management/\*,corvid/wsgi.py manage.py test
	cd corvid && ../venv/bin/coverage html -d ../htmlcov

venv:
	virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt

clean:
	rm -rf venv/
	find ./ -type d -name '__pycache__' | xargs rm -rf
