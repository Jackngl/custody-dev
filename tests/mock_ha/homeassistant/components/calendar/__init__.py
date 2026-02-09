from enum import IntFlag


class CalendarEntityFeature(IntFlag):
    CREATE_EVENT = 1
    DELETE_EVENT = 2
    UPDATE_EVENT = 4


class CalendarEvent:
    def __init__(self, summary, start, end, location=None, description=None, uid=None):
        self.summary = summary
        self.start = start
        self.end = end
        self.location = location
        self.description = description
        self.uid = uid
