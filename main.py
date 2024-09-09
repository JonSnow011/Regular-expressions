import csv
import re
from pprint import pprint

# Чтение адресной книги в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Шаг 1: Обработка ФИО
for i in range(1, len(contacts_list)):  # Пропускаем заголовок
    fio = contacts_list[i][:3]  # берем первые три поля
    names = " ".join(fio).split(" ")  # разбиваем на части

    contacts_list[i][0] = names[0]  # lastname
    contacts_list[i][1] = names[1]  # firstname
    contacts_list[i][2] = names[2] if len(names) > 2 else ''  # surname

# Шаг 2: Форматирование телефонов
phone_pattern = re.compile(r'(\+7|8)?\s*[-(]?(\d{3})[-)]?\s*(\d{3})[-]?(\d{2})[-]?(\d{2})(\s*доб\.(\d+))?')

def format_phone(phone):
    match = phone_pattern.search(phone)
    if match:
        formatted = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(7):
            formatted += f" доб.{match.group(7)}"
        return formatted
    return phone

for i in range(1, len(contacts_list)):  # Пропускаем заголовок
    if contacts_list[i][5]:  # Если телефон указан
        contacts_list[i][5] = format_phone(contacts_list[i][5])

# Шаг 3: Объединение дублирующихся записей
contacts_dict = {}
for contact in contacts_list[1:]:  # Пропускаем заголовок
    key = (contact[0], contact[1])  # Ключ - Фамилия и Имя
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        # Объединяем данные, переписывая только незаполненные поля
        existing_contact = contacts_dict[key]
        for i in range(len(contact)):
            if existing_contact[i] == "":
                existing_contact[i] = contact[i]

# Получение итогового списка
contacts_list = [list(contacts_dict.values())[0]]  # Заголовок
contacts_list.extend(list(contacts_dict.values()))

# Сохранение получившихся данных в другой файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

# Проверка результатов с форматированием
headers = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Должность', 'Телефон', 'Email']
column_widths = [max(len(header), max(len(str(contact[i])) for contact in contacts_list)) for i, header in enumerate(headers)]

# Заголовок
for i, header in enumerate(headers):
    print(f"{header:<{column_widths[i]}}", end=' | ')
print()  # Перенос строки

# Разделитель
print('-' * (sum(column_widths) + len(headers) * 4 - 1))

# Данные
for contact in contacts_list[1:]:  # Пропускаем заголовок
    for i, value in enumerate(contact):
        print(f"{value:<{column_widths[i]}}", end=' | ')
    print()  # Перенос строки
