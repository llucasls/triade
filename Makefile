PYTHON = python3.11

VENV   = $(.CURDIR)/.venv

PIP    = $(VENV)/bin/pip
BUILD  = $(VENV)/bin/$(PYTHON) -m build
TWINE  = $(VENV)/bin/twine
PYTEST = $(VENV)/bin/pytest
BUMP   = $(VENV)/bin/bumpline

PYTEST_FLAGS = --verbose --mocha

COVERAGE_DIR = triade

PYTHONPATH = $(.CURDIR)
.export-env PYTHONPATH

.if $(.TARGETS:Minstall) == install
.EXEC: $(VENV)
.endif

dist:
	if test ! -d $@; then mkdir $@; fi

build: $(VENV)
	$(BUILD) $(BUILD_FLAGS)

check: dist
	$(TWINE) check dist/*

publish: build
	$(TWINE) upload dist/*

clean: dist
	rm -rf dist/*

install: $(VENV)

$(VENV): dev_requirements.txt
	if test ! -d "$@"; then $(PYTHON) -m venv "$@"; fi
	$(PIP) install --upgrade pip -r dev_requirements.txt
	touch "$@"

test: $(VENV)
	$(PYTEST) $(PYTEST_FLAGS) $(FILES)

coverage: $(VENV)
	FLAGS="--cov=$(COVERAGE_DIR)"; \
	$(MAKE) test PYTEST_FLAGS="$${FLAGS}" 2> /dev/null

test_%: tests/test_%.py
	$(PYTEST) $(PYTEST_FLAGS) $<

.PHONY: build check publish clean install test coverage

.SILENT: build check publish install test coverage $(VENV)
