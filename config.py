"""
Configuration file for necessary variables
"""



class Config:
    """"Development configuration class."""
    SECRET_KEY = 'asdmnc5b4734-+*23'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    # need this for some weird reason I cannot remember
    @staticmethod
    def init_app():
        pass