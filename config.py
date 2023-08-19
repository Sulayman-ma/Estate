"""
Configuration file for necessary variables
"""



class Config:
    """"Development configuration class."""
    SECRET_KEY = 'asdmnc5b4734-+*23'
    # CSRF_TOKEN = 'fmn3c7(#&(3misaER'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:%Prometheus123@localhost/estate'
    # need this for some weird reason I cannot remember
    @staticmethod
    def init_app():
        pass