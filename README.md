# alma-copyroles
- Copies all alma roles from one user to another.
- Any existing roles of the destination user are overwritten.

# Required environment variables
ALMA_API_KEY = an Alma API key with `user` read/write permissions and `conf` read permissions

# How to run:
- Install dependencies in a virtual environment
    
    `pipenv install`
    
- add api key to environment variables

    `export ALMA_API_KEY=[alma api key]`

- Run the script from the virtual environment

    pipenv run copy [primary_id_of_user_to_copy_from] [primary_id_of_user_to_copy_to]