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