test:
	PYTHONPATH=src/ pytest --capture=no -x
cov: 
	PYTHONPATH=src/ pytest --capture=no --cov=src/
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
