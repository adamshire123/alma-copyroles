import os

import click
from requests.exceptions import HTTPError
from tabulate import tabulate

from copyroles.alma import AlmaClient


@click.group()
def cli() -> None:
    """CLI for CopyRoles."""


@cli.command()
@click.argument("source_username", type=str)
@click.argument("target_username", type=str)
@click.option(
    "-e",
    "--environment",
    type=click.Choice(["prod", "sandbox"], case_sensitive=False),
    required=True,
    help="The Alma environment(prod or sandbox) within which the roles will be copied.",
)
def copy_roles(
    source_username: str,
    target_username: str,
    environment: str,
) -> None:
    alma_api_keys = {}
    alma_api_keys["prod"] = os.environ["PROD_ALMA_API_KEY"]
    alma_api_keys["sandbox"] = os.environ["SANDBOX_ALMA_API_KEY"]
    alma_client = AlmaClient(alma_api_keys[environment])
    job_summary = (
        f"Source: \033[1m{source_username.upper()}\033[0m - "
        f"\033[1m{alma_client.alma_environment.upper()}\033[0m\n"
        f"Target: \033[1m{target_username.upper()}\033[0m - "
        f"\033[1m{alma_client.alma_environment.upper()}\033[0m\n"
    )
    click.echo("\n-- Copy Alma Roles --\n" + job_summary)

    if click.confirm("Continue and review roles?", default=False, abort=False):
        try:
            source_user = alma_client.get_alma_user(source_username)
            target_user = alma_client.get_alma_user(target_username)
        except HTTPError as e:
            error_message = f"Could not get user - {e.response.text}"
            raise click.ClickException(error_message) from e
        if click.confirm("review roles?"):
            click.echo(print_user_roles(source_user["user_role"]))
        do_copy = click.prompt(
            "\nCopy these Alma roles?\n"
            + job_summary
            + "\nWARNING: THIS OPERATION CANNOT BE UNDONE.\n",
            prompt_suffix="[type 'copy-roles' to continue or anything else to abort]: ",
            show_choices=False,
        )
        if do_copy == "copy-roles":
            try:
                alma_client.update_alma_roles(source_user["user_role"], target_user)
                click.echo("Roles copied.")
            except HTTPError as e:
                error_message = f"Could not update roles - {e.response.text}"
                raise click.ClickException(error_message) from e
        else:
            click.echo("Copy operation cancelled.")


@click.argument("username", type=str)
@click.option(
    "--source-env",
    type=click.Choice(["prod", "sandbox"], case_sensitive=False),
    required=True,
    default="prod",
    help="Environment of the source user (prod or sandbox).",
)
@click.option(
    "--target-env",
    type=click.Choice(["prod", "sandbox"], case_sensitive=False),
    required=True,
    default="sandbox",
    help="Environment of the target user (prod or sandbox).",
)
@cli.command()
def copy_user(username: str, source_env: str, target_env: str) -> None:
    if source_env == "sandbox" and target_env == "prod":
        message = "Cannot copy users from sandbox to prod environment."
        raise click.UsageError(message)
    click.echo("copy user")
    alma_api_keys = {}
    alma_api_keys["prod"] = os.environ["PROD_ALMA_API_KEY"]
    alma_api_keys["sandbox"] = os.environ["SANDBOX_ALMA_API_KEY"]
    source_alma_client = AlmaClient(alma_api_keys[source_env])
    target_alma_client = AlmaClient(alma_api_keys[target_env])
    job_summary = (
        f"Source: \033[1m{username.upper()}\033[0m - "
        f"\033[1m{source_alma_client.alma_environment.upper()}\033[0m\n"
        f"Target: \033[1m{username.upper()}\033[0m - "
        f"\033[1m{target_alma_client.alma_environment.upper()}\033[0m\n"
    )
    click.echo("\n-- Copy Alma User --\n" + job_summary)

    if click.confirm("Continue?", default=False, abort=False):
        try:
            source_user = source_alma_client.get_alma_user(username)
        except HTTPError as e:
            error_message = f"Could not get user - {e.response.text}"
            raise click.ClickException(error_message) from e
        try:
            target_alma_client.create_alma_user(source_user)
            click.echo("User copied.")
        except HTTPError as e:
            error_message = f"Could not create user - {e.response.text}"
            raise click.ClickException(error_message) from e


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
