from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    dynamic_content = "This content is coming from Flask!"
    return render_template("index.html")

@app.route('/listings')
def listings():
    dynamic_content = "This content is coming from Flask!"
    return render_template("listings.html")

@app.route('/applied_roles')
def applied_roles():
    dynamic_content = "This content is coming from Flask!"
    return render_template("applied_roles.html")



if __name__ == '__main__':
    app.run(debug=True)