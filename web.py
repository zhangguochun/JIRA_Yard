from flask import Flask
from configuration import DEBUG

app = Flask(__name__, static_url_path = "/pic", static_folder = "pic")

def render():
    rpt=open('report.html','r+')

    t=''
    for line in rpt:
        t=t+line

    return t



@app.route('/')
def hello_world():
    return render()

if __name__ == '__main__':
    app.run(debug=DEBUG,host='0.0.0.0')
