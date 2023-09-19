from flask import Flask, render_template

app = Flask(__name__)

@app.route('/design_reference')
def design_reference():
    dynamic_content = "This content is coming from Flask!"
    #Keep design reference untouched
    return render_template("design_reference.html")

@app.route('/index')
def index():
    #This will be our base, customised template that pages will follow
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


@app.route('/role_creation')
def role_creation():
    dynamic_content = "This content is coming from Flask!"
    return render_template("role_creation.html")

if __name__ == '__main__':
    app.run(debug=True)