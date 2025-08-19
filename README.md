## **Overview**
This script attempts to pull credentials from three (3) different places, the following order:
- Environment variables
- Command line arguments
- Configuration file

Each level will override any username/password that was set in a levele above it. For example,
a username provided on the command line argument will override a username value set with an 
environment variable, but not one provided in a configuration file

There is as conf.yaml file that you can use for testing


## **Tests**

---
### ***Running file with no options and no environment variables***

~~~bash
$ python credentials_example.py
Traceback (most recent call last):
  File "/home/github/HOME/git/Ferret741/tinstore/credentials_example.py", line 214, in <module>
    raise Exception(error_message['NO_CREDS'])
Exception: Either password or username was not properly populated.
~~~

### ***Running file with environment variables***

~~~bash
$ BIGTIN_TINSTORE_USERNAME=bigtin_env_user BIGTIN_TINSTORE_PASSWORD=bigtin_env_pass python credentials_example.py
Username is: bigtin_env_user
Password is: bigtin_env_pass
~~~

### ***Setting usrename and password on command line, while also having environment variables set***

~~~bash
$ BIGTIN_TINSTORE_USERNAME=bigtin_env_user BIGTIN_TINSTORE_PASSWORD=bigtin_env_pass python credentials_example.py  --username=bigtin_user_cli --password=bigtin_pass_cli
Username is: bigtin_user_cli
Password is: bigtin_pass_cli
~~~

### ***Running file with environment variables and configuration file***

~~~bash
$ BIGTIN_TINSTORE_USERNAME=bigtin_env_user BIGTIN_TINSTORE_PASSWORD=bigtin_env_pass python credentials_example.py  --config-file conf.yaml
Username is: i_am_bigtin
Password is: hehehehe
~~~

### ***Using combination of things***

~~~bash
$ BIGTIN_TINSTORE_USERNAME=bigtin_env_user  python credentials_example.py  --password=bigtin_pass_cli
Username is: bigtin_env_user
Password is: bigtin_pass_cli


$ BIGTIN_TINSTORE_USERNAME=bigtin_env_user  python credentials_example.py  --password=bigtin_pass_cli --config-file=conf.yaml
Username is: i_am_bigtin
Password is: hehehehe
~~~
