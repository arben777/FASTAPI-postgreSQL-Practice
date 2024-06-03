# FASTAPI-postgreSQL-Practice

The codebase consists of models for Questions and Choices, with corresponding database tables. FastAPI endpoints are set up to read questions and choices, and create new questions with choices. Data validation is done using Pydantic models. A database connection is established using SessionLocal.

### Database Structure and Relationships Summary:
- **Tables**: `questions` and `choices`
- **Columns**:
  - `questions`: id, question_text
  - `choices`: id, choice_text, is_correct, question_id (foreign key referencing questions.id)

### File Summaries:
- **main.py**:
  - Defines FastAPI endpoints for reading questions, choices, and creating questions with choices.
- **models.py**:
  - Contains SQLAlchemy models for Questions and Choices.
- **database.py**:
  - Establishes the database connection.