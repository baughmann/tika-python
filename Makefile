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

generate_stubs:
	@uv run python -m stubgenj --classpath "src/tika/jars/tika-app-3.0.0.jar" --convert-strings org.apache.tika java org.apache.commons org.w3c.dom org.xml.sax --output-dir stubs --no-stubs-suffix
# no idea why it generates stubs for jpype, but we have to remove them
	@rm -rf stubs/jpype-stubs



.PHONY: test benchmark