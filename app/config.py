import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

KAKAO_APP_KEY = os.getenv("KAKAO_APP_KEY")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
