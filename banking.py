import random
import numpy as np
import sqlite3

conn = sqlite3.connect('card.s3db')

cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS card
    (id INTEGER,
    number TEXT,
    pin TEXT
    )
    ''')
conn.commit()
# cur.execute('delete from card')
# conn.commit()
def checkLuhn(cardNo):
    cardNo = str(cardNo)
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')

        if (isSecond == True):
            d = d * 2
        nSum += d // 10
        nSum += d % 10

        isSecond = not isSecond

    if (nSum % 10 == 0):
        return True
    else:
        return False

def luth_algo():
    number = str(400000) + str(random.randint(0, 999999999)).zfill(9)
    n = list(number)
    list_n = [int(i) for i in number]
    sum = 0
    for i in np.arange(0, len(number), 2):
        list_n[i] = 2 * list_n[i]
    for i in np.arange(len(list_n)):
        if list_n[i] > 9:
            list_n[i] = list_n[i] - 9
    for i in list_n:
        sum += i
    if sum % 10 == 0:
        n.append(str(0))
    else:
        string = str(10 - int(list(str(sum))[-1]))
        n.append(string)
    number = ('').join(n)
    return number

def create_account():
    number = str(luth_algo())
    pin = str(random.randint(0, 9999)).zfill(4)
    print('Your card has been created\nYour card number:\n' + (number))
    print('Your card PIN:\n' + pin)
    cur.execute('''INSERT INTO card (number, pin) VALUES (?, ?)''', (number, pin))
    conn.commit()

def validation(number, pin):
    number = str(input(("Enter your card number:")))
    pin = str(input("Enter your PIN:"))
    cur.execute('SELECT number, pin FROM card WHERE number=? AND pin=?', (number, pin))
    conn.commit()
    res = cur.fetchone()
    validated = 0
    if res:
        print('You have successfully logged in!\n')
        validated = 1
    else:
        print('Wrong card number or PIN!\n')
        validated = 0
    return validated, number, pin

def Balance(number, pin):
        query = f'select balance from card where number = {number} and pin = {pin}'
        cur.execute(query)
        conn.commit()
        balance = cur.fetchone()
        return balance

def add_amount(number, pin):

    print('Enter income:')
    income = int(input())

    query = f'select balance from card where number = {cn};'
    cur.execute(query)
    conn.commit()
    money = cur.fetchone()[0]

    query = f'update card set balance = {income + money} where number = {number} and pin = {pin};'
    cur.execute(query)
    conn.commit()
    print('Income was added!')

def transfer(cn, number):
    query = f'select balance from card where number = {cn};'
    cur.execute(query)
    conn.commit()
    money = cur.fetchone()[0]
    number = str(input('''Transfer\nEnter card number:\n'''))
    if cn == number:
        print("You can't transfer money to the same account!")
    r = checkLuhn(number)

    if r is False:
        print('Probably you made mistake in card number. Please try again!')
    if r:
        a_query = f'select number from card where number = {number};'
        cur.execute(a_query)
        conn.commit()
        res = cur.fetchone()

        if res:
            existing_balance_query = f'select balance from card where number = {number};'
            cur.execute(existing_balance_query)
            conn.commit()
            existing_balance = cur.fetchone()[0]
            print('Enter how much money you want to transfer:')
            amount = int(input())
            if amount <= money:
                summ = existing_balance + amount
                query = f'update card set balance = {summ} where number = {number};'
                cur.execute(query)
                conn.commit()
                print('Success!')
                money = money - amount
                query = f'update card set balance = {money} where number = {cn};'
                cur.execute(query)
                conn.commit()
            else:
                print('Not enough money!')
        if res is None:
            print("Such a card does not exist.")

def close_account(cn):
    query = f'delete from card where number = {cn}'
    cur.execute(query)
    conn.commit()
    print('The account has been closed!')

while True:
    print('1. Create an account\n2. Log into account\n0. Exit')
    response = int(input())
    if response == 1:
        create_account()
    if response == 2:
        global cn
        global cp
        result, cn, cp = validation(input, input)
        while result:
                print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')
                response = int(input())
                if response == 1:
                    balance = Balance(cn, cp)
                    print('Balance: ' + str(balance[0]))
                if response == 2:
                    add_amount(cn, cp)
                if response == 3:
                    transfer(cn, input)

                if response == 4:
                    close_account(cn)

                if response == 5:
                    print('You have successfully logged out!')
                    break
                if response == 0:
                    print('bye!')
                    break
    if response == 0:
        print('bye!')
        quit()

