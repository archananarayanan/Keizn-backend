To Execute the Project -- 

1. pip install requirements.txt

Once you have a DB configured on your local - 
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py runserver 

Access the application from your local at -
http://127.0.0.800/doc -- Swagger documentation that guides for navigating across the APIs. 

1. Before you use the functional APIs, please create a user using http://127.0.0.800/api/register , then login with the same credentials at http://127.0.0.800/login. 
2. you will be presented with a Bearer token which you can use to access the functional APIs. 
3. Swagger does not support updating Auth headers, hence use Postman or other request services that are available to send the request to your local server, by updating the Authorization header with the Bearer token. 
