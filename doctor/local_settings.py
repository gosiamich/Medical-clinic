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