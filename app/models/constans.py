from fastapi.security import APIKeyHeader
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)
api_key = 'altooro'
users_table = 'users'