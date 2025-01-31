# copyroles

Utilities for copying alma roles and users

## Required ENV
```shell
PROD_ALMA_API_KEY=# an Alma API key for the Alma `production` environemnt with `user` read/write permissions and `conf` read permissions
SANDBOX_ALMA_API_KEY=# an Alma API key for the Alma `sandbox` environemnt with `user` read/write permissions and `conf` read permissions
```
## To run

- Create a virtual environment and install dependencies
    
    `make install`

- Run the command from the virtual environment, passing in the required parameters 
    - copy_roles: 
        - copy alma rules from one user to another in the same alma environment
        -  the roles of the target users will be completely overwritten

         `pipenv run copy_roles [primary_id_of_source_user] [primary_id_of_target_user] -e [alma environment 'prod' or 'sandbox']`
    - copy_user: 
        - Copy a user from Production to Sandbox

         `pipenv run copy_user = [primary_id_of_source_user]`
    
