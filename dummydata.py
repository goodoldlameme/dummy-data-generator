import random
import json
import argparse
import sys

def json_parsing(filename):
    with open(filename, 'r') as raw_data:
        return json.load(raw_data)


names_list = json_parsing('database_dir\\names.json')
lastnames_list = json_parsing('database_dir\lastnames.json')
domains_list = json_parsing('database_dir\domains.json')
citiesandcountries_dict = json_parsing('database_dir\citiesandcountries.json')
phonecodes_dict = json_parsing('database_dir\phonecodes.json')


class DummyData:
    def __init__(self, **kwargs):
        try:
            self.Name = kwargs["name"]()
        except KeyError:
            self.Name = None
        try:
            self.LastName = kwargs["lastname"]()
        except KeyError:
            self.LastName = None
        try:
            self.Age = kwargs["age"][0](kwargs["age"][1])
        except KeyError:
            self.Age = None
        try:
            self.Email = kwargs["email"](name=self.Name, lastname=self.LastName)
        except KeyError:
            self.Email = None
        try:
            self.Country = kwargs["country"]()
        except KeyError:
            self.Country = None
        try:
            self.City = kwargs["city"](country=self.Country)
        except KeyError:
            self.City = None
        try:
            self.PhoneNumber = kwargs["phonenumber"](country=self.Country)
        except KeyError:
            self.PhoneNumber = None
        self._args_list = [self.Name, self.LastName, self.Age, self.PhoneNumber, self.Email, self.Country, self.City]

    def __iter__(self):
        return iter(self._args_list)

    def __str__(self):
        return " Name: {};\n LastName: {};\n Age: {};\n PhoneNumber: {};\n Email: {};\n Country: {};\n City: {};\n".\
            format(*self._args_list)


def generate(*args, times=1, age=30):
    average = age
    generated_type_default = {"name": generate_name, "lastname": generate_lastname, "age": [generate_age, average],
                              "phonenumber": generate_phonenumber, "email": generate_email, "country": generate_country,
                              "city": generate_city}
    generated_type = {}

    if args.__contains__("all"):
        return generate_multiple(times, generated_type_default)
    else:
        for i in generated_type_default.keys():
            if args.__contains__(i):
                generated_type[i] = generated_type_default[i]
        return generate_multiple(times, generated_type)


def generate_name():
    return random.choice(names_list)


def generate_lastname():
    return random.choice(lastnames_list)


def generate_age(average):
    return int(random.gauss(average, 10))


def generate_phonenumber(country=None):
    n = str(random.randint(10**8, 10**9-1))
    if country:
        return "+" + phonecodes_dict[country] + '(' + n[:3] + ')-' + n[3:6] + '-' + n[6:]
    else:
        return "+" + random.choice(list(phonecodes_dict.values())) + '(' + n[:3] + ')-' + n[3:6] + '-' + n[6:]


def generate_email(name=None, lastname=None):
    if not name or not lastname:
        name = random.choice(names_list)
        lastname = random.choice(lastnames_list)
    domain = random.choice(domains_list)
    email = name + '.' + lastname + "@" + domain
    return email


def generate_country():
    country = random.choice(list(citiesandcountries_dict.keys()))
    return country


def generate_city(country=None):
    if country:
        return random.choice(citiesandcountries_dict.get(country))
    else:
        cities = [random.choice(i) for i in citiesandcountries_dict.values()]
        return random.choice(cities)


def generate_multiple(times, generated_types):
    for x in range(times):
        yield DummyData(**generated_types)


def custom_generate(database, times=1):
    database_list = json_parsing(database)
    for i in range(times):
        yield random.choice(database_list)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''Generates dummy data with key -p: name, lastname, email, country, city, phonenumber, age.
Generates customized dummy data from json list file with key -c'''
    )
    parser.add_argument('times', nargs='?', help='Times to generate', type=int, default=1)
    parser.add_argument('age', nargs='?', help='Average age', type=int, default=30)
    parser.add_argument('-p', '--parameters', type=str, nargs='+', help='Built-in parameters to generate')
    parser.add_argument('-c', dest='filename', metavar='FILE',
                        help='Json-file with database for customized generation',
                        type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.filename is None and args.parameters is None:
        print("You forgot to enter params, for more info ask for help [-h]")
    else:
        if args.filename:
            data = custom_generate(args.filename, times=args.times)
            for i in data:
                print(i)
        if args.parameters:
            persons = generate(*args.parameters, times=args.times, age=args.age)
            for person in persons:
                print(person)


if __name__ == '__main__':
    main()
