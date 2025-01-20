test:
	@uv run pytest -v -m 'not benchmark' --junitxml=reports/junit/junit.xml --html=reports/junit/report.html  --cov-report term --cov-report xml:reports/coverage.xml --cov=tika
	@genbadge coverage -i reports/coverage.xml -o reports/images/coverage.svg
	@genbadge tests -i reports/junit/junit.xml -o reports/images/tests.svg

benchmark:
	@uv run pytest -v -m benchmark

safety_scan:
	@uv run safety scan --save-as html reports/safety_scan.html

run-ruff:
	@uv run ruff check . --fix && ruff format

generate_badges:
	@genbadge coverage -i reports/coverage.xml -o reports/images/coverage.svg
	@genbadge tests -i reports/junit/junit.xml -o reports/images/tests.svg

check: test benchmark safety_scan generate_badges run-ruff



.PHONY: test benchmark