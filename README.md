# Django Project README

## Features

This Django project provides the following features:

1. **Upload Files:**

   - Upload files containing initial account information in CSV or TXT format.

2. **Save Accounts:**

   - Save the uploaded accounts into the database.

3. **List Accounts:**

   - List all accounts and show detailed information for each account individually.

4. **Search Accounts:**

   - Search for a specific account using the account name.

5. **Transfer Balance:**
   - Transfer balances between two accounts with proper validation.

6. **Unit Test:**
   - Unit test has been written to test main functionality (Balance Transfer, Search, Accounts List, Uploads files with different extensions)
---

## Setting up the Django Project Locally

Follow these steps to set up the Django project on your local machine:

1. **Create a Virtual Environment:**

   ```bash
   python -m venv .venv
   ```

2. **Activate the Virtual Environment:**

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. **Install Requirements:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create Migration Files:**

   ```bash
   python manage.py makemigrations
   ```

5. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Run the Server:**
   ```bash
   python manage.py runserver
   ```
   The server will run on the default port (127.0.0.1:8000). You can specify a custom port by appending it to the command, e.g., `python manage.py runserver 8080`.

---

## Running the Project Using Docker and Docker Compose

1. **Build the Docker Image:**

   ```bash
   docker build -t docspert-web:latest .
   ```

2. **Run Docker Compose:**

   ```bash
   docker-compose up
   ```

3. **Access the Application:**
   Open your browser and navigate to:

   ```
   http://127.0.0.1:8000
   ```

   (Assuming the port in the Dockerfile is bound to port 8000 on your machine.)

4. **Note:**
   - The Docker container uses a `startup.sh` script to execute commands when the container starts.

---

## Notes

1. **Database Configuration:**
   - By default, this project uses SQLite as the database. If you want to switch to another database instance (e.g., PostgreSQL, MySQL), you need to:
     - Update the `DATABASES` section in the `settings.py` file with your database configuration.
     - Modify the `docker-compose.yml` file to include the new database service and ensure proper connectivity between containers.

## To run unit test to check the logic

1. **Run Unit Test:**

   ```bash
   python manage.py test
   ```

## Video Demo

You can watch a demonstration of the functionality of the project in the video below:

[![Functionality Demo](https://img.shields.io/badge/Watch%20Video%20Demo-Click%20Here-blue)](https://drive.google.com/file/d/1fO25SxCj28UQmH9YgBSlsdG4l-GRPJBV/view?usp=sharing)

Click on the image or the link to view the video directly from Google Drive.

> **Note**: If the video does not play, you can directly access it by [clicking here](https://drive.google.com/file/d/1fO25SxCj28UQmH9YgBSlsdG4l-GRPJBV/view?usp=sharing).

