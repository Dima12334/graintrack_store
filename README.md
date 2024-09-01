# Graintrack challenge

## Used technologies:
- DRF, Pydantic, Poetry, Black, PostgreSQL, Docker.

## Installation
1. Clone repository:
```
git clone https://github.com/Dima12334/graintrack_store.git
```
2. Build and up docker containers:
```
docker-compose up --build
```
3. Load db dump (optional):
```
docker-compose exec -T db psql -U postgres -d graintrack_store < dump_db.sql
```
4. If you didn't load dumb, you need to apply django migrations by this command:
```
docker-compose exec app python manage.py migrate
```
5. Create user
```
docker-compose exec app python manage.py createsuperuser
```
or if you loaded db dump, you can use existing user:
* **username**: ```admin```
* **password**: ```qwerty```
6. Done. Use the App.

You can find Swagger documentation for API at this url http://127.0.0.1:8000/api/docs/

Also you can use Postman [collection](https://elements.getpostman.com/redirect?entityId=25524341-3da7f851-2949-42d0-a6fc-a662c3edc0a6&entityType=collection) to interact with API.

## API methods description

API entry point: http://127.0.0.1:8000/api/v1/.

All available filters are listed in the Postman collection and in the Swagger documentation.

---
## Auth

### `/auth/session/login/`
-  Implemented methods: POST

### `/auth/session/logout/`
-  Implemented methods: POST

---
## Orders
### `/orders/`
- Implemented methods: GET, POST

### `/orders/{uuid}/`
- Implemented methods: GET, PUT, DELETE

---
## Order products
*  **Used to link products to order.**

### `/orders/products/`
- Implemented methods: GET, POST

### `/orders/products/{uuid}/`
- Implemented methods: GET, PUT, DELETE

---
## Products
### `/products/`
- Implemented methods: GET, POST

### `/products/{uuid}/`
- Implemented methods: GET, PUT

### `/products/reports/sold-products/`
- Implemented methods: GET

---
## Product categories
### `/products/categories/`
- Implemented methods: GET, POST

### `/products/categories/{uuid}/`
- Implemented methods: GET, PUT

---
## Product incomes
* **Used to increase product available quantity.**
### `/products/incomes/`
- Implemented methods: GET, POST

---
## Product discounts
* **Used to activate or deactivate discount on product.**
### `/products/discounts/`
- Implemented methods: GET, POST

### `/products/discounts/{uuid}/`
- Implemented methods: GET, PUT
