.PHONY: build test

test: venv
	. venv/bin/activate && py.test tests -v

venv:
	python3.7 -m venv venv; \
	. venv/bin/activate; \
	pip3 install -r requirements.txt; \
	pip3 install -r tests/requirements.txt; \
	touch venv
