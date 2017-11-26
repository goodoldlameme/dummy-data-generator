import random
import unittest
import re
import dummydata


names_list = dummydata.json_parsing('database_dir\\names.json')
lastnames_list = dummydata.json_parsing('database_dir\lastnames.json')
domains_list = dummydata.json_parsing('database_dir\domains.json')
citiesandcountries_dict = dummydata.json_parsing('database_dir\citiesandcountries.json')
phonecodes_dict = dummydata.json_parsing('database_dir\phonecodes.json')


class TestSorting(unittest.TestCase):

    def test_phonenumber_country_pair(self):
        generated_data = dummydata.generate("country", "phonenumber", times=1000)
        for g_data in generated_data:
            phonecode = re.split('\W+', g_data.PhoneNumber[1:])[0]
            self.assertIn(phonecode, phonecodes_dict[g_data.Country])


    def test_email(self):
        generated_data = dummydata.generate("name", "lastname", "email", times=1000)
        for g_data in generated_data:
            email_splitted = re.split('\W+', g_data.Email, 2)
            self.assertIn(email_splitted[0], names_list)
            self.assertIn(email_splitted[1], lastnames_list)
            self.assertIn(email_splitted[2], domains_list)


    def test_city_country_pair(self):
        generated_data = dummydata.generate("country", "city", times=1000)
        for g_data in generated_data:
            self.assertIn(g_data.City, citiesandcountries_dict[g_data.Country])


    def test_requests(self):
        generated_data = dummydata.generate("name", "lastname", "age", "phonenumber", "email", "country", "city", times=1000)
        generated_data1 = dummydata.generate("all", times=1000)
        for g_data in generated_data:
            for field in g_data:
                self.assertIsNotNone(field)
        for g_data in generated_data1:
            for field in g_data:
                self.assertIsNotNone(field)


    def test_age(self):
        for i in range(1000):
            age = random.randint(1,120)
            generated_data = dummydata.generate("age", times=1000, age=age)
            sum = 0
            for g_data in generated_data:
                sum += g_data.Age
            self.assertTrue(age - sum/1000 < 2)


    def test_customized(self):
        generated_data = dummydata.custom_generate('database_dir\\customized.json', times=100)
        for g_data in generated_data:
            self.assertIn(g_data,dummydata.json_parsing('database_dir\\customized.json'))


    def test_name(self):
        generated_data = dummydata.generate("name", times=1000)
        for g_data in generated_data:
            self.assertIn(g_data.Name, names_list)


    def test_lastname(self):
        generated_data = dummydata.generate("lastname", times=1000)
        for g_data in generated_data:
            self.assertIn(g_data.LastName, lastnames_list)


if __name__ == '__main__':
    unittest.main()