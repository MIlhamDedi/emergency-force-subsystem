from datetime import datetime, date


class Asset:
    """Asset Data Object
    Attributes:
        1. name: str
        2. availability: int
    """
    def __init__(self, name, availability):
        try:
            assert type(name) == str
            assert type(availability) == int
            self.name = name
            self.availability = availability
        except AssertionError:
            raise TypeError("Wrong type for Asset attributes")


class Plan:
    """Plan Data Object
    Attributes:
        1. details: str
        2. time: struct_time (import from `time` library)
    """
    def __init__(self, details, time):
        try:
            assert type(details) == str
            assert type(time) == datetime
            self.details = details
            self.time = str(time)
        except AssertionError:
            raise TypeError("Wrong type for Plan attributes")


class Report:
    """Report Data Object
    Attributes:
        1. summary: str
        2. time: struct_time (import from `time` library)
    """
    def __init__(self, summary, time):
        try:
            assert type(summary) == str
            assert type(time) == date
            self.summary = summary
            self.time = str(time)
        except AssertionError:
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
