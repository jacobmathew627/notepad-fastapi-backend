# Configuration Setup Guide

## Quick Start

1. **Copy the example environment file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Generate a secure SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Edit `.env` and add your SECRET_KEY:**
   ```
   SECRET_KEY=your-generated-secret-key-here
   ```

4. **Optional: Customize other settings:**
   - `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT token expiration (default: 30)
   - `DATABASE_URL` - Database connection string (default: SQLite)
   - `CORS_ORIGINS` - Allowed frontend origins (comma-separated)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | **Yes** | None | JWT signing key (generate securely!) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | 30 | Token expiration time |
| `DATABASE_URL` | No | `sqlite:///mydatabase.db` | Database connection |
| `CORS_ORIGINS` | No | `http://localhost:5173,http://127.0.0.1:5173` | Allowed origins |
| `ENV` | No | `development` | Environment name |
| `HF_API_TOKEN` | No | None | Hugging Face API token for LLM parsing (optional) |

## Security Notes

- **NEVER commit `.env` to version control**
- Use strong, randomly generated SECRET_KEY in production
- Different environments should have different SECRET_KEY values

