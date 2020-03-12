lint:
	flake8 . && mypy src/ && pydocstyle src/
