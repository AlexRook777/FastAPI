# FastAPI Project

This is a project built with FastAPI that interacts with a SQL database.

## Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AlexRook777/FastAPI.git
   ```
2. Navigate to the project directory:
   ```bash
   cd FastAPI
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows, use:
   .venv\Scripts\activate
   # On macOS and Linux, use:
   source .venv/bin/activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

You can access the API documentation at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
