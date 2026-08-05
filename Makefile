.PHONY: check test build release

check:
	python3 tools/release.py check

test:
	python3 -m unittest discover -s tests -v

build: check test
	python3 tools/release.py build

release: build
	@echo "Release archives are ready in dist/."
