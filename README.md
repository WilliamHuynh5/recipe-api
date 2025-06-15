# 🧑‍🍳 Recipe API – Setup & Running Guide

This project is a **Recipe API** built with **FastAPI** and uses **SQLite** as its database. The API allows users to manage recipes by creating, reading, updating, and deleting recipe data including ingredients and portions. This guide will help you set up the project environment, seed the database with initial data, and run the API server locally.

---

## 🚀 Project Overview

The Recipe API provides a simple and efficient way to manage recipe information through RESTful endpoints. It is designed for easy local development and testing with FastAPI’s automatic documentation and hot-reload capabilities.

---

## 🛠️ Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.9 or higher  
- `pip` package manager

---

### 2. Create a Virtual Environment

Create an isolated Python environment to manage dependencies:

`python3 -m venv venv`

---

### 3. Activate the Virtual Environment

Activate your virtual environment:

`source venv/bin/activate`

> For Windows, use: `venv\Scripts\activate`

---

### 4. Install Dependencies

Install the required Python packages:

`pip install -r requirements.txt`

---

### 5. Seed the Database

Initialize and seed the SQLite database with starter data:

`python3 -m app.database.init_db`

---

### 6. Run the API Server

Start the FastAPI server with auto-reload enabled:

`uvicorn app.main:app --reload`

The API will be available at `http://127.0.0.1:8000`

Try out this sample route!

http://127.0.0.1:8000/ingredients?recipe_id=r2&desired_portions=10

---

