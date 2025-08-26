class Config:
    SECRET_KEY = "supersecretsauce&*&$"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://ucontainer:PNtMEZvVnCDTBuKdlF6hZHxfywTkpTVy@dpg-d2ehlvqdbo4c738f3fgg-a.oregon-postgres.render.com/mechanic_postgre"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://ucontainer:PNtMEZvVnCDTBuKdlF6hZHxfywTkpTVy@dpg-d2ehlvqdbo4c738f3fgg-a.oregon-postgres.render.com/mechanic_postgre"