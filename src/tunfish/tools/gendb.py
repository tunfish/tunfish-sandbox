from tunfish.database.control import dbc
from tunfish.model import Router
from sqlalchemy import exc

dbc_handler = dbc()

def create_device_fixture():

    router = Router(device_id='DEV0815', user_pw='userpw', device_pw='rootpw', wgprvkey='wgprivkey', wgpubkey='wgpubkey', ip='192.168.100.10')

    try:
        dbc_handler.session.add(router)
        dbc_handler.session.commit()
    except exc.SQLAlchemyError as e:
        print(f"Error: {e}")
        dbc_handler.session.rollback()
    except Exception as e:
        print(f"{e}")


dbc_handler.session.close()
