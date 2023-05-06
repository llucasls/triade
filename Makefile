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

PACKAGE_DIR := .venv/lib/python3.10/site-packages/triade

define DELETED_FILES
$(strip
	$(foreach FILE,
		$(filter-out
		$(notdir $(wildcard triade/*.py)),
		$(notdir $(wildcard .venv/lib/python3.10/site-packages/triade/*.py))),
		$(CURDIR)/.venv/lib/python3.10/site-packages/triade/$(FILE)
	)
)
endef

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
	$(ACTIVATE) && $(PIP) install --upgrade pip
	$(ACTIVATE) && $(PIP) install --upgrade -r dev_requirements.txt
	touch $(VENV)

test: $(VENV)
	$(ACTIVATE) && $(PYTEST) $(PYTEST_FLAGS) $(PYTEST_FILES)

coverage: $(VENV)
	FLAGS="--cov=$(COVERAGE_DIR)"; \
	$(MAKE) --no-print-directory test PYTEST_FLAGS="$${FLAGS}" 2> /dev/null

tar:
	$(TAR) --create --file=triade.tar $(SRC_FILES)

this: $(VENV)
	-rm -f $(DELETED_FILES)
	$(MAKE) --no-print-directory $(patsubst triade/%.py,$(PACKAGE_DIR)/%.py,$(wildcard triade/*.py))

$(PACKAGE_DIR):
	@mkdir -p $(PACKAGE_DIR)

$(PACKAGE_DIR)/%.py: triade/%.py | $(PACKAGE_DIR)
	ln $< $@

.PHONY: build check publish clean install test coverage tar

.SILENT: build check publish install test coverage $(VENV) this
