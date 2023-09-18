import datetime

class Diary:
    def __init__(self, userid: int , diarydate: datetime, entryname: str, entrytype: str, calories: int):
        self.id=None
        self.userID = userid
        self.diarydate = diarydate
        self.entrydate = None
        self.entrytype = entrytype
        self.entryname = entryname
        self.calories = calories

    def __str__(self):
        return f"id: {self.id}, userid: {self.userID}, diarydate: {self.diarydate}, entrydate: {self.entrydate}, entrytype: {self.entrytype}, name: {self.entryname}, calories: {self.calories}"