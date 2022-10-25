from flask import session, url_for

from uploader.Transfer import helpers


class NavBarItem:
    label = "" # Navigation link text
    route = "" # Route ("transfer.index" for example)

    def __init__(self, label, route):
        self.label = label
        self.route = route

    def get_url(self):
        return url_for(self.route)

    def is_visible(self):
        transfer_directory = helpers.get_transfer_directory()
        return self.route != "navigator.index" or transfer_directory


class NavBar:
    items = []

    def add(self, label, route):
        self.items.append(NavBarItem(label, route))
