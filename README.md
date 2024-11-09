# CSC 605

## Project: Kakeibo 2.0

### Author: Anthony R, Dillion T Errol V
V.1.0.0

### Links and Resources
- Back-end server url: http://localhost:8000
- Front-end application : None

### Setup
- Install Docker
- Install ThunderClient extension in VS Code

i.e.

- PORT - Port Number: 8000
- DATABASE_URL - None (using default SQLite database)

### How to initialize/run your application (where applicable)

- git clone https://github.com/evidad/CSC605
- Run the command: docker build -t django_project .
- Run the command: docker compose up --build
- Run the command: docker compose run web python manage.py createsuperuser
- In the web browser, navigate to http://localhost:8000/admin/

### How to use your library (where applicable)

### Manual Test Procedures:

- While Docker container is up, create superuser
    - run: docker compose run web python manage.py createsuperuser
- Get Token steps:
    - In ThunderClient, create a POST request to http://localhost:8000/api/token/ 
        - Navigate to Body --> JSON and create JSON object using "username": "superuser_username", "password": "superuser_password" 
        - Click send and copy access token
        - Copy refresh token if needed for refresh token steps
- Refresh Token steps:
    - In ThunderClient, create a POST request to http://localhost:8000/api/token/refresh/ 
        - Navigate to Body --> JSON and create JSON object using "refresh": "refresh_token" 
        - Click send and copy access token

- CRUD Routes:
    Certainly! Here’s the API endpoints section in plain Markdown, ready for copying:

---

### API Endpoints

Certainly! Here’s the API endpoints section in plain Markdown, ready for copying:

---

### API Endpoints

#### Admin Panel
- **URL**: [http://localhost:8000/admin/](http://localhost:8000/admin/)  
  Access the Django admin interface.

#### Transaction Endpoints
- **List All Transactions**
  - **Method**: `GET`
  - **URL**: `/api/v1/kakeibo/transactions/`

- **Create a Transaction**
  - **Method**: `POST`
  - **URL**: `/api/v1/kakeibo/transactions/`
  - **Body** (JSON):
    ```json
    {
      "owner": "user_id",
      "category": "INCOME/ESSENTIAL/WANTS/SAVINGS/OTHER",
      "description": "Transaction description",
      "amount": 100.00,
      "transaction_date": "YYYY-MM-DD"
    }
    ```

- **Transaction Detail**
  - **Method**: `GET`, `PUT`, `DELETE`
  - **URL**: `/api/v1/kakeibo/transactions/<int:id>/`
  - **Description**: View, update, or delete a transaction. Update and delete actions are restricted to the owner.

#### Budget Endpoints
- **List All Budgets**
  - **Method**: `GET`
  - **URL**: `/api/v1/kakeibo/budgets/`

- **Create a Budget**
  - **Method**: `POST`
  - **URL**: `/api/v1/kakeibo/budgets/`
  - **Body** (JSON):
    ```json
    {
      "owner": "user_id",
      "month": "Month name or identifier",
      "income_goal": 5000.00,
      "savings_goal": 1000.00
    }
    ```

- **Budget Detail**
  - **Method**: `GET`, `PUT`, `DELETE`
  - **URL**: `/api/v1/kakeibo/budgets/<int:id>/`
  - **Description**: View, update, or delete a budget. Update and delete actions are restricted to the owner.

#### Authentication Endpoints
- **Token Access**
  - **Method**: `POST`
  - **URL**: `/api/token/`
  - **Body** (JSON):
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```

- **Token Refresh**
  - **Method**: `POST`
  - **URL**: `/api/token/refresh/`
  - **Body** (JSON):
    ```json
    {
      "refresh": "your_refresh_token"
    }
    ```
