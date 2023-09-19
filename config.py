"""
Configuration file for necessary variables
"""



class Config:
    """"Development configuration class."""
    SECRET_KEY = 'asdmnc5b4734-+*23'
    # CSRF_TOKEN = 'fmn3c7(#&(3misaER'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:%Prometheus123@localhost/estate'
    API_KEY = 'sk_test_3cc377fb007fc4608e1c25f0e6810bf976c7af65'
    # need this for some weird reason I cannot remember
    @staticmethod
    def init_app():
        pass