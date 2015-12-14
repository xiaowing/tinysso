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
* .NET Framework 4.0
* [Newtonsoft.Json 7.0.1](http://www.newtonsoft.com/json)
  (If you want to build the test asp.net program, you'll need to place the Newtonsoft.Json dll file to test/lib first.)


###TODO
The following items need to be implemented in future.
- [x] A client web application for the test.
- [x] The database access code for the actual user authentication while signing in.
- [ ] A mechanism to certify the client applications.
- [x] A sign up logic.
- [ ] The implementation of tinysso log.
- [ ] The design of all the html pages.
- [ ] The single sign out logic.
