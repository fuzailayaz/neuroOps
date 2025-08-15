# NeuroOps Project Architecture & Documentation

## Table of Contents
1. [Current Implementation](#current-implementation)
2. [Docker Setup](#docker-setup)
3. [Authentication Flow](#authentication-flow)
4. [Frontend Structure](#frontend-structure)
5. [Backend Services](#backend-services)
6. [UI/UX Implementation Plan](#uiux-implementation-plan)
7. [Future Enhancements](#future-enhancements)
8. [Rollback Procedures](#rollback-procedures)

---

## Current Implementation

### Authentication
- **Backend**: Django REST Framework with JWT
- **Frontend**: React with TypeScript
- **Endpoints**:
  - `/api/auth/token/` - Obtain JWT token
  - `/api/auth/refresh/` - Refresh JWT token
  - `/api/auth/register/` - User registration
  - `/api/auth/profile/` - User profile

### Database
- PostgreSQL
- Redis (for caching and session management)

### Search & AI
- Qdrant (vector database)
- Elasticsearch (full-text search)

### Monitoring
- Prometheus
- Grafana

---

## Docker Setup

### Services
1. **Backend**: Django application
   - Port: 8000
   - Dependencies: PostgreSQL, Redis

2. **Database**: PostgreSQL
   - Port: 5432
   - Volume: `postgres_data`

3. **Redis**: Caching and session store
   - Port: 6379

4. **Qdrant**: Vector database
   - Port: 6333
   - Volume: `qdrant_data`

5. **Elasticsearch**: Search engine
   - Port: 9200
   - Volume: `es_data`

6. **MinIO**: Object storage
   - Port: 9000
   - Volume: `minio_data`

7. **MLflow**: Experiment tracking
   - Port: 5000

8. **Prometheus**: Monitoring
   - Port: 9090

9. **Grafana**: Visualization
   - Port: 3000

### Network
- All services are connected to the `neuroops_network`
- Internal communication uses service names as hostnames

---

## Authentication Flow

### Current Implementation
1. User submits login credentials
2. Frontend sends request to `/api/auth/token/`
3. Backend validates credentials and returns JWT tokens
4. Frontend stores tokens in localStorage
5. Subsequent requests include token in Authorization header

### Future Considerations
- Implement token refresh mechanism
- Add social authentication (Google, GitHub)
- Implement password reset flow
- Add email verification

---

## Frontend Structure

### Key Directories
- `/src/components/` - Reusable UI components
- `/src/pages/` - Page components
- `/src/services/` - API service modules
- `/src/stores/` - State management
- `/src/lib/` - Utility functions and configurations

### Styling
- Mantine UI components
- Custom CSS modules
- Responsive design with mobile-first approach

---

## Backend Services

### Core Services
1. **Accounts**: User authentication and management
2. **Agents**: AI agent management
3. **Chat**: Real-time chat functionality
4. **Knowledge**: Document and knowledge management

### API Structure
- Base URL: `/api/`
- Versioning: `/api/v1/` for core services
- Authentication: JWT tokens

### Database Models
- User
- Agent
- Chat
- Document
- (Additional models to be documented)

---

## UI/UX Implementation Plan

### Sidebar Implementation
1. **Color Scheme**
   - Background: `#F8F8F8` (light), `#212121` (dark)
   - Text: `#666666` (inactive), `#4F46E5` (active)
   - Icons: 20-24px, consistent style

2. **Animations**
   - Smooth transitions for sidebar collapse/expand
   - Hover effects on navigation items
   - Page transitions

3. **Responsive Design**
   - Collapsible sidebar for mobile
   - Adaptive layouts
   - Touch-friendly elements

### Component Library
- Create reusable UI components
- Implement theme provider
- Add loading states and error boundaries

---

## Future Enhancements

### Short-term
1. Complete user profile management
2. Implement chat interface
3. Add document upload and management
4. Create agent management dashboard

### Long-term
1. Real-time collaboration features
2. Advanced analytics
3. Plugin system for extensibility
4. Mobile app

---

## Rollback Procedures

### Database Rollback
```bash
docker-compose exec db pg_dump -U postgres neuroops > backup_$(date +%Y%m%d).sql
```

### Code Rollback
```bash
git checkout <commit-hash>
docker-compose down
docker-compose up -d --build
```

### Configuration Backup
- `.env` files
- Docker Compose files
- Database dumps

---

## Troubleshooting

### Common Issues
1. **Port Conflicts**
   - Check running services: `lsof -i :<port>`
   - Update port in `.env` if needed

2. **Docker Issues**
   - Rebuild containers: `docker-compose up -d --build`
   - View logs: `docker-compose logs -f <service>`

3. **Database Migrations**
   ```bash
   docker-compose exec backend python manage.py makemigrations
   docker-compose exec backend python manage.py migrate
   ```

---

## Development Workflow

1. Make changes to the code
2. Test locally
3. Commit changes with descriptive messages
4. Push to feature branch
5. Create pull request
6. Review and merge to main

---

## Deployment

### Staging
- Automated CI/CD pipeline
- Separate environment variables
- Test database

### Production
- Zero-downtime deployment
- Database backups
- Monitoring and alerts

---

## Security Considerations

1. **Secrets Management**
   - Never commit `.env` files
   - Use environment variables for sensitive data
   - Rotate credentials regularly

2. **API Security**
   - Rate limiting
   - Input validation
   - CORS configuration

3. **Data Protection**
   - Encryption at rest and in transit
   - Regular backups
   - Access controls

---

## Performance Optimization

### Frontend
- Code splitting
- Lazy loading
- Image optimization

### Backend
- Database indexing
- Query optimization
- Caching strategy

---

## Monitoring and Logging

### Backend Logs
```bash
docker-compose logs -f backend
```

### Database Metrics
- Prometheus endpoint: `http://localhost:9090`
- Grafana dashboard: `http://localhost:3000`

### Error Tracking
- Sentry integration
- Log aggregation

---

## Testing Strategy

### Unit Tests
- Jest for frontend
- Pytest for backend

### Integration Tests
- API endpoint testing
- Database operations

### E2E Tests
- Cypress for UI flows

---

## Documentation

### API Documentation
- Swagger UI at `/api/docs/`
- Redoc at `/api/redoc/`

### Component Documentation
- Storybook setup planned
- Prop types and usage examples

### Development Guides
- Setup instructions
- Code style guide
- Contribution guidelines
