# Task Manager Application

A simple web-based task management application built with Python and Flask.

## Features

- Create, read, and delete tasks
- Mark tasks as complete/incomplete
- Responsive design that works on mobile and desktop
- Clean and modern user interface
- Real-time updates

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository or download the source code
2. Navigate to the project directory:
   ```
   cd C:\work\task_manager_python
   ```
3. Create a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure you're in the project directory
2. Run the application:
   ```
   python app.py
   ```
3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure

```
task_manager_python/
├── app.py              # Main application file
├── config.py           # Application configuration
├── database.py         # Database initialization
├── requirements.txt    # Python dependencies
├── models/             # Data models
│   ├── __init__.py
│   └── task.py         # Task model
├── routes/             # Application routes
│   ├── __init__.py
│   └── tasks.py        # Task-related routes
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   └── index.html      # Main page
└── static/             # Static files
    ├── css/
    │   └── style.css   # Stylesheet
    └── js/
        └── main.js     # JavaScript
```

## License

This project is open source and available under the [MIT License](LICENSE).
