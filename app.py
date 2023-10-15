from flask import Flask, render_template, request, redirect, url_for
from AccessControlManager import AccessControlManager

app = Flask(__name__)
db_name = 'access_control_db.sqlite'
acm = AccessControlManager(db_name)

# @app.route('/')
# def index():
#     rules = acm.get_access_control_rules()
#     return render_template('index.html', rules=rules)

@app.route('/grant', methods=['POST'])
def grant_permission():
    user = request.form['user']
    resource = request.form['resource']
    action = request.form['action']
    acm.grant_permission(user, resource, action)
    return redirect(url_for('index'))

@app.route('/revoke', methods=['POST'])
def revoke_permission():
    user = request.form['user']
    resource = request.form['resource']
    action = request.form['action']
    acm.revoke_permission(user, resource, action)
    return redirect(url_for('index'))

@app.route('/')
def index():
    rules = acm.get_access_control_rules()
    return render_template('index.html', rules=rules)


if __name__ == '__main__':
    app.run(debug=True)
