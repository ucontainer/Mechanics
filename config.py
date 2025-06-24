class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/mechanics_db'
    DEBUG = True   #Causes flask to auto-update whenever there are changes.
    
class TestingConfig:
    pass

class ProductionConfig:
    pass