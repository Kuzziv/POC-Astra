# Django Ninja CMS Backend

This project is built with Django Ninja for backend development. Below are the instructions to set up the project, run the development server, and perform basic operations like database migrations and creating a superuser.

## Prerequisites

Make sure you have the following installed on your system:
- [Python 3.12.6](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <project_directory>
```

### 2. Create and Activate a Virtual Environment

#### On Windows:
```bash
python -m venv env
.\env\Scripts\Activate
```

#### On macOS/Linux:
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install the Required Dependencies

Once the virtual environment is activated, install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Start the Application

To run the Django development server, use the following command:

```bash
py manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.

## Common Django Management Commands

### 1. Make Migrations
To create new migrations based on changes to models, run:

```bash
py manage.py makemigrations
```

### 2. Apply Migrations
To apply the migrations to the database, run:

```bash
py manage.py migrate
```

### 3. Flush the Database
To reset the database (delete all data and reset tables), use:

```bash
py manage.py flush
```

### 4. Create a Superuser
To create an admin user for accessing the Django admin panel, run:

```bash
py manage.py createsuperuser
```

Follow the prompts to set up the username, email, and password.

### 5. Check for Issues
To run Django's system check for potential problems, use:

```bash
py manage.py check
```

### 6. Django Shell
To open the Django shell and import custom functions, run:

```bash
py manage.py shell
```

Inside the shell, you can import functions or modules as needed:

```python
from yourapp.models import YourModel
from yourapp.views import functionName
```

## Swagger documention
http://127.0.0.1:8000/api/docs

## Additional Notes

- Make sure the virtual environment is activated before running any `manage.py` commands.
- If you encounter any issues, check that the dependencies are installed correctly by running `pip freeze` and comparing with the `requirements.txt` file.

---

Happy Coding!