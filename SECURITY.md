# Security Guidelines

## API Key Management

### ✅ Secure Practices
- All API keys are managed through environment variables
- No hardcoded credentials in source code
- `.secure/` directory for local development (git-ignored)
- Production uses platform environment variables

### 🔒 Local Development
1. Copy the example environment file:
   ```bash
   cp .env.example .secure/.env
   ```
2. Edit `.secure/.env` with your actual API keys
3. Load environment variables from secure location

### 🚀 Production Deployment
- Set environment variables directly on your hosting platform
- Never commit actual API keys to version control
- Use platform-specific secret management

### 🛡️ Security Features
- JWT authentication with secure tokens
- bcrypt password hashing
- OAuth state validation
- CORS protection
- Input validation and sanitization

## Reporting Security Issues
If you discover a security vulnerability, please email: security@yourproject.com