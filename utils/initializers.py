import datetime

import bson


class Date:
    def __init__(self) -> None:
        self.value = None
        self.testing = False

    def set_test_value(self, value):
        self.value = value
        self.testing = True

    def get_new_value(self):
        if self.testing:
            return self.value
        return datetime.datetime.now()


class ObjectId:
    def __init__(self) -> None:
        self.value = None
        self.testing = False

    def set_test_value(self, value):
        self.value = bson.ObjectId(value)
        self.testing = True

    def get_new_value(self):
        if self.testing:
            return self.value
        return bson.ObjectId()


app_date = Date()
app_objectid = ObjectId()


def get_new_date():
    return app_date.get_new_value()


def get_new_objectid():
    return app_objectid.get_new_value()


def set_new_date(value):
    return app_date.set_test_value(value)


def set_new_objectid(value):
    return app_objectid.set_test_value(value)
