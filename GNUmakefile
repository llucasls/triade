PYTHON = python3

VENV   = $(CURDIR)/.venv

PIP    = $(VENV)/bin/pip
BUILD  = $(VENV)/bin/python -m build
TWINE  = $(VENV)/bin/twine
PYTEST = $(VENV)/bin/pytest
BUMP   = $(VENV)/bin/bumpline

PYTEST_FLAGS = --verbose --mocha

COVERAGE_DIR = triade

export PYTHONPATH = $(CURDIR)

VERSION != awk -F\" '/version/ { print $$2; }' pyproject.toml
TARBALL := $(wildcard dist/triade-$(VERSION).tar.gz)

dist:
	mkdir dist

ifdef TARBALL
build: $(VENV)
else
build: $(VENV)
	$(BUILD) $(BUILD_FLAGS)
endif

check: | dist
	$(TWINE) check dist/*

publish: build
	$(TWINE) upload dist/*

clean: | dist
	rm -f dist/*

install:
	$(MAKE) --always-make --no-print-directory $(VENV)

$(VENV): dev_requirements.txt
	if test ! -d "$@"; then $(PYTHON) -m venv "$@"; fi
	$(PIP) install --upgrade pip -r $<
	touch "$@"

test: $(VENV)
	$(PYTEST) $(PYTEST_FLAGS) $(FILES)

coverage: $(VENV)
	if test -t 1; then color=-c; else color=-C; fi; \
	PYTEST=$(PYTEST) $(VENV)/bin/$(PYTHON) tasks/get_coverage.py $${color}

test_%: tests/test_%.py
	$(PYTEST) $(PYTEST_FLAGS) $<

.PHONY: build check publish clean install test coverage

.SILENT: build check publish install test coverage $(VENV)
