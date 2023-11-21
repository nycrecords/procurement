class Config(object):
    SQLALCHEMY_DATABASE_URI = ("postgresql://leonardolopez2003:EYEr1DEaXAke4byjFuUo39BegCzby9Nw"
                               "@dpg-cicraodph6eoptg2df6g-a.oregon-postgres.render.com/procurement_db_wahr"
                               "?sslmode=require&sslcert=/path_to_cert&sslkey=/path_to_key&sslrootcert=/path_to_ca")
    # set this to False to silence the warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
