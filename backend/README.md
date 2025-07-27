# Cloud Optimization Dashboard Backend

This document provides instructions for setting up and running the backend of the Cloud Optimization Dashboard project, which is built using FastAPI.

## Prerequisites

- Python 3.7 or higher
- PostgreSQL database
- pip (Python package installer)

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd cloud-optimization-dashboard/backend
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables. Create a `.env` file in the `backend` directory with the following content:

   ```
   DATABASE_URL=postgresql://<username>:<password>@localhost/<database_name>
   ```

   Replace `<username>`, `<password>`, and `<database_name>` with your PostgreSQL credentials.

## Running the Application

1. Start the FastAPI application:

   ```
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Directory Structure

- `app/`: Contains the main application code.
  - `api/`: Defines the API endpoints.
  - `core/`: Contains configuration settings.
  - `models/`: Defines the database models.
  - `schemas/`: Contains Pydantic schemas for data validation.
  - `services/`: Implements business logic for optimization.
  - `main.py`: Entry point for the FastAPI application.
  
## API Endpoints

- `GET /resources`: Fetch all resources.
- `POST /optimize`: Apply optimization rules to resources.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.