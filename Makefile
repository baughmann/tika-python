test:
	@uv run pytest -v -m 'not benchmark' --junitxml=reports/junit/junit.xml --html=reports/junit/report.html  --cov-report term --cov-report xml:reports/coverage.xml --cov=tika
	@genbadge coverage -i reports/coverage.xml -o reports/images/coverage.svg
	@genbadge tests -i reports/junit/junit.xml -o reports/images/tests.svg

benchmark:
	@pytest -v -m benchmark

.PHONY: test benchmark