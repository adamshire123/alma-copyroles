# copyroles

- Copies all alma roles from one user to another.
- Any existing roles of the destination user are overwritten.

## Required ENV
```shell
PROD_ALMA_API_KEY=# an Alma API key for the Alma `production` environemnt with `user` read/write permissions and `conf` read permissions
SANDBOX_ALMA_API_KEY=# an Alma API key for the Alma `sandbox` environemnt with `user` read/write permissions and `conf` read permissions
```
## To run

- Create a virtual environment and install dependencies
    
    `make install`

- Run the script from the virtual environment, passing in the primary ID's of the source and target users as commandline arguments

    `pipenv run copy_roles [primary_id_of_user_to_copy_from] [primary_id_of_user_to_copy_to] -e [alma environment 'prod' or 'sandbox']`
