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


@app.route('/newuser', methods=['POST'])
def newuser():

    if request.method == 'POST':
        form = request.form
        name = form['user']
        team = form['userteam']
        email = form['useremail']

        requests.post('{}/user?name={}&team={}&email={}'.format(
            BASEURL, name, team, email
            )
        )

        """
        # deal with errors
        if post status == 'Failed':
            return error message
        """

    r = requests.get('{}/user'.format(BASEURL))

    return render_template('getuser.html', user=r.json())


@app.route('/newpatron', methods=['POST'])
def newpatron():

    if request.method == 'POST':
        form = request.form
        client = form['patron']
        contact = form['patronname']
        contactphone = form['patronmob']
        contactemail = form['patronemail']

        # 127.0.0.1:5000/patron/api/patron?client=webuildcrap&contact=sally&contactphone=9292349525&contactemail=sally@webuildcrap.co

        requests.post('{}/patron?client={}&contact={}&contactphone={}&contactemail={}'.format(
            BASEURL, client, contact, contactphone, contactemail
            )
        )

        """
        # deal with errors
        if post status == 'Failed':
            return error message
        """

        r = requests.get('{}/patron'.format(BASEURL))

        return render_template('getpatron.html', patron=r.json())


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
