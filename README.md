# Event Manager
## Getting Started
- Clone the repository:
   ```bash
   git clone https://github.com/pedro-coelho-dr/event-manager.git
   ```
   ```bash
   cd event-manager
   ```

- Create a virtual environment:   
  
    Linux:
   ```bash
   python3 -m venv venv
   ```
   ```bash
   source venv/bin/activate
   ```
    Windows:
   ```bash
   python -m venv venv
   ```
   ```bash
   .\venv\Scripts\activate
   ```
   If ExecutionPolicy is restricted:
   ```bash
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

- Install dependecies:
   ```bash
   pip install -r requirements.txt
   ```

## Docker



## Database Entities

### 1. Users

| Column     | Type             | Description                                                      |
|------------|------------------|------------------------------------------------------------------|
| id         | SERIAL PRIMARY KEY | Unique identifier                                |
| username   | VARCHAR(50) UNIQUE | login credential                 |
| role       | VARCHAR(10) CHECK (role IN ('User', 'Producer')) NOT NULL | 'User' or 'Producer' |

### 2. Categories

| Column     | Type               | Description                        |
|------------|--------------------|------------------------------------|
| id         | SERIAL PRIMARY KEY | Unique identifier |
| name       | VARCHAR(50) UNIQUE | Name of the category |

### 3. Events

| Column       | Type               | Description                                                          |
|--------------|--------------------|----------------------------------------------------------------------|
| id           | SERIAL PRIMARY KEY | Unique identifier                                     |
| producer_id  | INT REFERENCES users(id) | References the producer who created the event |
| category_id  | INT REFERENCES categories(id) | References the event’s category                                  |
| name         | VARCHAR(100)       | Name of the event.                                                   |
| date         | DATE               | Date the event                                        |

### 4. Event_Attendees

| Column     | Type               | Description                                                      |
|------------|--------------------|------------------------------------------------------------------|
| event_id   | INT REFERENCES events(id) ON DELETE CASCADE | References the event being attended                        |
| user_id    | INT REFERENCES users(id) ON DELETE CASCADE | References the user attending the event                  |
| PRIMARY KEY | (event_id, user_id) | Primary key|


## Database Schema

```mermaid
erDiagram
    USERS {
        INT id PK
        VARCHAR username
        VARCHAR role
    }
    CATEGORIES {
        INT id PK
        VARCHAR name
    }
    EVENTS {
        INT id PK
        INT producer_id FK
        INT category_id FK
        VARCHAR name
        DATE date
    }
    EVENT_ATTENDEES {
        INT event_id FK
        INT user_id FK
    }

    USERS ||--o{ EVENTS : "creates"
    USERS ||--o{ EVENT_ATTENDEES : "attends"
    CATEGORIES ||--o{ EVENTS : "categorizes"
    EVENTS ||--o{ EVENT_ATTENDEES : "includes"
