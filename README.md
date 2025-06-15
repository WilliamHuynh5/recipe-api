# 🧑‍🍳 Recipe API – Setup & Running Guide

This project is a **Recipe API** built with **FastAPI** and uses **SQLite** as its database. 
During marking, please refer to these following files:
- `design.txt` - A high level explanation of the design
- `assumptions.txt` - A list of assumptions made throughout this project
- `challenges.txt` - A list of technical challenges encountered throughout this project

## 🚀 Project Overview
A simple Recipe API that returns a list of recipes, ingredients and provides options for unit conversion and portion sizes.

## 🛠️ Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.9 or higher  
- `pip` package manager
- Linux/WSL Environment

### 2. Create a Virtual Environment

Create an isolated Python environment to manage dependencies:

```
python3 -m venv venv
```

### 3. Activate the Virtual Environment

Activate your virtual environment:

```
source venv/bin/activate
```

### 4. Install Dependencies

Install the required Python packages:

```
pip install -r requirements.txt
```


### 5. Seed the Database

Initialize and seed the SQLite database with starter data:

```
python3 -m app.database.init_db
```

### 6. Run the API Server

Start the FastAPI server with auto-reload enabled:

```
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Try out this sample route!

http://127.0.0.1:8000/ingredients?recipe_id=r2&desired_portions=10

> Highly reccomended to use a API Client like `Postman` to invoke the API

**`/recipes` route:**

https://.postman.co/workspace/My-Workspace~69baad4f-6d85-4ff0-8c44-e3dad326618e/request/21722913-360401b5-0869-4807-8df7-6d59c879c859?action=share&creator=21722913&ctx=documentation

**`/ingredients` route:**

https://.postman.co/workspace/My-Workspace~69baad4f-6d85-4ff0-8c44-e3dad326618e/request/21722913-8377459e-8914-4b50-a5b8-5387aa6e0021?action=share&creator=21722913&ctx=documentation
