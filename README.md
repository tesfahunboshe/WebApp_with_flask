# WebApp_with_flask
**Setup**

This web App was created based on the tutorial at Flask documentation.The following steps were followed:

**The application factory**

* A function with a flask instance was created.

**Database**

SQLite database. Python’s sqlite3 module was used to create and connect the connection to the database. 

Package g was used to store data accessed by multiple functions during the request.


![Database scheme ](https://github.com/tesfahunboshe/WebApp_with_flask/blob/main/Screenshot%20from%202021-05-08%2023-56-17.png?raw=true)

**Blueprints and Views**

Blueprint modules were used to create an organized and group related views and other code.

* Auth

    * Register – registers a new user to the database
    
    * Login – verifies user information and creates a session for a logged in user.
    
    * Logout – clears the session. Frees up the memory.

* Blog

    * Home – redirects the logged in user to the home page.

    * Applications – displays the most recent application of the user.

    * Get_post – a function for querying the data from database.

    * Applynow – redirects to applynow.html file. This is where the user makes first draft of his
    application.

    * Update – redirects to the page where the user can update his current application.

    * Table – redirects to the page with applicants table and countries table.

    * Profile – this returns the profile page for the logged in user.

    * Delete – deletes the user input data from the database.

    * Admin – the admin is able to see all applicants and grade the applications, as well as give
final decisions.


**Templates**

Jinja template library is used to render templates.

**Run the application.**

    $ export FLASK_APP=flaskr
  
    $ export FLASK_ENV=development
  
    $ flask run



**Other locations**

The app was deployed to https://tesfaboshe.pythonanywhere.com/ 
