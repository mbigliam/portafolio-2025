# 🔐 Local-First IA Security Gateway

**Secure AI Integration with Local LLM Processing**

A Python FastAPI-based security gateway that manages communication with AI services while maintaining strict data privacy and compliance standards. All processing stays local using Ollama, with comprehensive traffic control and audit logging.

## 📋 Project Overview

### Problem Statement
Organizations increasingly share sensitive data with AI services without realizing the security implications. This gateway provides a secure, compliant layer that:
- Processes all AI requests locally (no external API calls by default)
- Detects and prevents data exfiltration attempts
- Maintains comprehensive audit trails for compliance
- Enforces rate limiting and access control
- Classifies data sensitivity automatically

### Architecture

```
┌─────────────────────────────────────────┐
│         Client Applications             │
├─────────────────────────────────────────┤
│   FastAPI Security Gateway (Port 8000)  │
├────────────┬──────────────┬─────────────┤
│ Traffic    │ Compliance   │ Security    │
│ Control    │ Logging      │ Module      │
├────────────┴──────────────┴─────────────┤
│    Ollama Local LLM (Port 11434)        │
├─────────────────────────────────────────┤
│   Models: LLaMA 2, Mistral 7B, etc.     │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Ollama running locally (https://ollama.ai)
- At least one LLM model installed in Ollama (e.g., `ollama pull llama2`)

### Installation

1. **Clone and setup**
```bash
cd ia-security-gateway
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start Ollama** (in another terminal)
```bash
# Ensure Ollama is running on localhost:11434
ollama serve
```

3. **Run the gateway**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## 📚 API Endpoints

### 1. Generate Text
**POST** `/api/generate`

Generate text using local LLM with security controls.

**Request:**
```json
{
  "prompt": "Explain the importance of data privacy",
  "temperature": 0.7
}
```

**Response:**
```json
{
  "success": true,
  "response": "Data privacy is crucial because...",
  "model_used": "llama2",
  "generation_time_ms": 1234.56,
  "data_sensitivity": "public",
  "timestamp": "2024-09-13T10:30:00"
}
```

### 2. Chat Interaction
**POST** `/api/chat`

Multi-turn conversation with context tracking.

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "What is data privacy?"},
    {"role": "assistant", "content": "Data privacy refers to..."},
    {"role": "user", "content": "How can I protect my data?"}
  ],
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "success": true,
  "response": "You can protect your data by...",
  "session_id": "session_123",
  "messages_processed": 3,
  "timestamp": "2024-09-13T10:30:00"
}
```

### 3. Compliance Report
**GET** `/api/compliance`

Get comprehensive compliance and audit status.

**Response:**
```json
{
  "report_date": "2024-09-13T10:30:00",
  "gdpr_enabled": true,
  "hipaa_enabled": true,
  "pci_dss_enabled": true,
  "data_retention_days": 90,
  "log_sensitive_data": false,
  "audit_entries": 1250,
  "status": "compliant",
  "allowed_requests": 5000,
  "blocked_requests": 12,
  "active_clients": 42
}
```

### 4. Gateway Status
**GET** `/api/status`

Check operational status and Ollama availability.

**Response:**
```json
{
  "status": "operational",
  "ollama_available": true,
  "version": "1.0.0",
  "timestamp": "2024-09-13T10:30:00",
  "uptime_seconds": 3600.5
}
```

### 5. Traffic Statistics
**GET** `/api/traffic-stats`

Monitor traffic control metrics.

**Response:**
```json
{
  "allowed_requests": 5000,
  "blocked_requests": 12,
  "active_clients": 42,
  "block_rate_percent": 0.24,
  "timestamp": "2024-09-13T10:30:00"
}
```

## 🔒 Security Features

### Data Sensitivity Classification
Automatically detects and classifies sensitive data patterns:
- **Critical**: SSN, Credit Cards, Passport Numbers, DNI
- **Sensitive**: API Keys, Tokens, Passwords
- **Internal**: Company-specific information
- **Public**: General information

### Traffic Control
- **Rate Limiting**: Configurable limits per client (default: 100 requests/60s)
- **Payload Size Limiting**: Prevents exfiltration of large data dumps (>1MB)
- **Pattern Detection**: Identifies suspicious combinations of sensitive patterns

### Compliance Logging
- **GDPR Compliance**: Data retention policies, audit trails
- **HIPAA Compliance**: Secure logging without sensitive data storage
- **PCI-DSS Compliance**: Payment data protection measures

### Audit Trail
Every request is logged with:
- Timestamp and client identification
- HTTP method, path, status code
- Processing time and performance metrics
- Data classification results
- Security events and violations

## ⚙️ Configuration

### Environment Variables
Create a `.env` file (optional):
```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_TIMEOUT=60

# Gemini (fallback, optional)
GEMINI_API_KEY=your-key-here

# Traffic Control
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
MAX_PAYLOAD_SIZE=10485760

# Compliance
GDPR_ENABLED=True
HIPAA_ENABLED=True
PCI_DSS_ENABLED=True
LOG_SENSITIVE_DATA=False
DATA_RETENTION_DAYS=90
```

### Configuration File
Edit `app/core/config.py` to modify default settings:
```python
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60
```

## 📁 Project Structure

```
ia-security-gateway/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                  # Git configuration
└── app/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py           # Settings and configuration
    │   └── security.py         # JWT, sanitization, classification
    ├── services/
    │   ├── __init__.py
    │   ├── ollama_service.py   # Local LLM integration
    │   ├── traffic_control.py  # Rate limiting & detection
    │   └── compliance.py       # Audit logging & compliance
    ├── models/
    │   ├── __init__.py
    │   └── schemas.py          # Pydantic data models
    └── api/
        ├── __init__.py
        └── routes.py           # API endpoints
```

## 🛠️ Development

### Adding New Models
1. Pull model to Ollama:
```bash
ollama pull mistral
```

2. Update configuration:
```python
# app/core/config.py
OLLAMA_MODEL = "mistral"
```

### Running Tests
```bash
pytest tests/ -v
```

### Monitoring Logs
Check compliance audit trail:
```bash
tail -f logs/compliance.log
```

## 📊 Key Metrics

- **Requests Processed**: Total allowed requests
- **Block Rate**: Percentage of blocked requests
- **Active Clients**: Concurrent client connections
- **Generation Time**: Average LLM response time
- **Audit Entries**: Total compliance log entries

## 🔄 Compliance Reports

Generate comprehensive compliance reports:
```bash
curl http://localhost:8000/api/compliance | jq
```

Export audit trail for review:
```bash
# Logs are stored in logs/compliance.log (JSON format)
cat logs/compliance.log | jq '.event == "ERROR"' | wc -l
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Production Considerations
1. Use environment variables for sensitive config
2. Set `DEBUG=False` in production
3. Configure appropriate CORS origins
4. Implement authentication/authorization
5. Set up log aggregation
6. Use HTTPS/TLS
7. Monitor compliance metrics continuously

## 📈 Performance

- **Average Response Time**: ~500-2000ms (depends on model and prompt length)
- **Concurrent Connections**: 100+ (configurable)
- **Memory Usage**: ~2-4GB (with LLM models)
- **Disk Usage**: 5-10GB (varies by models installed)

## 🔧 Troubleshooting

### Ollama Connection Failed
```
Error: Failed to connect to Ollama
Solution: Ensure Ollama is running and accessible at OLLAMA_URL
```

### Rate Limit Exceeded
```
Status Code: 429
Solution: Adjust RATE_LIMIT_REQUESTS or RATE_LIMIT_WINDOW
```

### Data Sensitivity Errors
```
Status Code: 400 - Request contains sensitive data patterns
Solution: Remove sensitive information or adjust classification rules
```

## 📝 Technical Skills Applied

✅ **Backend Development**: FastAPI, Python async/await, RESTful API design
✅ **Security**: Data classification, rate limiting, input sanitization, JWT authentication
✅ **Compliance**: GDPR/HIPAA/PCI-DSS standards, audit logging, data retention
✅ **Integration**: Ollama LLM integration, external API fallback mechanism
✅ **Architecture**: Microservices pattern, separation of concerns, middleware design
✅ **DevOps**: Environment configuration, Docker containerization
✅ **Data Processing**: Sensitivity detection, pattern matching, payload validation

## 🎯 Portfolio Justification

This project demonstrates:
1. **Enterprise Architecture**: Multi-layered security with compliance frameworks
2. **Real-World Problem Solving**: Addresses actual data privacy concerns
3. **Production-Ready Code**: Error handling, logging, monitoring
4. **Security Best Practices**: Data classification, rate limiting, audit trails
5. **Full Stack Implementation**: From API design to database logging
6. **Scalability**: Modular design for easy expansion
7. **Documentation**: Comprehensive API docs and setup guides

## 📄 License

This project is provided as-is for educational and portfolio purposes.

## 👤 Author

**Mauricio Fernando Biglia**  
Email: mauriciobigliam@gmail.com

---

**Last Updated**: September 2024  
**Version**: 1.0.0
