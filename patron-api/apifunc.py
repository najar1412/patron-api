import config.cred as cred
from models import Base, User, Patron


# private functions
def reset_db(engine):
    """drops tables and rebuild"""
    try:
        User.__table__.drop(engine)
        Patron.__table__.drop(engine)
        print('Old tables removed')
    except:
        print('failed to remove old tables')
    try:
        Base.metadata.create_all(engine)
        print('new tables built')
    except:
        print('failed to build new tables.')

    return True

# public functions
def post_patron(session, **user_columns):
    """ create new patron """
    # Validated query
    query = {}
    # Check user columns
    patron_columns = Patron.__table__.columns.keys()
    # compare user column data to database columns
    for k, v in user_columns.items():
        if k in patron_columns:
            # if match append user data to approved query variable
            query[k] = v
        else:
            pass

    for column in patron_columns:
        # if user data does include all database columns. There are added to
        # approve query variable and padded with 'None'
        if column not in user_columns and column != 'id':
            query[column] = None

    # create new collection and commit to database
    patron = Patron(
        client=query['client'], contact=query['contact'],
        contactemail=query['contactemail'], contactphone=query['contactphone']
    )

    session.add(patron)
    session.commit()
    session.close()

    return patron


def post_user(session, **kwarg):

    """ create new user """
    # Validated query

    query = {}
    # Check user columns
    User_columns = User.__table__.columns.keys()
    # compare user column data to database columns
    for k, v in kwarg.items():
        if k in User_columns:
            # if match append user data to approved query variable
            query[k] = v
        else:
            pass

    for column in User_columns:
        # if user data does include all database columns. There are added to
        # approve query variable and padded with 'None'
        if column not in kwarg and column != 'id':
            query[column] = None

    # create new collection and commit to database

    user = User(
        name=query['name'], team=query['team'], patron_id=query['patron_id']
    )

    session.add(user)
    session.commit()
    session.close()

    # return user
    return user.id


def get_patron(session):
    """Returns all patron objects"""
    patrons = []
    for patron in session.query(Patron).order_by(Patron.id):
        patrons.append(patron)

    return patrons


def get_user(session):
    """Returns all user objects"""
    users = []
    for user in session.query(User).order_by(User.id):
        users.append(user)

    return users


def get_patron_by_id(session, id):
    """return patron by is"""
    patron_by_id = session.query(Patron).get(id)
    result = {
        'id': patron_by_id.id, 'client': patron_by_id.client,
        'contact': patron_by_id.contact, 'contactphone': patron_by_id.contactphone,
        'contactemail': patron_by_id.contactemail, 'user': {}
    }

    for i in patron_by_id.user:
        result['user'][i.id] = {
            'name': i.name, 'team': i.team
        }

    return result


def get_user_by_id(session, id):
    """return user by is"""
    user_by_id = session.query(User).get(id)
    print(user_by_id)
    result = {
        'id': user_by_id.id, 'name': user_by_id.name,
        'team': user_by_id.team, 'patrons': []
    }
    try:
        result['patrons'].append({
            'id': user_by_id.patron.id,
            'client': user_by_id.patron.client,
            'contact': user_by_id.patron.contact,
            'contactemail': user_by_id.patron.contactemail,
            'contactphone': user_by_id.patron.contactphone
        })
    except:
        # TODO: Better errors
        pass

    return result


def patch_patron():
    pass


def patch_user():
    pass


def delete_patron(session, id):
    try:
        to_delete = session.query(Patron).get(id)
        if to_delete:
            session.delete(to_delete)

            session.commit()
            session.close()

            return True

        elif to_delete == None:
            return None
    except:
        # TODO: Catch proper errors
        return False


def delete_user(session, id):
    try:
        to_delete = session.query(User).get(id)
        session.delete(to_delete)

        session.commit()
        session.close()
        print('nada')
        return True
    except:
        # TODO: Catch proper errors
        print('nada')
        return False
