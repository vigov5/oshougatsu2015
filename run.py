#!venv/bin/python
from app import app
from app import app as application

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)
