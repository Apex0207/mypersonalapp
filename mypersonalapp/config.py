class Config(object):
    DATABASE_URI="some random parameters"
    MERCHANT_ID="SAMPLE"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/personal"
    MERCHANT_ID="t98765@0"
class TestConfig(Config):
    DATABASE="test connection parameters"