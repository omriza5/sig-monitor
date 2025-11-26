from flask import Flask
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)

@app.route('/health')
def health():
    return "OK" , 200

if __name__ == '__main__':
    app.run(debug=True)