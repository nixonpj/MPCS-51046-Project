from flask import Flask, escape, request, render_template

app = Flask(__name__)

SHGs = [
    {
        'name': 'Shiv SHG',
        'date_of_formation': '12/04/2018',
        'address': 'Prabhat Colony, Kaithal',
        'no_members': 10
    },
    {
        'name': 'Bholenath SHG',
        'date_of_formation': '19/02/2017',
        'address': 'Pilot Colony, Kaithal',
        'no_members': 10
    }
]

@app.route('/')
@app.route('/home')
def home():
    name = request.args.get("name", "Nixon")
    return render_template("home.html", shgs=SHGs)

@app.route('/about')
def about():
    name = request.args.get("name", "Nixon")
    return f'<h1>About Page<h1>'



if __name__ == '__main__':
    app.run(debug=True)
