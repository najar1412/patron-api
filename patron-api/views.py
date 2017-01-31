from flask import Flask, jsonify, request, make_response
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from apifunc import (
    post_patron, get_user, reset_db, post_user, get_patron, get_patron_by_id,
    get_user_by_id, delete_patron, delete_user
)
from models import Patron, User

import config.cred as cred


app = Flask(__name__)

# Globals
BASE_ROUTE = '/patron/api'
TEAM = ['new york', 'london', 'los angeles']
USER_COLUMNS =['name', 'team', 'patron_id']
PATRON_COLUMNS = ['client', 'contact', 'contactemail', 'contactphone']

# Int sqlalchemy engine
engine = create_engine(
    'postgresql://{}:{}@{}:5432/glance'.format(
        cred.username, cred.password, cred.ip
    ),
    echo=False
)

# Init sessionmaker
Session = sessionmaker(bind=engine)

@app.route('{}/patron'.format(BASE_ROUTE), methods=['POST', 'GET'])
def patron():

    # Init session
    session = Session()

    if request.method == 'POST':
        try:
            # query dict collector
            query = {}
            # query dict padder (for empty values)
            param_list = PATRON_COLUMNS
            for attri in request.args:
                query[attri] = request.args[attri]
                for param in param_list:
                    if param not in query:
                        query[param] = None

            patron = post_patron(session, **query)

            print(query)

            return make_response(
                jsonify({'{} Status'.format(request.method): 'Success'})
            ), 200

        except:
            return make_response(
                jsonify({'Status': 'failed'})
            ), 404

    elif request.method == 'GET':

        patrons = get_patron(session)

        result = []
        for patron in patrons:
            result.append({
                'id': patron.id,
                'client': patron.client,
                'contact': patron.contact,
                'phone': patron.contactphone,
                'email': patron.contactemail
            })

        return make_response(
            jsonify({'{} Status'.format(request.method): 'Success'},
            {'Patrons': result}
            )
        ), 200

    return make_response(
        jsonify({'Status': 'failed'})
    ), 404


@app.route('{}/user'.format(BASE_ROUTE), methods=['POST', 'GET'])
def user():

    # Init session
    session = Session()

    if request.method == 'POST':
        if 'patron_id' in request.args:
            id_check = session.query(Patron).get(request.args['patron_id'])
            if id_check == None:
                return make_response(
                    jsonify(
                        {
                            '{} Status'.format(request.method): 'Failed'
                        },
                        {
                            'Message': 'Patron_id does not exists.'
                        }
                    )
                ), 400
        if 'name' not in request.args or 'team' not in request.args:
            return make_response(
                jsonify(
                    {
                        '{} Status'.format(request.method): 'Failed'
                    },
                    {
                        'Message': 'Request must include \'name\' and \'team\'.',
                        'Valid Data': 'name=name, team=team'
                    }
                )
            ), 400
        try:
            # query dict collector
            query = {}
            # process and valid requests
            param_list = USER_COLUMNS
            for attri in request.args:
                if attri == 'team':
                    if request.args[attri].lower() not in TEAM:
                        # check if User team is valid
                        # return failed if invalid
                        return make_response(
                            jsonify(
                                {
                                    '{} Status'.format(request.method): 'Failed'
                                },
                                {
                                    'Message': 'Team is invalid.',
                                    'Valid Data': '{}'.format(TEAM)
                                }
                            )
                        ), 400

                # build valid request dict, and send to function
                query[attri] = request.args[attri].lower()
                for param in param_list:
                    if param not in query:
                        query[param] = None

            user = post_user(session, **query)

            return make_response(
                jsonify({'{} Status'.format(request.method): 'Success'})
            ), 200

        except:
            # TODO:
            return make_response(
                jsonify({'Status': 'sdfsdfsdf'})
            ), 404

    elif request.method == 'GET':

        users = get_user(session)
        # TODO: refactor below loop to func, or api func
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'name': user.name,
                'team': user.team,
                'patron_id': user.patron_id
            })


        # result = [x for x in users]

        return make_response(
            jsonify({'{} Status'.format(request.method): 'Success'},
            {'Users': result}
            )
        ), 200

    return make_response(
        jsonify({'Status': 'bla'})
    ), 404


@app.route('{}/user/<id>'.format(BASE_ROUTE), methods=['GET'])
def user_by_id(id):
    if request.method == 'GET':

        # Init session
        session = Session()

        result = get_user_by_id(session, id)

        return make_response(
            jsonify(
                {'{} Status'.format(request.method): 'Success'},
                {'User': result}
            )
        ), 200

    return make_response(
        jsonify({'Status': 'failed'})
    ), 404


@app.route('{}/patron/<id>'.format(BASE_ROUTE), methods=['GET'])
def patron_by_id(id):
    if request.method == 'GET':

        # Init session
        session = Session()

        result = get_patron_by_id(session, id)

        return make_response(
            jsonify(
                {'{} Status'.format(request.method): 'Success'},
                {'Patron': result}
            )
        ), 200

    return make_response(
        jsonify({'Status': 'failed'})
    ), 404


@app.route('{}/user/patch'.format(BASE_ROUTE), methods=['PATCH'])
def patch_user():
    if request.method == 'PATCH':

        return make_response(
            jsonify({'{} Status'.format(request.method): 'Success'.format(request.method)})
        ), 200

    return make_response(
        jsonify({'Status': 'failed'})
    ), 404


@app.route('{}/patron/patch'.format(BASE_ROUTE), methods=['PATCH'])
def patch_patron():
    if request.method == 'PATCH':

        return make_response(
            jsonify({'{} Status'.format(request.method): 'Success'.format(request.method)})
        ), 200

    return make_response(
        jsonify({'Status': 'failed'})
    ), 404


@app.route('{}/user/delete/<id>'.format(BASE_ROUTE), methods=['DELETE'])
def del_user(id):
    if request.method == 'DELETE':
        print(id)

        # Init session
        session = Session()

        result = delete_user(session, id)

        return make_response(
            jsonify({'{} Status'.format(request.method): 'Success'.format(request.method)})
        ), 200

    return make_response(
        jsonify({'Status': 'failed'})
    ), 404


@app.route('{}/patron/delete/<id>'.format(BASE_ROUTE), methods=['DELETE'])
def del_patron(id):
    if request.method == 'DELETE':

        # Init session
        session = Session()

        result = delete_patron(session, id)
        if result:
            return make_response(
                jsonify({'{} Status'.format(request.method): 'Success'})
            ), 200

        elif result == None:
            return make_response(
                jsonify(
                    {'{} Status'.format(request.method): 'Failed'},
                    {'message': 'ID does not exist'}
                )
            ), 200

    return make_response(
        jsonify({'Status': 'failed'})
    ), 404


# reset_db(engine)

if __name__ == '__main__':
    app.run(debug=True)
