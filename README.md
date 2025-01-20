This is an online store built using Django. The project supports:
account management (django_auth), product management, cart and order management, product search functionality (postgres trigram).

Follow these steps to deploy the application:
1. docker compose up --build
2. follow the link http://127.0.0.1:8000/
3. To interact with Django via console from Docker:
   docker exec -it webstore-main-web-1 /bin/bash
5. Postgres database setup. To use the search string in the app, enter the following:
  docker exec -it webstore-main-db-1 psql -U postgres -d webstore
  CREATE EXTENSION pg_trgm;
