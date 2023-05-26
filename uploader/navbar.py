from flask import session, url_for

from uploader.Transfer import helpers


class NavBarItem:
    label = ""  # Navigation link text
    route = ""  # Route ("transfer.index" for example)

    def __init__(self, label, route):
        self.label = label
        self.route = route

    def get_url(self):
        return url_for(self.route)

    def is_visible(self):
        transfer_directory = helpers.get_transfer_directory()
        always_visible = ["transfer.index", "dataverse.index", "job.index"]
        return self.route in always_visible or transfer_directory

    def is_active(self, request):
        # Determine which Blueprint this navigation item is part of
        route_blueprint = self.route.split(".")[0]

        return route_blueprint == request.blueprint


class NavBar:
    items = []

    def add(self, label, route):
        self.items.append(NavBarItem(label, route))
