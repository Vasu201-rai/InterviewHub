import os

if not os.environ.get('RENDER'):
    import pymysql
    pymysql.install_as_MySQLdb()