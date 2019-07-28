from .base import  *

DEBUG = False
ALLOWED_HOSTS = ['typeidea.com']

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':'typeidea',
        'USER':'jge',
        'PASSWORD':'jge520',
        'HOST':'<ip>',
        'PORT':3306,
        # 'CONN_MAX_AGE':5*60,
        # 'OPTIONS':{'charset':'utf8mb4'}
    },
}

"""
---------------------------------------------
                配置缓存
--------------------------------------------
"""
'''
local-memory caching:默认本地内存缓存
'''
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION':'unique-snowflake',
    }
}
'''
file-system caching
'''
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION':'/var/tmp/django_cache',
    }
}
'''
database caching
$python manage.py createcachetable
'''
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.db.DatabaseCache',
        'LOCATION':'db_cache_table',
    },
}

'''
memcached:推荐，django内置支持
'''
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION':[
                '172.19.26.240:11211',
                '172.19.26.242:11211',
            ],
    }
}
'''
Redis caching
$pip install django-redis
$pip install hiredis #提升redis性能
'''
CACHES = {
    'default':{
        'BACKEND':'django_redis.cache.RedisCache',
        'LOCATION':REDIS_URL,
        'TIMEOUT':300,
        'OPTIONS':{
            'PASSWORD':'<>',
            'CLIENT_CLASS':'django_redis.client.DefaultClient',
            'PARSER_CLASS':'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS':'redis.connection.BlockingConnectionPool',
    }
}