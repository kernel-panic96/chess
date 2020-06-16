run:
	cd tui-client && PYTHONPATH=../src python3 main_loop.py

test:
	./tests/run --source-root ./src/ --verbose 2 

pytest:
	PYTHONPATH=src/:tests/ pytest --capture=no --pdbcls=IPython.terminal.debugger:TerminalPdb -v 

cov: 
	PYTHONPATH=src/:tests/ pytest --capture=no --pdbcls=IPython.terminal.debugger:TerminalPdb --cov=src/

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
