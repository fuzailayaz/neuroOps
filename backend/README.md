# NeuroOps - Autonomous Multi-Agent AI Platform

NeuroOps is a self-hosted, open-source platform for building and managing autonomous AI agents that can collaborate to solve complex tasks.

## Features

- **Multi-Agent System**: Create and manage multiple AI agents with specialized roles
- **Knowledge Graph**: Store and retrieve information in a structured knowledge graph
- **Real-time Chat**: Interact with agents through a real-time chat interface
- **Document Processing**: Ingest and process various document formats (PDF, DOCX, TXT, etc.)
- **Hybrid Search**: Combine vector similarity search with keyword search for better results
- **Fine-tuning**: Fine-tune models on your own data
- **API-First**: Fully-featured REST API for integration with other systems

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js 16+ (for frontend development)

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/neuroops.git
   cd neuroops/backend
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start the services**
   ```bash
   docker-compose up -d --build
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a superuser (admin) account**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   docker-compose exec web python manage.py runserver 0.0.0.0:8000
   ```

7. **Access the admin interface**
   - URL: http://localhost:8000/admin/
   - Use the superuser credentials you created

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Project Structure

```
backend/
├── agents/               # Agent management and orchestration
├── chat/                 # Real-time chat functionality
├── config/               # Django project settings
├── knowledge/            # Knowledge management and document processing
├── static/               # Static files (CSS, JavaScript, etc.)
├── media/                # User-uploaded files
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Development

### Setting up the development environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running tests

```bash
pytest
```

### Code style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run all code style checks:
```bash
black .
isort .
flake8
mypy .
```

## Deployment

For production deployment, please refer to the [deployment guide](DEPLOYMENT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) to get started.
