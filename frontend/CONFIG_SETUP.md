# Frontend Configuration Setup

## Quick Start

1. **Create `.env` file in the `frontend` directory:**
   ```bash
   cd frontend
   touch .env
   ```

2. **Add your API URL:**
   ```
   VITE_API_URL=http://127.0.0.1:8000
   ```

3. **For production, update to your backend URL:**
   ```
   VITE_API_URL=https://api.yourdomain.com
   ```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | No | `http://127.0.0.1:8000` | Backend API base URL |

## Notes

- Vite requires the `VITE_` prefix for environment variables
- Changes to `.env` require restarting the dev server
- `.env` should be in `.gitignore` (never commit secrets)

