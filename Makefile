run:
	uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload

install:
	pip install -r requirements.txt


# Setup virtual environment
setup-env:
	python3 -m venv venv
	@echo "✅ Virtual environment created"
	@echo "📦 Run 'make install' to install dependencies"
	@echo "🔓 Run 'source venv/bin/activate' to activate"

# Activate environment (with helper message)
activate:
	@echo "🔓 Run this command to activate:"
	@echo "source venv/bin/activate"

# ============================================================
# ТЕСТЫ
# ============================================================

# Запуск всех тестов
test:
	pytest tests/ -v

# Запуск тестов с покрытием
test-cov:
	pytest tests/ --cov=src.services --cov-report=term

# Только тесты для судьи
test-judge:
	pytest tests/test_llm_judge.py -v

# Только fallback-тесты (без API)
test-fallback:
	pytest tests/test_llm_judge.py -v -k "fallback"

# Очистка
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/