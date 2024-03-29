
from datetime import timedelta


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer","Token",),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}