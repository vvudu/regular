from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

#Функция на нормализацию номера
def normalize_phone(phone):
    pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?\s*[-.\s]?(\d{3})[-.\s]?(\d{2})[-.\s]?(\d{2})(?:\s*(?:доб\.?|добавочный|ext\.?|extension)?\s*(\d+))?'
    )
    match = pattern.search(phone)
    if match:
        parts = match.groups()
        formatted_phone = f'+7({parts[1]}){parts[2]}-{parts[3]}-{parts[4]}'
        if parts[5]:
            formatted_phone += f' доб.{parts[5]}'
        return formatted_phone
    return phone

#разбивка контакта
def process_contact(contact):
    fullname = " ".join(contact[:3]).split()
    lastname, firstname, surname = fullname[0], fullname[1], fullname[2] if len(fullname) > 2 else ""
    organization = contact[3] if contact[3] else ""
    position = contact[4] if contact[4] else ""
    phone = normalize_phone(contact[5]) if contact[5] else ""
    email = contact[6] if contact[6] else ""
    return (lastname, firstname, surname, organization, position, phone, email)

#слияние контактов
def merge_contacts(contacts_list):
    merged = {}
    for contact in contacts_list:
        lastname, firstname, surname, organization, position, phone, email = process_contact(contact)
        key = (lastname, firstname)
        if key not in merged:
            merged[key] = [lastname, firstname, surname, organization, position, phone, email]
        else:
            existing = merged[key]
            merged[key] = [
                lastname,
                firstname,
                surname if existing[2] == "" else existing[2],
                organization if existing[3] == "" else existing[3],
                position if existing[4] == "" else existing[4],
                phone if existing[5] == "" else existing[5],
                email if existing[6] == "" else existing[6]
            ]
    
    return list(merged.values())

#Запись
def main():   
    normalized_contacts = merge_contacts(contacts_list)
    normalized_contacts = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']] + normalized_contacts
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(normalized_contacts)

if __name__ == "__main__":
    main()
    
