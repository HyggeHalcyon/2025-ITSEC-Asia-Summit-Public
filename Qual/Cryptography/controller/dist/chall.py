#!/usr/bin/env python3
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
from secret import flag


user_database = []
class User:
    def __init__(self, username, password, isAdmin, tag):
        self.username = username
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.isAdmin = isAdmin
        self.tag = tag

class signature():
    def __init__(self, key):
        self.key = key
        self.blocksize = 16
        self.iv = b"\x00" * self.blocksize

    def tag(self, m):
        m = bytes.fromhex(m)
        if len(m) % 16 != 0:
            m = pad(m, self.blocksize)
        c1 = AES.new(self.key, AES.MODE_CBC, iv = self.iv).encrypt(m)
        return c1[-self.blocksize:].hex()

    def verify(self, m, tag):
        return self.tag(m) == tag

def check_availibility(username):
    for i in user_database:
        if username == i.username:
            return False
    return True

def check_userpass(username, password):
    for i in user_database:
        if username == i.username:
            return hashlib.md5(password).hexdigest() == i.password
    return False

def check_usertoken(username, token):
    for i in user_database:
        if username == i.username:
            return token == i.tag
    return False

def check_privilege(username):
    for i in user_database:
        if username == i.username:
            return i.isAdmin
    return False


def main():
    bebek = signature(os.urandom(16))
    user_database.append(User(b"thegreatestadminsinthewholeworld", os.urandom(16).hex(), True, bebek.tag(b"thegreatestadminsinthewholeworld".hex())))

    print("===HAPPY HAPPY ITSEC aCCounT PAGE==")
    while True:
        print("1. Register")
        print("2. Login")
        choice = input(">> ")
        try:
            if choice == "1":
                regis_user = input("Username (hex): ")
                regis_password = input("Password: ")
                avail = check_availibility(bytes.fromhex(regis_user))
                if avail:
                    user_database.append(User(bytes.fromhex(regis_user), regis_password, False, bebek.tag(regis_user)))
                    auth_token = bebek.tag(regis_user)
                    print("User successfully registered!")
                    print(f"your authentication token: {auth_token}")
                else:
                    print("User already exist!")

            elif choice == "2":
                print("a. Login with password")
                print("b. Login with token")
                login_choice = input(">> ")
                if login_choice == "a":
                    login_user = bytes.fromhex(input("Username (hex): "))
                    login_pass = input("Password: ")
                    result = check_userpass(login_user, login_pass.encode())
                    if result:
                        print(f"Hello {login_user.decode()}, You are logged in!")
                        priv = check_privilege(login_user)
                        if priv:
                            print(f"As a superadmin, here's your flag: {flag}")
                        else:
                            print("Too bad you are not superadmin")
                    else:
                        print("Login failed!") 
                elif login_choice == "b":
                    login_user = bytes.fromhex(input("Username (hex): "))
                    login_token = input("Token: ")
                    result = check_usertoken(login_user, login_token)
                    if result:
                        print(f"Hello {login_user.decode()}, You are logged in!")
                        priv = check_privilege(login_user)
                        if priv:
                            print(f"As a superadmin, here's your flag: {flag}")
                        else:
                            print("Too bad you are not superadmin")
                    else:
                        print("Login failed!")
            elif choice == "3":
                exit()
        except:
            print("Application Error!")

if __name__ == '__main__':
    main()