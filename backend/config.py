import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# SECURITY CONFIGURATION
# ============================================
# SECRET_KEY: Used for JWT token signing
# ⚠️ CRITICAL: Never commit this to version control
# Generate a new one with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production-use-env-var")

# JWT Algorithm (rarely changes)
ALGORITHM = "HS256"

# Token expiration time in minutes
# Default: 30 minutes (can be overridden via env var)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# ============================================
# DATABASE CONFIGURATION
# ============================================
# Database URL - defaults to SQLite for development
# For production, use: postgresql://user:pass@localhost/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///mydatabase.db")

# ============================================
# CORS CONFIGURATION
# ============================================
# Allowed origins for CORS (comma-separated)
# Default: localhost:5173 (Vite dev server)
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
).split(",")

# ============================================
# APPLICATION ENVIRONMENT
# ============================================
ENV = os.getenv("ENV", "development")

# ============================================
# PASSWORD VALIDATION (Business Rules - Constants)
# ============================================
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 72

# ============================================
# AI/LLM CONFIGURATION (Hugging Face)
# ============================================
# Hugging Face Inference API (OpenAI Compatible)
# Get a key at https://huggingface.co/settings/tokens
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://router.huggingface.co/v1/")
AI_MODEL = os.getenv("AI_MODEL", "meta-llama/Llama-3.1-8B-Instruct")

# Hugging Face Token (Used for legacy fallback or specific HF tools)
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
