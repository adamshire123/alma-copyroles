import pytest
from click.testing import CliRunner
from requests.exceptions import HTTPError

from copyroles.cli import cli, print_user_roles


@pytest.fixture
def roles():
    return [
        {
            "status": {"desc": "ACTIVE"},
            "role_type": {"desc": "Admin"},
            "scope": {"desc": "Institution"},
        },
        {
            "status": {"desc": "INACTIVE"},
            "role_type": {"desc": "User"},
            "scope": {"desc": "Library"},
        },
    ]


@pytest.fixture
def mock_alma_client(mocker):
    mocked_alma_client_class = mocker.patch("copyroles.cli.AlmaClient")
    mocked_client_instance = mocked_alma_client_class.return_value

    mocked_client_instance.alma_environment = "sandbox"
    mocked_client_instance.get_alma_user.side_effect = [
        {"primary_id": "sourceuser@example.com", "user_role": [{"role": "test"}]},
        {"primary_id": "targetuser@example.com", "user_role": []},
    ]
    mocked_client_instance.update_alma_roles.return_value = None
    return mocked_client_instance


@pytest.fixture
def mock_print_roles(mocker):
    return mocker.patch("copyroles.cli.print_user_roles", return_value="test")


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("SANDBOX_ALMA_API_KEY", "test_sandbox_api_key")


def test_print_user_roles(roles):
    expected = (
        "status    role_type    scope\n"
        "--------  -----------  -----------\n"
        "ACTIVE    Admin        Institution\n"
        "INACTIVE  User         Library"
    )
    assert print_user_roles(roles) == expected


def test_copy_user_sandbox_to_prod_raises_error(cli_runner):
    usage_error_code = 2

    result = cli_runner.invoke(
        cli, ["copy-user", "--source-env", "sandbox", "--target-env", "prod", "testuser"]
    )
    assert result.exit_code == usage_error_code
    assert "Cannot copy users from sandbox to prod environment." in result.output


def test_copy_roles_success(mock_alma_client, mock_print_roles, cli_runner):
    result = cli_runner.invoke(
        cli,
        [
            "copy-roles",
            "-e",
            "sandbox",
            "sourceuser@example.com",
            "targetuser@example.com",
        ],
        input="y\ny\ncopy-roles\n",
    )
    mock_print_roles.assert_called_once()
    mock_alma_client.get_alma_user.assert_any_call("sourceuser@example.com")
    mock_alma_client.get_alma_user.assert_any_call("targetuser@example.com")
    mock_alma_client.update_alma_roles.assert_called_once()
    assert "Roles copied" in result.output
    assert result.exit_code == 0


def test_copy_roles_get_user_error(mocker, mock_alma_client, cli_runner):
    mock_response = mocker.MagicMock()
    mock_response.text = "foo"
    mock_alma_client.get_alma_user.side_effect = HTTPError(response=mock_response)
    result = cli_runner.invoke(
        cli,
        ["copy-roles", "-e", "sandbox", "sourceuser", "targetuser"],
        input="y\ny\n",
    )
    assert result.exit_code == 1
    assert "Error: Could not get user - foo" in result.output


def test_copy_roles_update_roles_error(
    mock_print_roles, mocker, mock_alma_client, cli_runner
):
    mock_response = mocker.MagicMock()
    mock_response.text = "foo"
    mock_alma_client.update_alma_roles.side_effect = HTTPError(response=mock_response)
    result = cli_runner.invoke(
        cli,
        ["copy-roles", "-e", "sandbox", "sourceuser", "targetuser"],
        input="y\ny\ncopy-roles\n",
    )
    assert result.exit_code == 1
    assert "Error: Could not update roles - foo" in result.output


def test_copy_roles_cancelled(
    mock_print_roles, mocker, mock_env, mock_alma_client, cli_runner
):
    mock_response = mocker.MagicMock()
    mock_response.text = "foo"
    mock_alma_client.update_alma_roles.side_effect = HTTPError(response=mock_response)
    result = cli_runner.invoke(
        cli,
        ["copy-roles", "-e", "sandbox", "sourceuser", "targetuser"],
        input="y\ny\nfoo\n",
    )
    assert result.exit_code == 0
    assert "Copy operation cancelled" in result.output


def test_copy_user_default_success(mocker, mock_alma_client, cli_runner):
    """Test copy-user CLI command."""
    mock_click_echo = mocker.patch("click.echo")
    result = cli_runner.invoke(
        cli,
        ["copy-user", "username"],
        input="y\ny\ncopy-user\n",
    )

    mock_alma_client.get_alma_user.assert_called_once_with("username")
    mock_click_echo.assert_called_with("User copied.")
    assert result.exit_code == 0


def test_copy_user_get_user_error(mocker, mock_alma_client, cli_runner):
    mock_response = mocker.MagicMock()
    mock_response.text = "foo"
    mock_alma_client.get_alma_user.side_effect = HTTPError(response=mock_response)
    result = cli_runner.invoke(
        cli,
        ["copy-user", "username"],
        input="y\ny\n",
    )
    assert result.exit_code == 1
    assert "Error: Could not get user - foo" in result.output


def test_copy_user_create_user_error(mocker, mock_alma_client, cli_runner):
    mock_response = mocker.MagicMock()
    mock_response.text = "foo"
    mock_alma_client.create_alma_user.side_effect = HTTPError(response=mock_response)
    result = cli_runner.invoke(
        cli,
        ["copy-user", "username"],
        input="y\ny\n",
    )
    assert result.exit_code == 1
    assert "Error: Could not create user - foo" in result.output
