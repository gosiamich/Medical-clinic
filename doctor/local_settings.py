# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'doctor_db',
        'HOST': 'localhost',
        'PASSWORD': 'coderslab',
        'USER': 'postgres',
        'PORT': 5432
    }
}


API_KEY = '6b268b37ccc6c82d7fa5e88f6498fcb0'