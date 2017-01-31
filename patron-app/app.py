from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BASEURL = 'http://127.0.0.1:5000/patron/api'

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')

@app.route('/getuser', methods=['GET'])
def getuser():

    r = requests.get('{}/user'.format(BASEURL))

    return render_template('getuser.html', user=r.json())

@app.route('/getpatron', methods=['GET'])
def getpatron():

    r = requests.get('{}/patron'.format(BASEURL))

    return render_template('getpatron.html', patron=r.json())

@app.route('/getuserbyid', methods=['GET'])
def getuserbyid():

    bla = request.args['id']

    r = requests.get('{}/user/{}'.format(BASEURL, str(bla)))

    return render_template('getuserbyid.html', bla=r.json())


@app.route('/getpatronbyid', methods=['GET'])
def getpatronbyid():

    bla = request.args['id']

    r = requests.get('{}/patron/{}'.format(BASEURL, str(bla)))

    return render_template('getpatronbyid.html', bla=r.json())


@app.route('/deluser', methods=['GET'])
def deluser():

    bla = request.args['id']

    del_user = requests.delete('{}/user/delete/{}'.format(BASEURL, int(bla)))
    print(del_user)
    r = requests.get('{}/user'.format(BASEURL))

    return render_template('getuser.html', user=r.json())


@app.route('/delpatron', methods=['GET'])
def delpatron():

    bla = request.args['id']

    del_user = requests.delete('{}/patron/delete/{}'.format(BASEURL, int(bla)))
    r = requests.get('{}/patron'.format(BASEURL))

    return render_template('getpatron.html', patron=r.json())



if __name__ == '__main__':
    app.run(port=5050, debug=True)
