.PHONY: install dev dev-back dev-front test

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	cd fend && npm ci

dev-back:
	cd bend/src && ../../.venv/bin/python main.py

dev-front:
	cd fend && npm run dev

dev:
	$(MAKE) -j2 dev-back dev-front

test:
	.venv/bin/pytest
	cd fend && npx vitest run
