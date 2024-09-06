# Independent Study Project

This project is a FastAPI-based application with PostgreSQL vector database integration, designed for advanced data processing and AI capabilities.

## 🚀 Features

- FastAPI backend with RESTful API endpoints
- PostgreSQL with pgvector extension for vector similarity search
- Google Generative AI integration
- Web scraping capabilities using Selenium and BeautifulSoup4
- PDF processing with pdfminer.six
- Containerized deployment using Docker

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL with pgvector
- **AI Integration:** Google Generative AI
- **Web Scraping:** Selenium, BeautifulSoup4
- **PDF Processing:** pdfminer.six
- **Containerization:** Docker, Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.x
- PostgreSQL

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd independentStudy
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add necessary environment variables.

## 🚀 Running the Application

### Using Docker (Recommended)

1. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

The application will be available at `http://localhost:8000`

### Simulating Database with Backup

To simulate the database using a backup file:

1. Copy the backup file into the container:
   ```bash
   docker cp ./backup.sql independentstudy-db-1:/tmp/backup.sql
   ```

2. Restore the database from the backup:
   ```bash
   docker exec independentstudy-db-1 bash -c 'psql -U postgres -d db < /tmp/backup.sql'
   ```

### Without Docker

1. Ensure PostgreSQL is running locally
2. Set up the environment variables
3. Run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📁 Project Structure

```
independentStudy/
├── app/              # Main application code
├── docs/            # Documentation
├── scripts/         # Utility scripts
├── requirements.txt # Python dependencies
├── dockerfile      # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── .env            # Environment variables
```

## 📝 Usage

Refer to the API documentation at `http://localhost:8000/docs` when the application is running.

