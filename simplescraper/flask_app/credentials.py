import os

# MONGO_USERNAME = os.getenv('MONGO_USERNAME')
# MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
# MONGO_CLUSTER = os.getenv('MONGO_CLUSTER')
# MONGO_DATABASE = os.getenv('MONGO_DATABASE')
# PORT = os.getenv('POSTGRES_PORT')
# SECRET_KEY = config('SECRET_KEY')

MONGO_USERNAME = 'simpleapi'
MONGO_PASSWORD = 'eXECr0Ky6gpcrchp'
MONGO_CLUSTER = 'simpleapicluster.rhvxe0i.mongodb.net/'
MONGO_DATABASE = 'simpleapi_db'

MONGO_URI = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@' \
                    f'{MONGO_CLUSTER}' \
                    f'?retryWrites=true&w=majority'

SECRET_KEY = os.urandom(24)

# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')

AWS_BUCKET_NAME = 'simplefilesapi'
AWS_ACCESS_KEY_ID = 'AKIA4WYZ6P225ZKCFWGU'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION_NAME = 'us-east-2'
