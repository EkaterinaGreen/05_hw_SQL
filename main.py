import psycopg2

def create_db(conn):
    #Создание таблицы основных клиентских данных
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
    id SERIAL PRIMARY KEY, 
    client_name VARCHAR(100) NOT NULL, 
    client_surname VARCHAR(100) NOT NULL, 
    client_email VARCHAR(100) NOT NULL
    );
    """)
    '''Создание отдельной таблицы с клиентскими номерами'''
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_phones(
    id_phonenumber SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    client_phonenumber VARCHAR(20) UNIQUE);
    """)

def add_client(cur, first_name, client_surname, client_email):
    cur.execute("""
    INSERT INTO clients(client_name,client_surname, client_email) VALUES(%s, %s, %s);
    """, (first_name, client_surname, client_email))

def add_new_phonenumber(cur, client_id, phonenumber):
    '''Добавление нового номера телефона в таблицу client_phonenumbers'''
    cur.execute("""
    INSERT INTO client_phones(client_id, client_phonenumber) VALUES(%s, %s);
    """, (client_id, phonenumber))

def change_client_data():
    '''Изменение информации о клиенте'''
    print("Для изменения информации о клиенте, пожалуйста, введите нужную Вам команду.\n "
        "1 - изменить имя; 2 - изменить фамилию; 3 - изменить e-mail; 4 - изменить номер телефона")

    while True:
        command_symbol = int(input())
        if command_symbol == 1:
            input_id_for_changing_name = input("Введите id клиента имя которого хотите изменить: ")
            input_name_for_changing = input("Введите имя для изменения: ")
            cur.execute("""
            UPDATE clients SET client_name=%s WHERE id=%s;
            """, (input_name_for_changing, input_id_for_changing_name))
            break
        elif command_symbol == 2:
            input_id_for_changing_surname = input("Введите id клиента фамилию которого хотите изменить: ")
            input_surname_for_changing = input("Введите фамилию для изменения: ")
            cur.execute("""
            UPDATE clients SET client_surname=%s WHERE id=%s;
            """, (input_surname_for_changing, input_id_for_changing_surname))
            break
        elif command_symbol == 3:
            input_id_for_changing_email = input("Введите id клиента e-mail которого хотите изменить: ")
            input_email_for_changing = input("Введите e-mail для изменения: ")
            cur.execute("""
            UPDATE clients SET client_email=%s WHERE id=%s;
            """, (input_email_for_changing, input_id_for_changing_email))
            break
        elif command_symbol == 4:
            input_phonenumber_you_wanna_change = input("Введите номер телефона который Вы хотите изменить: ")
            input_phonenumber_for_changing = input("Введите новый номер телефона, который заменит собой старый: ")
            cur.execute("""
            UPDATE client_phones SET client_phonenumber=%s WHERE client_phonenumber=%s;
            """, (input_phonenumber_for_changing, input_phonenumber_you_wanna_change))
            break
        else:
            print("К сожалению, Вы ввели неправильную команду, пожалуйста, повторите ввод")


def delete_client_phonenumber():
    '''Удаление номера телефона клиента из таблицы client_phonenumbers'''
    input_id_for_deleting_phonenumber = input("Введите id клиента номер телефона которого хотите удалить: ")
    input_phonenumber_for_deleting = input("Введите номер телефона который хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phones WHERE client_id=%s AND client_phonenumber=%s
        """, (input_id_for_deleting_phonenumber, input_phonenumber_for_deleting))

def delete_client():
    '''Удаление имеющейся информации о клиенте'''
    input_id_for_deleting_client = input("Введите id клиента которого хотите удалить: ")
    input_client_surname_for_deleting = input("Введите фамилию клиента которого хотите удалить: ")
    with conn.cursor() as cur:
        #удаление связи с таблицей client_phonenumbers
        cur.execute("""
        DELETE FROM client_phones WHERE client_id=%s
        """, (input_id_for_deleting_client,))
        #удаление информации о клиенте из таблицы clients_Homework5
        cur.execute("""
        DELETE FROM clients WHERE id=%s AND client_surname=%s
        """, (input_id_for_deleting_client, input_client_surname_for_deleting))

def find_client():
    '''Поиск клиента по имени'''
    print("Для поиска информации о клиенте, пожалуйста, введите команду, где:\n "
          "1 - найти по имени; 2 - найти по фамилии; 3 - найти по e-mail; 4 - найти по номеру телефона")
    while True:
        input_command_for_finding = int(input("Введите команду для поиска информации о клиенте: "))
        if input_command_for_finding == 1:
            input_name_for_finding = input("Введите имя для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients AS ch5
            LEFT JOIN client_phones AS cp ON cp.id_phonenumber = ch5.id
            WHERE client_name=%s
            """, (input_name_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 2:
            input_surname_for_finding = input("Введите фамилию для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients AS ch5
            LEFT JOIN client_phones AS cp ON cp.id_phonenumber = ch5.id
            WHERE client_surname=%s
            """, (input_surname_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 3:
            input_email_for_finding = input("Введите email для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients AS ch5
            LEFT JOIN client_phones AS cp ON cp.id_phonenumber = ch5.id
            WHERE client_email=%s
            """, (input_email_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 4:
            input_phonenumber_for_finding = input("Введите номер телефона для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients AS ch5
            LEFT JOIN client_phones AS cp ON cp.id_phonenumber = ch5.id
            WHERE client_phonenumber=%s
            """, (input_phonenumber_for_finding,))
            print(cur.fetchall())
        else:
            print("К сожалению, Вы ввели неправильную команду, пожалуйста, повторите ввод")


with psycopg2.connect(database="postgres", user="postgres", host="localhost", password="119104") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, "Oliver", "Williams", "ol@g.com")
        add_client(cur, "Brian", "Kelly", "br@g.com")
        add_client(cur, "Jack", "Gibson", "ja@g.com")
        add_client(cur, "Edward", "Graham", "ed@g.com")
        add_client(cur, "Charley", "Grant", "ch@g.com")
        add_new_phonenumber(cur, 1, "11111111")
        add_new_phonenumber(cur, 2, "222222222")
        add_new_phonenumber(cur, 3, "3333333333")
        add_new_phonenumber(cur, 4, "44444444444")
        add_new_phonenumber(cur, 5, "555555555555")
        change_client_data()
        delete_client_phonenumber()
        delete_client()
        find_client()


conn.close()
