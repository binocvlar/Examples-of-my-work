.PHONY: check doco stylecheck typecheck

passfile := ~/pw

doco: send_readme_to_confluence.py README.md
	@./send_readme_to_confluence.py rphillis $(passfile)

stylecheck: send_readme_to_confluence.py
	flake8 --max-line-length=140 send_readme_to_confluence.py

typecheck: send_readme_to_confluence.py
	mypy --ignore-missing-imports send_readme_to_confluence.py

check: typecheck stylecheck
