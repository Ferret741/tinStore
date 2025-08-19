## ========================================================================= ##
##                                                                           ##
##                              IMPORT SECTION                               ##
##                                                                           ##
## ========================================================================= ##
import argparse
import os
import yaml



## ========================================================================= ##
##                                                                           ##
##                             VARIABLES SECTION                             ##
##                                                                           ##
## ========================================================================= ##
env_username = 'BIGTIN_TINSTORE_USERNAME'
env_password = 'BIGTIN_TINSTORE_PASSWORD'
default_config_file_location = '/etc/tinstore.yaml'
error_message = {'NO_CONFIG': 'You little shit, the configuration file does not exist!',
                 'NO_CREDS' : 'Either password or username was not properly populated.',}



## ========================================================================= ##
##                                                                           ##
##                             CLASSES SECTION                               ##
##                                                                           ##
## ========================================================================= ##




## ========================================================================= ##
##                                                                           ##
##                             FUNCTION SECTION                              ##
##                                                                           ##
## ========================================================================= ##
def obtain_creds_from_conf(conf_file: str) -> list:
    """
    Parse a yaml cofniguration file, extract the username and passwords,
    and return those values in a list format.
    """


    ## ========================================================================
    ## Basic variable assignment
    username = None
    password = None


    ## ========================================================================
    ## Parse the configuration file
    with open(conf_file,'r') as conf_file_handle:


        ## ====================================================================
        ## Load the yaml file
        yaml_obj = yaml.safe_load(conf_file_handle)


        ## ====================================================================
        ## Try to grab a username and password from the top level.
        username = yaml_obj.get('username',None)
        password = yaml_obj.get('password',None)


    ## ========================================================================
    ## Return the username and password values
    return [username, password]




def check_if_file_exists(filepath: str) -> bool:
    """
    This function thecks the existence of a file, and returns a boolean
    indicating as such
    """


    ## ========================================================================
    ## Return whether the file exists
    return os.path.isfile(filepath)




def check_if_creds_are_populated(username: str,
                                 password: str,) -> bool:
    """
    This function checks to ensure that the user and password credentials
    are populated. Returns either a true or false
    """


    ## ========================================================================
    ## Define some local variables
    all_credentials_exist = True


    ## ========================================================================
    ## Either username or password is defined as None. This implies that
    ## the corresponding username or password argument was not supplied on
    ## command line, AND no associated environment variable was found. In
    ## this case, set the all_credentials_exist variable to false
    if not username or not password:
        all_credentials_exist = False


    ## ========================================================================
    ## Return the result of the check for the existence of credentials
    return all_credentials_exist






def parse_command_line_args() -> argparse.Namespace:
    """
    Function that parses command line arguments and assigns values accordingly
    """


    ## ========================================================================
    ## Create a arguemnt parser object
    parser_object = argparse.ArgumentParser()


    ## ========================================================================
    ## Add the username and password arguments to the parser object. These
    ## both accept a default value corresponding to an environment variable.
    ## Should that environment variable not be defined, then the argument will
    ## assume a value of 'None' (python's version of NULL)
    parser_object.add_argument('-u',
                               '--username',
                               dest    = 'username',
                               action  = 'store',
                               default = os.environ.get(env_username,None))
    parser_object.add_argument('-p',
                               '--password',
                               dest    = 'password',
                               action  = 'store',
                               default = os.environ.get(env_password,None))
    parser_object.add_argument('-c',
                               '--config-file',
                               dest    = 'config_file',
                               action  = 'store',
                               default = default_config_file_location)



    ## ========================================================================
    ## Return the parsed arguments. This method is lazy, but gets the point
    ## across. You should really error check for the parse_args() method
    return parser_object.parse_args()




## ========================================================================= ##
##                                                                           ##
##                              MAIN BODY                                    ##
##                                                                           ##
## ========================================================================= ##
if __name__ == "__main__":
    """
    Main program. We are looking for credentials in the following levels
    - Environment variables
    - Configuration file (yaml file with top-level username/password keys)
    - Command line --username/--password values

    A value provided at each level will override the one above it (e.g. a
    username provided at command line will override usernames provided in
    both configuration file and environment variable leves).
    """



    ## ========================================================================
    ## Some basic variable declarations
    script_args = None


    ## ========================================================================
    ## Parse the command line arguments here
    script_args = parse_command_line_args()


    ## ========================================================================
    ## If the configuration file exists, then parse it for the username
    ## and passwords. This will override the default environment variables
    if check_if_file_exists(script_args.config_file):
        [script_args.username,
         script_args.password] = obtain_creds_from_conf(script_args.config_file)



    ## ========================================================================
    ## Parse the configuration file and retrieve the username and password


    ## ========================================================================
    ## Make certain that both username and password are properly populated. At
    ## this point we have checked our entire hierarchy, and so someone done
    ## messed up
    if not check_if_creds_are_populated(script_args.username,
                                        script_args.password):


        ## ====================================================================
        ## Raise an exception
        raise Exception(error_message['NO_CREDS'])


    ## ========================================================================
    ## Print the username and password
    print(f'Username is: {script_args.username}')
    print(f'Password is: {script_args.password}')
