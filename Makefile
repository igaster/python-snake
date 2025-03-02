.PHONY: venv init test run

PYTHON = python3

venv:
	@echo "Activating python virtual environment..."
	@. venv/bin/activate

init:
	@if [ ! -d "venv" ]; then \
		$(PYTHON) -m venv venv; \
	fi
	@. venv/bin/activate
	@venv/bin/pip3 install --upgrade pip
	@venv/bin/pip3 install pytest pygame pygbag

test: venv
	venv/bin/pytest test_game.py -v

run: venv
	venv/bin/python3 game.py