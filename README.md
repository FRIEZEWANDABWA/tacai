# 🚀 JACAI Pro - AI Social Media Automation Platform

**Enterprise-grade AI-powered social media content generation and automation system**

Built with **FastAPI** and **Python** for production deployment, powered by **Gemini AI** and **OpenAI** for intelligent content generation.

## ✨ Features

### 🤖 AI-Powered Content Generation
- **Multi-AI Support** - Gemini Pro, OpenAI GPT-3.5/4
- **Platform-Specific Content** - Instagram, Twitter, LinkedIn, Facebook, TikTok
- **Multiple Styles** - Professional, Casual, Creative, Motivational, Humorous
- **Smart Fallbacks** - Automatic failover between AI providers

### 🔐 Enterprise Security
- **User Authentication** - JWT-based secure login system
- **Role-Based Access** - Admin, User, Viewer permissions
- **OAuth Integration** - Secure social media account linking
- **Rate Limiting** - API abuse prevention

### 🔗 Social Media Integration
- **Multi-Platform Posting** - Bulk posting to all connected accounts
- **Account Management** - Link/unlink social media accounts
- **Connection Testing** - Validate account credentials
- **Platform Guidelines** - Automatic content formatting

### ⏰ Automation & Scheduling
- **Content Scheduling** - Plan posts for optimal times
- **Recurring Posts** - Automated content generation
- **n8n Integration** - Workflow automation support
- **Batch Processing** - Handle multiple posts efficiently

### 📊 Analytics & Management
- **Post History** - Track all generated content
- **Performance Metrics** - Monitor posting success rates
- **User Management** - Multi-user support
- **API Monitoring** - Health checks and status monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git
- Virtual environment (recommended)

### Installation
```bash
# Clone repository
git clone https://github.com/FRIEZEWANDABWA/tacai.git
cd tacai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Run application
python enhanced_app.py
```

**Access at:** `http://localhost:8080`

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t jacai .
docker run -p 8080:8080 --env-file .env jacai
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# AI API Keys
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key

# Social Media APIs
INSTAGRAM_ACCESS_TOKEN=your-instagram-token
TWITTER_API_KEY=your-twitter-api-key
LINKEDIN_ACCESS_TOKEN=your-linkedin-token

# Security
SECRET_KEY=your-super-secret-key

# Server
PORT=8080
HOST=0.0.0.0
```

### Social Media Setup

#### Instagram Business API
1. Create Facebook Developer App
2. Add Instagram Basic Display product
3. Configure OAuth redirect URI
4. Generate long-lived access token

#### Twitter API v2
1. Apply for Twitter Developer account
2. Create project and app
3. Enable OAuth 2.0 with write permissions
4. Generate API keys and tokens

#### LinkedIn API
1. Create LinkedIn Developer app
2. Request Marketing Developer Platform access
3. Configure OAuth redirect URI
4. Get w_member_social permission

## 🎯 Usage

### Web Interface
1. **Register/Login** - Create account or sign in
2. **Link Accounts** - Connect social media accounts via OAuth or manual tokens
3. **Generate Content** - Create AI-powered posts for multiple platforms
4. **Schedule Posts** - Plan content for optimal posting times
5. **Monitor Performance** - Track posting success and analytics

### API Endpoints

#### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/health` - System health check

#### Content Generation
- `POST /api/generate` - Generate content for platforms
- `GET /api/posts` - Get user's post history
- `POST /api/n8n/generate` - n8n automation endpoint

#### Social Media Management
- `POST /api/link-social-account` - Link social media account
- `GET /api/social-accounts` - Get linked accounts
- `DELETE /api/social-accounts/{platform}` - Unlink account
- `GET /api/test-social-connections` - Test account connections

#### Scheduling
- `POST /api/schedule-post` - Schedule future post
- `GET /api/scheduled-posts` - Get scheduled posts
- `POST /api/automation-rule` - Create automation rule

### n8n Integration

JACAI provides dedicated endpoints for n8n workflow automation:

```json
{
  "method": "POST",
  "url": "http://your-domain:8080/api/n8n/generate",
  "body": {
    "topic": "motivation Monday",
    "platforms": ["instagram", "twitter", "linkedin"],
    "style": "motivational",
    "auto_post": true
  }
}
```

## 🏗️ Architecture

```
JACAI Pro Architecture
├── FastAPI Backend
│   ├── Authentication & Authorization
│   ├── AI Service Integration
│   ├── Social Media APIs
│   └── Database Management
├── Frontend (HTML/CSS/JS)
│   ├── User Dashboard
│   ├── Account Linking
│   └── Content Management
├── Database (SQLite/PostgreSQL)
│   ├── Users & Authentication
│   ├── Social Accounts
│   ├── Generated Content
│   └── Scheduling Data
└── External Integrations
    ├── AI APIs (Gemini, OpenAI)
    ├── Social Media APIs
    └── n8n Workflows
```

## 🌐 Deployment

### Railway (Recommended)
1. Fork this repository
2. Connect Railway to your GitHub
3. Deploy with automatic builds
4. Configure environment variables

### VPS Deployment
```bash
# Clone on server
git clone https://github.com/FRIEZEWANDABWA/tacai.git
cd tacai

# Setup production environment
pip install -r requirements.txt
cp .env.example .env
# Configure production values

# Run with process manager
pm2 start enhanced_app.py --name jacai

# Or use systemd service
sudo systemctl enable jacai
sudo systemctl start jacai
```

### Docker Production
```bash
# Production docker-compose
docker-compose -f docker-compose.prod.yml up -d

# With reverse proxy (nginx)
docker-compose -f docker-compose.nginx.yml up -d
```

## 📊 Performance & Scaling

- **Response Time:** < 500ms for content generation
- **Throughput:** 100+ concurrent users
- **Memory Usage:** ~200MB base, scales with users
- **Database:** SQLite for development, PostgreSQL for production
- **Caching:** Redis support for session management
- **Load Balancing:** Ready for horizontal scaling

## 🔒 Security Features

- **JWT Authentication** with secure token management
- **Password Hashing** using bcrypt
- **Rate Limiting** to prevent API abuse
- **Input Validation** and sanitization
- **CORS Configuration** for secure cross-origin requests
- **Environment Variables** for sensitive data
- **OAuth State Validation** for secure social media linking

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Load testing
locust -f tests/load_test.py
```

## 📈 Roadmap

### Phase 1 (Current)
- [x] Multi-user authentication system
- [x] Social media account linking
- [x] AI content generation
- [x] Basic scheduling
- [x] n8n integration

### Phase 2 (Next)
- [ ] Advanced analytics dashboard
- [ ] Image generation integration
- [ ] Team collaboration features
- [ ] Advanced scheduling with timezone support
- [ ] Content templates and campaigns

### Phase 3 (Future)
- [ ] Mobile app (React Native)
- [ ] Advanced AI training on user data
- [ ] Multi-language support
- [ ] Enterprise SSO integration
- [ ] Advanced reporting and insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run development server with auto-reload
uvicorn enhanced_app:app --reload --port 8080
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/FRIEZEWANDABWA/tacai/issues)
- **Discussions:** [GitHub Discussions](https://github.com/FRIEZEWANDABWA/tacai/discussions)
- **Email:** support@jacai.pro

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **OpenAI** and **Google** for AI API access
- **Social Media Platforms** for their APIs
- **Open Source Community** for inspiration and tools

---

**Built with ❤️ for the social media automation community**

*Empowering creators and businesses with AI-driven social media management*