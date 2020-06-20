run:
	PYTHONPATH=./ python3 tui-client/main_loop.py tui-client/controls.json

test:
	pytest --cov chess/ \
		--cov-report=term-missing \
		--cov-report=xml:cov.xml \
		--cov-report=html \
		--cov-branch \
		--doctest-modules \
		--verbosity=2 \
		--durations=10 \
		--capture=no\
		--pdbcls=IPython.terminal.debugger:TerminalPdb
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
