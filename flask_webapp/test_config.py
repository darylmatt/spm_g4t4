class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://g4t4:password@spm-g4t4-sbrp.cybxkypjkirc.ap-southeast-2.rds.amazonaws.com:3306/sbrp_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
