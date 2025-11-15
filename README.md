# TrustMess

**TrustMess** is a secure, privacy-focused real-time messaging application designed for confidential communication. The platform prioritizes user privacy by not storing any message history on the server, ensuring that conversations remain private and ephemeral.

## Overview

TrustMess is a full-stack web application that enables users to communicate in real-time through WebSocket connections. The project consists of a React-based frontend and a FastAPI backend, deployed as containerized services for scalability and reliability.

## Key Features

### Core Functionality

- **Real-Time Messaging**: Instant message delivery using WebSocket protocol for low-latency communication
- **User Authentication**: Secure JWT-based authentication system with password hashing
- **Privacy-First Architecture**: Messages are transmitted in real-time without server-side storage
- **User Management**: Registration, login, and user profile management
- **Contact List**: Browse and select users for private conversations
- **Responsive UI**: Modern, mobile-friendly interface built with React

### Security Features

- JWT (JSON Web Token) authentication
- Bcrypt password hashing
- Protected API routes with authentication middleware
- Secure WebSocket connections

### Technical Highlights

- **No Message Persistence**: Messages are never stored in the database, ensuring complete privacy
- **Real-Time Communication**: WebSocket-based architecture for instant message delivery
- **Containerized Deployment**: Docker-based infrastructure for consistent environments

## Technology Stack

### Frontend

- **Framework**: React 19
- **Build Tool**: Vite
- **Routing**: React Router DOM v7
- **HTTP Client**: Axios
- **Form Management**: Formik
- **Styling**: SCSS/Sass
- **WebSocket**: Native WebSocket API
- **Date Utilities**: date-fns

### Backend

- **Framework**: FastAPI (Python)
- **WebSocket**: Native FastAPI WebSocket support
- **Database**: PostgreSQL 15
- **Authentication**: JWT with PyJWT
- **Password Hashing**: Bcrypt (passlib)
- **Database Driver**: psycopg2
- **ASGI Server**: Uvicorn

### Infrastructure

- **Containerization**: Docker, Docker Compose
- **Web Server**: Nginx (reverse proxy)
- **Hosting**: Google Cloud Platform (GCP) Virtual Machine
- **CI/CD**: GitHub Actions

## Architecture

The application follows a three-tier architecture:

1. **Frontend Layer**: React SPA served by Nginx
2. **Backend Layer**: FastAPI application handling REST API and WebSocket connections
3. **Database Layer**: PostgreSQL for user data storage (no messages)

### Communication Flow

- HTTP/HTTPS requests for authentication and user management
- WebSocket connections for real-time messaging
- Nginx reverse proxy routes requests to appropriate backend services

## Project Structure

```
trustmess-frontend/
├── src/
│   ├── api/              # API request handlers
│   ├── components/       # React components
│   ├── contexts/         # React contexts (Auth, WebSocket, Theme)
│   ├── pages/            # Page components
│   ├── scss/             # Stylesheets
│   └── config/           # Configuration files
├── public/               # Static assets
├── conf/                 # Build configuration
├── dockerfile            # Frontend Docker configuration
├── nginx.conf            # Nginx configuration
└── .github/workflows/    # CI/CD workflows

trustmess-backend/
├── src/
│   ├── db/               # Database models and queries
│   ├── routes/           # API route handlers
│   ├── schemas/          # Pydantic schemas
│   ├── secure/           # Authentication & security
│   └── websocket/        # WebSocket manager
├── Dockerfile            # Backend Docker configuration
└── main.py               # Application entry point
```

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens for stateless authentication
- No message storage on server
- Protected routes require authentication
- Environment variables for sensitive configuration

## Privacy Features

**No Message Storage**: The core privacy feature of TrustMess is that no messages are stored in the database. Messages are only:

- Transmitted in real-time through WebSocket connections
- Kept in client-side memory during active sessions
- Lost when the browser is closed or refreshed

This ensures that conversations are truly ephemeral and cannot be retrieved or accessed after the session ends.

## Future Enhancements

- End-to-end encryption for messages
- File sharing capabilities
- Group messaging support
- Message status indicators (sent/delivered/read)
- Push notifications
- Mobile applications (React Native)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this software for any purpose, including commercial applications.

## Author

**Stanislav Kucherenko** - Full Stack Developer

## Support

For issues or questions, please contact the development team.

---

**Note**: TrustMess prioritizes privacy and security. No conversation history is retained on the server, ensuring that your communications remain confidential.
