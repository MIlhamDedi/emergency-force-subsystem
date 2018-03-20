from datetime import datetime, date


class Asset:
    """Asset Data Object
    Data attributes structure:
        [
            ...
            (index: int, name: str, availability: int)
            ...
        ]
    """
    def __init__(self, data):
        try:
            self.json = dict()
            for _ in data:
                assert type(_[1]) == str
                assert type(_[2]) == int
                self.json[_[0]] = {
                    "Name": _[1],
                    "Availability": _[2],
                }
        except AssertionError:
            print("Found an issue in the Database")
            raise TypeError("Wrong type for Asset attributes")


class Plan:
    """Plan Data Object
    Data attributes structure:
        [
            ...
            (index: int, details: str, timestamp: datetime.datetime)
            ...
        ]
    """
    def __init__(self, data):
        try:
            self.json = dict()
            for _ in data:
                assert type(_[1]) == str
                assert type(_[2]) == datetime
                self.json[_[0]] = {
                    "details": _[1],
                    "time": str(_[2]),
                }
        except AssertionError:
            print("Found an issue in the Database")
            raise TypeError("Wrong type for Plan Attributes")


class Report:
    """Report Data Object
    Data attributes structure:
        [
            ...
            (index: int, summary: str, date: datetime.date)
            ...
        ]
    """
    def __init__(self, data):
        try:
            self.json = dict()
            for _ in data:
                assert type(_[1]) == str
                assert type(_[2]) == date
                self.json[_[0]] = {
                    "summary": _[1],
                    "time": str(_[2]),
                }
        except AssertionError:
            print("Found an issue in the Database")
            raise TypeError("Wrong type for Report attributes")


class Crisis:
    """Crisis Data Object
    Attributes:
        1. uid: int
        2. name: str
        3. crisis_type: str
        4. description: str
    """
    def __init__(self, uid, name, crisis_type, desc):
        try:
            assert type(uid) == int
            assert type(uid) == int
            assert type(uid) == int
            assert type(uid) == int
            self.uid = uid
            self.name = name
            self.crisis_type = crisis_type
            self.desc = desc
        except AssertionError:
            raise TypeError("Wrong type for Crisis Attributes")
