## ROUTES
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/auth/signup/``` | _Register new user_| _All users_|
| *POST* | ```/auth/login/``` | _Login user_|_All users_|
| *POST* | ```/auth/refresh/``` | _Refresh Token_|_All users_|
| *POST* | ```/orders/create_order/``` | _Create an order_|_All users_|
| *PUT* | ```/orders/order/update/{id}/``` | _Update an order_|_All users_|
| *PUT* | ```/orders/order/status/{id}/``` | _Update order status_|_Superuser_|
| *DELETE* | ```/orders/order/delete/{order_id}/``` | _Delete/Remove an order_ |_All users_|
| *GET* | ```/auth/all_users/``` | _List all users_|_All users_|
| *GET* | ```/orders/user/orders/``` | _Get user's orders_|_All users_|
| *GET* | ```/orders/all_orders/``` | _List all orders made_|_Superuser_|
| *GET* | ```/orders/orders/{order_id}/``` | _Retrieve an order_|_Superuser_|
| *GET* | ```/orders/user/order/{order_id}/``` | _Get user's specific order_|                          
<<<<<<< HEAD
| *GET* | ```/docs/``` | _View API documentation_|_All users_|
=======
| *GET* | ```/docs/``` | _View API documentation_|_All users_|
>>>>>>> 779e936eb467abf9cf06e4b5f812c636b8306755
