import os
from dotenv import load_dotenv

load_dotenv()

class APIConfig:
    BASE_URL_V1 = 'https://hackapi.hellozelf.com/backend/api/v1'
    API_KEY = os.getenv('API_KEY')
    MAX_PAGE_SIZE = 28
