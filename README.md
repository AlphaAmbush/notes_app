# Notes app

## Description

This is a full-stack web application built using Python and React. It allows users to manage notes, including creating, and deleting them. This project serves as a learning exercise for Python FastAPI.

## Features

- User authentication: Users can register, login, and logout(use /logout and /register to navigate).
- CRUD operations on notes: Users can create, read, and delete their notes.
- Protected routes: Certain routes are protected and require authentication.
- OAuth2 with JWT token: Authentication is implemented using OAuth2 and JWT tokens for secure communication.

## Technologies Used

### Backend
- Python (>= 3.10)
- FastAPI
- SQLAlchemy
- Uvicorn
- Other dependencies listed in requirements.txt

### Frontend
- React
- React Router
- Other dependencies managed by npm

## Setup

### Backend
1. Install Python (>= 3.10).
2. Install the required dependencies using `pip install -r requirements.txt` from root folder.
3. Run the backend server using `uvicorn backend.main:app` from root folder.

### Frontend
1. Navigate to the `frontend` directory.
2. Install npm dependencies using `npm install`.
3. Run the frontend server using `npm run dev`.

## Usage

1. Register a new account or login with existing credentials.
2. Create, edit, or delete notes as needed.
3. Logout when finished.

## Folder Structure

- `backend`: Contains the backend Python code.
- `frontend`: Contains the frontend React code.
- `requirements.txt`: Lists the Python dependencies.
- Other project files and folders.

