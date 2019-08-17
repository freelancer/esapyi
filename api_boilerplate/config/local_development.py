import os

DEBUG = True
ENV = 'development'

SQLALCHEMY_DB_URI = '{engine}://{user}:{pwd}@{addr}:{port}/{db_name}'.format(
    engine='mysql+pymysql',
    user=os.environ['API_BOILERPLATE_DB_ENV_MYSQL_USER'],
    pwd=os.environ['API_BOILERPLATE_DB_ENV_MYSQL_PASSWORD'],
    addr=os.environ['API_BOILERPLATE_DB_PORT_3306_TCP_ADDR'],
    port=os.environ['API_BOILERPLATE_DB_PORT_3306_TCP_PORT'],
    db_name=os.environ['API_BOILERPLATE_DB_ENV_MYSQL_DATABASE'],
)
