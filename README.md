Генератор фиктивных данных

Версия 1.0

Автор: Копанова Арина

Описание

Данное приложение является реализацией генератора фиктивных данных.
Результатом генерации является генератор Dummydata с 8-ю атрибутами: имя, фамилия, возраст, номер телефона, город, страна, email
Также поддерживается генерация из добавленных пользователем баз данных 

Требования

Python версии не ниже 3.4

Состав

Консольная версия: dummydata.py
Тесты: tests.py
База данных: database_dir/

Консольная версия

Справка: ./dummydata.py -h

Пример запуска: ./dummydata.py 5 40 -p "all" -c "example.json"

Пример вывода: 

Name: Earle;
LastName: Saldibar;
Age: 32;
PhoneNumber: +236(522)-822-022;
Email: Earle.Saldibar@hotmail.com;
Country: Central African Republic;
City: Bangui;