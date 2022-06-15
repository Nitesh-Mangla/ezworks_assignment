#this is direct execute server sh
#pip3 freeze > requirements.txt (to freeze all module in requirements.txt)
#pip install -r ./requirements.txt
#python3 -m venv env

source development/bin/activate
exec python3 app.py