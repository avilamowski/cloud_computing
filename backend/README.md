# Commands 

## Install dependencies
`python3 -m venv .venv`

## Activate virtual environment
`source .venv/bin/activate` 

## Install dependencies
`pip install -r requirements.txt` 

## Run the server (production)
`gunicorn -w 4 -b 0.0.0.0:[port] 'server:app`

## Run the server (development)
`python server.py`