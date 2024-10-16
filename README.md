drScratch
=========

drScratch is an analytical tool that evaluates your Scratch projects in a variety of computational areas to provide feedback on aspects such as abstraction, logical thinking, synchronization, parallelization, flow control, user interactivity and data representation. This analyzer is a helpful tool to evaluate your own projects, or those of your Scratch students.

You can try a beta version of drScratch at http://drscratch.org

### How to deploy drScratch server in local environment
Docker and docker-compose are required to deploy local environment. Type next commands:

```console
make build
make start
```

### How to access to containers of drScratchv3
```console
$ docker run -d -p 3306:3306 --name drscratchv3_database -e MYSQL_ROOT_PASSWORD=password mysql
$ docker exec -it drscratchv3_database mysql -p
$ docker exec -it drscratchv3_django bash
```

### How to activate translations
```console
make translate
```
## For use Batch Mode and Contact Form
For use Batch Mode and Contact Form you will need to set up an email, you can use the provider you preffer. Remember that it's important the email can be used in a website environment. For set up the email in Dr. Scratch in order to use the Batch Mode and the Contact Form, you have to open the **.env** file and fill the put the email and the password in his corresponding line. **DEFAULT_FROM_EMAIL** and **EMAIL_HOST_USER** for the email and **EMAIL_HOST_PASSWORD** for the password.  

¿Why i have to do this?
The Batch Mode allows you to analyze multiple projects and then send the results to an email, because of this you will need a email host provider in order to send this results to an specific email. The same situation happens with the Contact Form.
