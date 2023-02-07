from website.utilities import database as db
from website.utilities.users import User


def test_no_user_in_db():
    """Tests db query response for incorrect username.

    Args:
        Invalid username

    Returns:
        Test passed if return from query is None

    Raises:
        Assertion error.
    """
    assert (db.query_users_db(username='ThisCouldNotBeAValidUserName') is None)
    assert (db.query_users_db(user_id=1) is None)
    assert (db.query_users_db() is None)


def test_user_query_return_type():
    """Tests db query response for correct username.

    Args:
        Valid username

    Returns:
        Test passed if return from query is of type User

    Raises:
        Assertion error.
    """
    assert (isinstance(db.query_users_db(username='devuser4'), User))
    return


def test_invalid_insert_into_users_db():
    """Tests db insert request response for invalid insertion object

    Args:
        Invalid User object

    Returns:
        Test passed if return from insertion request is False

    Raises:
        Assertion error.
    """
    assert (not db.insert_user_into_db('NotAUserObject'))
    assert (not db.insert_user_into_db(User(1, None, None)))
    return
