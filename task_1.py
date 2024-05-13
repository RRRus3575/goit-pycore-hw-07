from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        del self.data[name]

    def find(self, name):
        return self.data[name]
    
    def get_upcoming_birthdays(self):
        new_users = {}
        current_date = datetime.today().date()
        finish_date = current_date + timedelta(days=7)

        for user, record in self.data.items():
            if record.birthday:
                date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                now_year_date = date.replace(year=current_date.year)
                if current_date <= now_year_date <= finish_date:
                    weekday_number = now_year_date.weekday()
                    if weekday_number == 5:
                        correct_date = now_year_date + timedelta(days=2)
                        new_users[user] = correct_date
                    elif weekday_number == 6:
                        correct_date= now_year_date + timedelta(days=1)
                        new_users[user] = correct_date
                    else:
                        new_users[user] = date
        sorted_dates_dict = {key: value for key, value in sorted(new_users.items(), key=lambda item: item[1])}
        return sorted_dates_dict
