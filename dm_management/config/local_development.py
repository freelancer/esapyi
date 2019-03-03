import os

DEBUG = True

SQLALCHEMY_DB_URI = '{engine}://{user}:{pwd}@{addr}:{port}/{db_name}'.format(
    engine='mysql+pymysql',
    user=os.environ['DM_MANAGEMENT_DB_ENV_MYSQL_USER'],
    pwd=os.environ['DM_MANAGEMENT_DB_ENV_MYSQL_PASSWORD'],
    addr=os.environ['DM_MANAGEMENT_DB_PORT_3306_TCP_ADDR'],
    port=os.environ['DM_MANAGEMENT_DB_PORT_3306_TCP_PORT'],
    db_name=os.environ['DM_MANAGEMENT_DB_ENV_MYSQL_DATABASE'],
)
