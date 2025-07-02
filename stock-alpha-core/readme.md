python3 -m venv stock-venv 
source stock-venv/bin/activate

pip install -r requirements.txt


#to run dev
python -m uvicorn main:app --reload

#Build Docker image
docker build -t stock-alpha-core .

#Run docker container
docker run -p 8000:8000 stock-alpha-core


For test unit
pip install pytest httpx

To run unit test
pytest tests/test_backtest_api.py
or
PYTHONPATH=. pytest tests/test_backtest_api.py

