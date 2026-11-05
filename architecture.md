# System Architecture — Smart Travel Planner

## 1. Architecture Overview

Smart Travel Planner uses a client-server architecture with separate frontend, backend, AI, and database layers.

The system is designed to be modular, scalable, and easy to maintain.

## 2. Technology Stack

| Layer | Technology | Responsibility |
|---|---|---|
| Frontend | React + TypeScript | User interface |
| Styling | Tailwind CSS | Responsive design |
| Backend | Python + FastAPI | Business logic and APIs |
| AI Service | OpenAI API | Travel itinerary generation |
| Database | PostgreSQL | Persistent data storage |
| ORM | SQLAlchemy | Database operations |
| Version Control | Git + GitHub | Source code management |

## 3. System Components

### Frontend

Responsibilities:
- Display the landing page.
- Collect travel preferences.
- Send requests to the backend.
- Display AI-generated itineraries.
- Show estimated travel budgets.

### Backend

Responsibilities:
- Receive frontend requests.
- Validate user input.
- Process travel planning requests.
- Communicate with the AI service.
- Calculate estimated travel expenses.
- Manage database operations.

### AI Service

Responsibilities:
- Generate personalized travel itineraries.
- Recommend daily activities.
- Suggest travel experiences.
- Provide budget optimization suggestions.

### Database

The database will store:
- User accounts.
- Travel preferences.
- Saved trips.
- Generated itineraries.
- Travel history.

## 4. Main User Flow

1. User opens the platform.
2. User selects a destination.
3. User enters travel dates and budget.
4. Frontend sends the information to the backend.
5. Backend validates the information.
6. Backend requests a personalized itinerary from the AI service.
7. AI generates the travel plan.
8. Backend returns the result.
9. Frontend displays the itinerary and estimated expenses.

## 5. API Design

Initial API endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | API status |
| POST | /api/v1/trips/plan | Generate travel plan |
| POST | /api/v1/budget/calculate | Calculate estimated budget |
| GET | /api/v1/destinations | Get destination information |

## 6. Security

- Store API keys in environment variables.
- Never expose secret keys in frontend code.
- Validate incoming user data.
- Use secure authentication when user accounts are introduced.
- Protect database credentials.

## 7. Deployment Architecture

- Frontend: Vercel
- Backend: Render
- Database: Managed PostgreSQL
- Source code: GitHub

## 8. Future Scalability

The architecture will support future integrations such as:
- Flight search APIs.
- Hotel booking services.
- Weather APIs.
- Interactive maps.
- Payment gateways.
- Travel agency integrations.

## 9. Architecture Principle

Keep frontend, backend, AI services, and database responsibilities separate to make the platform maintainable and scalable.
