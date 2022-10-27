import pytest

from uploader.Navigator import permissions

PERMS = {
    "/test/transfer/images": "public",
    "/test/transfer/images/logos": "private",
    "/test/transfer/images/logos/hockey": "restricted",
    "/test/transfer/images/logos/hockey/pro": "public",
}


def test_get_and_set():
    perms = permissions.FilePermissions()
    perms.copy_from_dict(PERMS)
    perms.set("/test/transfer/images", "private")
    assert perms.get("/test/transfer/images") == "private"


def test_unset_permissions_of_descendants():
    perms = permissions.FilePermissions()
    perms.copy_from_dict(PERMS)
    perms.unset_permissions_of_descendants("/test/transfer/images/logos")

    assert perms.get("/test/transfer/images") == "public"
    assert perms.get("/test/transfer/images/logos") == "private"
    assert "/test/transfer/images/logos/hockey" not in perms.permissions
    assert "/test/transfer/images/logos/hockey/pro" not in perms.permissions


def test_get_inherited_permission_of_directory_none(fs):
    # Create virtual directory structure so directory check won't raise an exception
    fs.create_dir("/test/transfer")

    perms = permissions.FilePermissions()
    perms.copy_from_dict(PERMS)

    perm = perms.get_inherited_permission_of_directory("/test/transfer")

    assert perm is None


def test_get_inherited_permission_of_directory_invalid(fs):
    # Create virtual directory structure so we can try to access something not in it
    fs.create_dir("/test/transfer/images/logos")

    perms = permissions.FilePermissions()
    perms.copy_from_dict(PERMS)

    with pytest.raises(Exception):
        perm = perms.get_inherited_permission_of_directory("/fake")


def test_get_inherited_permission_of_directory_same_directory(fs):
    # Create virtual directory structure so directory check won't raise an exception
    fs.create_dir("/test/transfer/images/logos")

    perms = permissions.FilePermissions()
    perms.copy_from_dict(PERMS)

    perm = perms.get_inherited_permission_of_directory("/test/transfer/images/logos")

    assert perm == "private"


def test_get_inherited_permission_of_directory_inherit_from_parent(fs):
    # Create virtual directory structure so directory check won't raise an exception
    fs.create_dir("/test/transfer/images/logos/baseball")

    perms = permissions.FilePermissions()
    perms.copy_from_dict(PERMS)

    perm = perms.get_inherited_permission_of_directory(
        "/test/transfer/images/logos/baseball"
    )

    assert perm == "private"


def test_get_inherited_permission_of_directory_inherit_from_ancestor(fs):
    # Create virtual directory so directory check won't raise an exception
    fs.create_dir("/test/transfer/images/logos/baseball/teams")

    perms = permissions.FilePermissions()
    perms.copy_from_dict(PERMS)

    perm = perms.get_inherited_permission_of_directory(
        "/test/transfer/images/logos/baseball/teams"
    )

    assert perm == "private"
