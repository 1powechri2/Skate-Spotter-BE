from flask import Flask, request, render_template
import db_models

app = Flask(__name__)

@app.route('/')
def hello():
    return 'SKATEBOARDING IS NOT A CRIME'

# @app.route('/user/<int:id>')
# def no_query_string(id=1):
#     return '<h1> The Query id is ' + str(id) + '</h1>'

if __name__ == '__main__':
    app.run(debug=True)
