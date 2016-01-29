Tinysso
=============
[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

###Summary 
A very simple SSO(i.e. Single Sign On) system based on the flask microframework.

###Dependencies

####TinySSO
* python(3.0+)
* Flask (0.10.1+)
* Flask-WTF (0.12+)
* psycopg2 (2.6+)

####Test Program
#####.NET SDK & Sample
* .NET Framework 4.0
* [Newtonsoft.Json 7.0.1](http://www.newtonsoft.com/json)
  (If you want to build the test asp.net program, you'll need to place the Newtonsoft.Json dll file to test/lib first.)

#####Python SDK & Sample
* python(3.0+)
* Flask (0.10.1+)

###How to configure
There are some basic setting for the tinysso to work normally. 
Divided into 2 catagories:
- Settings for the tinysso server itself
- Settings for the PostgreSQL database to which the tinysso connects

The configure file is named as "tinysso.ini" and should be placed in the root directory of the tinysso.
Anytime you change the settings of the configure file, you must restart the tinysso server to make the change work.

A sample of "tinysso.ini" is as follows.
```
    [sso_server]
    listenport = 5000   ; The port number from which the tinysso accepts the requests.

    [pg_server]
    host = 127.0.0.1    ; The host name or ip address of the PostgreSQL server.
    port = 5432         ; The port number of the PostgreSQL database instance to which the tinysso connects.
    dbname = testdb     ; The name of the logical database to which the tinysso connects.
    user = tinysso      ; The PostgreSQL user name with which the tinysso connects to the database
    password = asdf1234 ; The password for the option "user".
```

###TODO
The following items need to be implemented in future.
- [x] A client web application for the test.
- [x] The database access code for the actual user authentication while signing in.
- [ ] A mechanism to certify the client applications.
- [x] A sign up logic.
- [ ] The implementation of tinysso log.
- [ ] The design of all the html pages.
- [ ] The single sign out logic.
