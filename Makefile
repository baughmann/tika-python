test:
	@pytest -v -m 'not benchmark'

benchmark:
	@pytest -v -m benchmark

coverage:
	@pytest --cov=src --cov-report=term-missing -m 'not benchmark'

.PHONY: test benchmark coverage