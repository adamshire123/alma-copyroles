import os

import click
from requests.exceptions import HTTPError
from tabulate import tabulate

from copyroles.alma import AlmaClient


@click.command()
@click.argument("source_username", type=str)
@click.argument("target_username", type=str)
@click.option(
    "--source-env",
    type=click.Choice(["prod", "sandbox"], case_sensitive=False),
    required=True,
    help="Environment of the source user (prod or sandbox).",
)
@click.option(
    "--target-env",
    type=click.Choice(["prod", "sandbox"], case_sensitive=False),
    required=True,
    help="Environment of the target user (prod or sandbox).",
)
def main(
    source_username: str, target_username: str, source_env: str, target_env: str
) -> None:
    if source_env == "sandbox" and target_env == "prod":
        message = "Cannot copy roles from sandbox to prod environment."
        raise click.UsageError(message)
    alma_api_keys = {}
    alma_api_keys["prod"] = os.environ["PROD_ALMA_API_KEY"]
    alma_api_keys["sandbox"] = os.environ["SANDBOX_ALMA_API_KEY"]
    try:
        source_alma_client = AlmaClient(alma_api_keys[source_env])
        target_alma_client = AlmaClient(alma_api_keys[target_env])
    except KeyError as e:
        click.echo(f"Error creating alma client: {e}")
        return
    job_summary = (
        f"Source: \033[1m{source_username.upper()}\033[0m - "
        f"\033[1m{target_alma_client.alma_environment.upper()}\033[0m\n"
        f"Target: \033[1m{target_username.upper()}\033[0m - "
        f"\033[1m{target_alma_client.alma_environment.upper()}\033[0m\n"
    )
    click.echo("\n-- Copy Alma Roles --\n" + job_summary)

    if click.confirm("Continue and review roles?", default=False, abort=False):
        try:
            source_user = source_alma_client.get_alma_user(source_username)
            target_user = target_alma_client.get_alma_user(target_username)
            source_roles: list = source_user["user_role"]
        except HTTPError as e:
            click.echo(f"Error getting users: {e}")
            return
        if click.confirm("review roles?"):
            click.echo(print_user_roles(source_roles))
        do_copy = click.prompt(
            "\nCopy these Alma roles?\n"
            + job_summary
            + "\nWARNING: THIS OPERATION CANNOT BE UNDONE.\n",
            prompt_suffix="[type 'copy-roles' to continue or anything else to abort]: ",
            show_choices=False,
        )
        if do_copy == "copy-roles":
            target_alma_client.update_alma_roles(source_roles, target_user)
            click.echo("Roles copied.")
        else:
            click.echo("Copy operation cancelled.")


def print_user_roles(roles: list) -> str:
    """Print a nicely formatted table of alma user roles."""
    roles_tab = [
        {
            "status": role["status"]["desc"],
            "role_type": role["role_type"]["desc"],
            "scope": role["scope"].get("desc"),
        }
        for role in roles
    ]
    return tabulate(roles_tab, headers="keys")
