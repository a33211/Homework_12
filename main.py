from collections import UserDict
from datetime import datetime, timedelta
import pickle
from pathlib import Path

class Field:
    def __init__(self, param):
        self._param = None
        self.param = param

    def __repr__(self):
        return f'{self.param}'

    @property
    def param(self):
        return self._param


class Name(Field):
    @Field.param.setter
    def param(self, param):
        self._param = param


class Phone(Field):
    @Field.param.setter
    def param(self, data):
        if len(data) == 13 or data.startswith('+380'):
            self._param = data
        else:
            raise ValueError("Phone is incorrect. Please enter phone in +380.. format. It's length should be 13 chars")
        print("setter method called")


class Birthday(Field):
    @Field.param.setter
    def param(self, data):
        try:
            self._param = datetime.strptime(data, '%d.%m.%Y').date()
        except:
            raise ValueError("Birthday format issue. Please enter b-day in DD.MM.YY format")


class Record:
    def __init__(self, name, phone=None, b_day=None):
        self.name = name
        self.b_day = b_day
        self.phones = []
        if phone:
            self.addPhone(phone)

    def __repr__(self):
        return f'{self.phones} {self.b_day.param if self.b_day else ""}'

    def addPhone(self, phone: Phone):
        self.phones.append(phone)

    def erasePhone(self, phone: Phone):
        for p in self.phones:
            if p.param == phone.param:
                self.phones.remove(p)

    def changePhone(self, phone: Phone, new_phone: Phone):
        for p in self.phones:
            if p.param == phone.param:
                self.erasePhone(p)
                self.addPhone(new_phone)

    def days_to_birthday(self):
        if not self.b_day:
            return None
        day_now = datetime.now().date()
        current_year = self.b_day.param.replace(year=day_now.year)
        if current_year > day_now:
            delta = current_year - day_now
            print(f'You have left {delta.days} to next birthday!')
            return delta
        else:
            next_b_day = current_year.replace(year=day_now.year + 1)
            delta = next_b_day - day_now
            print(f'You have left {delta.days} to next birthday!')
            return delta


class AddressBook(UserDict):
    def add_record(self, rec):
        self.data[rec.name.param] = rec

    def paginator(self, rec_num=2):
        print_str = ''
        i = 1
        for record in self.values():
            print_str += f'{record.name}~~~~{record.phones}\n'
            if i < rec_num:
                i += 1
            else:
                yield print_str + '\n'
                print_str = ''
                i = 1
        yield print_str + '\n'


#phone_book = AddressBook()
filename = 'database.bin'

def paginate(*args):
    for print_str in phone_book.paginator():
        print(print_str)


def add(*args):
    name = Name(args[0])
    try:
        phone = Phone(args[1])
    except ValueError as e:
        return e
    try:
        b_day = Birthday(args[2])
    except IndexError:
        b_day = None
    except ValueError as e:
        return e
    rec = Record(name, phone, b_day)
    phone_book.add_record(rec)
    print(phone_book)
    return f'Contact {name.param} add successful'


def erase_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = phone_book[name.param]
    if rec:
        rec.erasePhone(phone)
    print(phone_book)
    return f'Contact {phone.param} erase successful'


def adds_phone(*args):
    key = args[0]
    phone = Phone(args[1])
    value = phone_book.get(key)
    if value:
        value.addPhone(phone)
        print(phone_book)
    return phone_book


def change_phone(*args):
    key = args[0]
    phone = Phone(args[1])
    value = phone_book.get(key)
    new_phone = Phone(args[2])
    if new_phone:
        value.changePhone(phone, new_phone)
        print(f'Contact {value} changed successful')
    print(phone_book)
    return phone_book


def days_left(*args):
    print(*args)
    rec = phone_book.get(args[0])
    if rec:
        b_days_left = rec.days_to_birthday()
        print(f'b_days_left = {b_days_left}')


def exit(*args):
    return "Good bye!"


COMMANDS = {
    add: ["add"],
    adds_phone: ['append phone'],
    erase_phone: ["erase"],  # in command enter command, user, phone number to erase
    change_phone: ["change phone"],
    days_left: ['days left'],
    paginate: ['paginate'], # just type  paginate
    exit: ["good bye", "close", "exit"]
}


def parse_command(user_input: str):
    for komand, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                data = user_input[len(i):].strip().split(" ")
                return komand, data


def main():
    while True:
        user_input = input('Please enter your command in format command -> User -> phone number -> birthday date \n')
        result, data = parse_command(user_input)
        print(result(*data))
        if result is exit:
            break


if __name__ == '__main__':
    #main()
    file = Path(filename)
    if file.exists():
        with open(file, 'rb') as f:
            phone_book: AddressBook = pickle.load(f)
    else:
        phone_book = AddressBook()

    main()

    with open(file, "wb") as f:
        pickle.dump(phone_book, f)