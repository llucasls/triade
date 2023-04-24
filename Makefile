PYTHON = python3
BUILD  = /usr/bin/python3 -m build
TWINE  = $(PYTHON) -m twine
PYTEST = $(PYTHON) -m pytest
PIP    = $(PYTHON) -m pip

VENV     = $(CURDIR)/.venv
ACTIVATE = . $(VENV)/bin/activate

BUMP = bumpline

PYTEST_FLAGS = --verbose --mocha

COVERAGE_DIR = triade/

TAR       = tar
TAR_FLAGS = --create --file=$(SRC_ARCHIVE)

SRC_FILES    = pyproject.toml README.md triade/*.py
SRC_ARCHIVE := $(shell mktemp --dry-run --suffix=.tar)

dist:
	mkdir dist

build:
	$(BUILD) $(BUILD_FLAGS)

check: | dist
	$(TWINE) check dist/*

publish: build
	$(TWINE) upload dist/*

clean: | dist
	rm -rf dist/*

install:
	$(MAKE) --always-make --no-print-directory $(VENV)

$(VENV): dev_requirements.txt
	if test ! -d $(VENV); then $(PYTHON) -m venv $(VENV); fi
	$(ACTIVATE) && $(PIP) install --upgrade -r dev_requirements.txt
	touch $(VENV)

test: $(VENV)
	$(ACTIVATE) && $(PYTEST) $(PYTEST_FLAGS) $(PYTEST_FILES)

coverage: $(VENV)
	FLAGS="--cov=$(COVERAGE_DIR)"; \
	$(MAKE) --no-print-directory test PYTEST_FLAGS="$${FLAGS}" 2> /dev/null

tar:
	$(TAR) --create --file=triade.tar $(SRC_FILES)

.PHONY: build check publish clean install test coverage tar

.SILENT: build check publish install test coverage $(VENV)
