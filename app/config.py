import os

class Config:
    SECRET_KEY = 'my-super-secret-hardcoded-key-123'
    
    # This automatically puts the DB file in your 'instance' folder
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Go up one level (..) to root, then into instance/
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "../instance/moodflix.db")}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

