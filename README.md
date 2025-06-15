# 🧑‍🍳 Recipe API – Running & Seeding the Database

This guide explains how to set up, run, and seed the database for the Recipe API project using FastAPI and SQLite.

---

## 📦 Prerequisites

- Python 3.9+
- `pip` package manager
---

## 🔧 1. Create a Virtual Environment

Create virtual environment:

```bash
 python3 -m venv venv  
```

## 🔧 2. Active the Virtual Environment

Activate virtual environment. This should create a `venv` terminal

```bash
source venv/bin/activate
```

## 📥 3. Install Dependencies

In the `venv` terminal, install the required packages:

```
pip install -r requirements.txt
```

## 📥 4. Seed the database

```
python3 -m app.database.init_db
```

## 🚀 5. Run the Server

```
uvicorn app.main:app --reload
```
