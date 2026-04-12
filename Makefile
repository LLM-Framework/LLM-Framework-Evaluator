run:
	uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload

install:
	pip install -r requirements.txt