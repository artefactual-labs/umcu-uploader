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
