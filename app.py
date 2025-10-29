from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "the changes are seen damnn! this is a change from remote repo "

if __name__ == '__main__':
    app.run(debug=True)
