.PHONY: test test-cov test-cov-html install-test help

help:
	@echo "Comandos disponibles:"
	@echo "  make install-test     - Instala dependencias de testing"
	@echo "  make test             - Ejecuta los tests"
	@echo "  make test-cov         - Ejecuta tests con reporte de cobertura en terminal"
	@echo "  make test-cov-html    - Ejecuta tests y genera reporte HTML de cobertura"

install-test:
	pip install -r requirements-test.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=term-missing -v

test-cov-html:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v
	@echo "Reporte HTML generado en htmlcov/index.html"

clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -f .coveragerc
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
