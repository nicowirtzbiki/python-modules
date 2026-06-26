.PHONY: install run debug clean lint lint-strict build

install:
	pip install flake8 mypy build

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache dist build *.egg-info

fclean: clean
	rm -f mazegen-*.whl

lint:
	flake8  --exclude venv  .
	mypy --exclude venv --warn-return-any --warn-unused-ignores \
	       --ignore-missing-imports --disallow-untyped-defs \
	       --check-untyped-defs .

lint-strict:
	flake8 .
	mypy . --strict

build: install
	python3 -m build
	cp dist/mazegen-*.whl . 
