from flask import Flask, request, url_for, redirect
from jinja2 import Environment, PackageLoader
from cassandra.cluster import Cluster

app = Flask(__name__)
cluster = Cluster()
session = cluster.connect('mykeyspace')
msgid = 0


@app.route("/", methods=['GET', 'POST'])
def route_main():
    global msgid
    def render_controlpanel():
        data = session.execute('SELECT * from users')
        env = Environment(loader=PackageLoader('cas', 'templates'))
        template = env.get_template('controlpanel.jinja.html')
        return template.render(data=data)
        
    if request.method == 'GET':
        return render_controlpanel()
    else:
        msgid += 1
        input_a = request.form['input_a']
        input_b = request.form['input_b']
        print input_a, input_b
        session.execute(
            '''INSERT INTO users (user_id, fname, lname) 
            values (%s, %s, %s)''', (msgid, input_a, input_b))
        return render_controlpanel()

@app.route("/clear", methods=['GET'])
def route_clear():
    global msgid
    msgid = 0
    session.execute('truncate users')
    return redirect(url_for('route_main'))
    
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=3400)
