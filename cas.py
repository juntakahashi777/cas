from flask import Flask, request
from jinja2 import Environment, PackageLoader

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def test():
    def render_controlpanel():
        env = Environment(loader=PackageLoader('cas', 'templates'))
        template = env.get_template('controlpanel.jinja.html')
        return template.render()
        
    if request.method == 'GET':
        return render_controlpanel()
    else:
        
        return render_controlpanel()

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0", 5000)
