from flask import Flask, render_template

app = Flask(__name__)


@app.route('/linreg')
def linreg():
    return render_template('linreg.html')


app.run()
