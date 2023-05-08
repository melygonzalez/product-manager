# Product Manager with DRF

This is a Product Manager app built using Django Rest Framework. The app allows users to create, update, delete, and view products based on permissions. This app use JWT for authentication.

## Getting Started

Follow this instructions to setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation

1. Create project directory using `mkadir productmanager`.
2. Navigate to the project directory using `cd productmanager`.
3. Clone the repository from GitHub using `git clone https://github.com/melygonzalez/productmanager.git`.
4. Create a virtual environment using `python -m venv env` command.
5. Activate the virtual environment using `source env/bin/activate` command.
6. Install the dependencies using `pip install -r requirements.txt` command.
7. Run the migrations using `python manage.py migrate` command.

### Usage

To start the app, run python manage.py runserver command. This will start the development server at http://localhost:8000/.

### Authentication

The app uses token-based authentication. To obtain an access token, send a `POST` request to the `/api/token` endpoint with a valid username and password. The response will contain an access token which can be used to authenticate subsequent requests.

### API endpoints:

1. `POST /api/token/`
- Create access token. ***Anyone can access***
2. `GET /users/`
- Get a list of all users. ***Only admins can access***
3. `POST /users/`
- Create a new user. ***Anyone can access***
4. `GET /users/{id}/approve`
- Approve users by id. ***Only admins can access***
5. `GET /products/`
- Get a list of all products. ***Anyone can access, only users view all info***
6. `POST /products/`
- Create a new product. ***All approved users can access***
7. `GET /api/v1/products/{id}/`
- Get a product by id. ***All approved users can access***
8. `PATCH /api/v1/products/{id}/`
- Update a product by id. ***All approved users can access***
9. `DELETE /products/{id}/`: .
- Delete a product by id. ***All approved users can access***


### Testing

Postman collection for the project are available in folder `productmanager`, ready to import and use.

