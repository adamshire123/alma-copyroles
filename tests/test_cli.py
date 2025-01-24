from copyroles.cli import print_user_roles


def test_print_user_roles():
    roles = [
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
    expected = (
        "status    role_type    scope\n"
        "--------  -----------  -----------\n"
        "ACTIVE    Admin        Institution\n"
        "INACTIVE  User         Library"
    )
    assert print_user_roles(roles) == expected
