test:
	PYTHONPATH=src/ pytest --capture=no -x
cov: 
	PYTHONPATH=src/ pytest --capture=no --cov=src/
