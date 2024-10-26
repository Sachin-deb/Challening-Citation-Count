Citation Count Backend

This repository contains a FastAPI application that provides endpoints for fetching citation and publication data for professors. The backend utilizes the OpenAlex and Semantic Scholar APIs to gather data.
Features

    Fetch data for a list of predefined professors.
    Retrieve individual professor data based on their name.
    Support for CORS to allow requests from the frontend application.

Prerequisites

Before running the application, ensure you have the following installed on your system:

    Python 3.7 or later
    pip (Python package installer)

Installation

    Clone the repository:

    bash

git clone https://github.com/Sachin-deb/Challening-Citation-Count.git
cd Challening-Citation-Count

Create a virtual environment (optional but recommended):

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required dependencies:

bash

    pip install fastapi httpx uvicorn

Running the Application

    Start the FastAPI application using Uvicorn:

    bash

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

    main refers to the name of your Python file (e.g., main.py).
    The --reload option allows for automatic code reload during development.

Access the API documentation:

Once the server is running, you can access the automatically generated API documentation at:

bash

    http://localhost:8000/docs

    Here, you can explore the available endpoints and test them directly from your browser.

API Endpoints

    GET /professors-data
        Fetches data for all predefined professors.

    GET /professor-data/{professor_name}
        Fetches detailed data for a specific professor by name. If the professor is not found, it returns a 404 error.

CORS Configuration

The application is configured to allow requests from the frontend hosted at http://localhost:3000. Adjust the CORS settings in the main.py file if needed for other origins.
Contribution

If you would like to contribute to this project, please fork the repository and submit a pull request.
