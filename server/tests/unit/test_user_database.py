from website.utilities import database as db
from website.utilities.users import User


def test_no_user_in_db_returns_None():
    assert (db.query_users(username='fjdklsghjnadklnvkanfkdljsan') is None)


def test_user_query_return_type_is_User_object():
    assert (isinstance(db.query_users(username='devuser4'), User))
    return


def test_invalid_insert_into_users_db():
    assert (not db.insert_user('NotAUserObject'))
    assert (not db.insert_user(User(1, None, None)))
    assert (not db.insert_user(User(1, "valid_username", None)))
    assert (not db.insert_user(User(1, None, "valid_password")))
    return
