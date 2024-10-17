import pymongo
import hashlib

class Node:
    # Node structure for linked list
    def __init__(self, data, info: str):
        self.data = data  # User data containing password and balance
        self.acc = info   # Username
        self.next = None  # Pointer to the next node

class Linked:
    def __init__(self, collection):
        self.head = None  # Head of the linked list
        self.collection = collection  # MongoDB collection for users

    def add_user(self, username, password):
        # Create a new user node
        new_user = Node({'password': password, 'balance': 0}, username)
        if not self.head:
            self.head = new_user  # Set as head if list is empty
        else:
            current = self.head
            # Traverse to the end of the linked list
            while current.next:
                current = current.next
            current.next = new_user  # Append new user at the end

        # Insert user data into MongoDB
        user_data = {
            "username": username,
            "password": password,
            "balance": 0
        }
        self.collection.insert_one(user_data)

    def find_user(self, username):
        # Find a user in the linked list by username
        current = self.head
        while current:
            if current.acc == username:
                return current  # Return the user node if found
            current = current.next
        return None  # Return None if not found

class BankSystem:
    def __init__(self):
        # Initialize MongoDB connection
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["bank"]  # Database name
        self.users = self.db["users"]   # Users collection
        self.linked_list = Linked(self.users)  # Linked list for user management
        self.logged_in_user = None  # Currently logged-in user

    def hash_password(self, password):
        # Hash the password using SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, stored_password, provided_password):
        # Check if provided password matches the stored hashed password
        return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

    def is_valid_username(self, username):
        # Validate username length
        return len(username) >= 3

    def is_valid_password(self, password):
        # Validate password length
        return len(password) >= 4

    def register(self, username, password):
        # Register a new user
        if not self.is_valid_username(username):
            return "Invalid username. Must be at least 3 characters."

        if not self.is_valid_password(password):
            return "Invalid password. Must be at least 4 characters."

        if self.users.find_one({"username": username}):
            return "Username has been taken!!"

        hashed_password = self.hash_password(password)
        self.linked_list.add_user(username, hashed_password)
        return "Successfully Registered!!"

    def login(self, username, password):
        # Log in a user
        user = self.users.find_one({"username": username})
        if not user or not self.check_password(user["password"], password):
            return "Incorrect Username or Password!!"

        self.logged_in_user = user  # Set the logged-in user
        return f"Welcome {username}!!"

    def add_amount(self, amount):
        # Add amount to the logged-in user's balance
        if not self.logged_in_user:
            return "You Haven't Logged In!!"

        if amount <= 0:
            return "Amount must be greater than zero."

        self.users.update_one({"username": self.logged_in_user["username"]}, {"$inc": {"balance": amount}})
        self.logged_in_user["balance"] += amount  # Update local balance
        return f"Successfully Added! New balance: {self.logged_in_user['balance']}"

    def withdraw(self, amount):
        # Withdraw amount from the logged-in user's balance
        if not self.logged_in_user:
            return "You Haven't Logged In!!"

        if amount <= 0:
            return "Amount must be greater than zero."

        if self.logged_in_user["balance"] < amount:
            return "Not Enough Money!!"

        self.users.update_one({"username": self.logged_in_user["username"]}, {"$inc": {"balance": -amount}})
        self.logged_in_user["balance"] -= amount  # Update local balance
        return f"Successfully Withdrawn! New balance: {self.logged_in_user['balance']}"

    def transfer(self, to_username, amount):
        # Transfer amount to another user
        if not self.logged_in_user:
            return "Please log in first."

        to_user = self.users.find_one({"username": to_username})
        if not to_user:
            return "Receiver Doesn't Exist!!"

        if amount <= 0:
            return "Amount must be greater than zero."

        if self.logged_in_user["balance"] < amount:
            return "Not Enough Money!!"

        self.users.update_one({"username": self.logged_in_user["username"]}, {"$inc": {"balance": -amount}})
        self.users.update_one({"username": to_user["username"]}, {"$inc": {"balance": amount}})
        self.logged_in_user["balance"] -= amount  # Update local balance
        return "Successfully Transferred!!"

    def check_balance(self):
        # Check the balance of the logged-in user
        if not self.logged_in_user:
            return "You Haven't Logged In!!"
        return f"Your current balance is: {self.logged_in_user['balance']}"

def main():
    bank = BankSystem()  # Create a bank system instance

    while True:
        choice = input("1:Register\n2:Login\n3:Exit\n")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(bank.register(username, password))  # Register a new user

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            reply = bank.login(username, password)  # Log in user
            print(reply)
            if reply == "Incorrect Username or Password!!":
                continue

            while True:
                choice = input("1:Add Amount\n2:Withdraw Amount\n3:Transfer Money\n4:Check Balance\n5:Logout\n")
                if choice == '1':
                    amount = float(input("Enter amount to add: "))
                    print(bank.add_amount(amount))  # Add amount to balance
                    continue
                elif choice == '2':
                    amount = float(input("Enter amount to withdraw: "))
                    print(bank.withdraw(amount))  # Withdraw amount from balance
                    continue
                elif choice == '3':
                    to_username = input("Enter receiver's username: ")
                    amount = float(input("Enter amount to transfer: "))
                    print(bank.transfer(to_username, amount))  # Transfer amount to another user
                    continue
                elif choice == '4':
                    print(bank.check_balance())  # Check balance
                    continue
                elif choice == '5':
                    bank.logged_in_user = None  # Log out user
                    break
                else:
                    print("Unknown Input!!")

        elif choice == '3':
            print("Goodbye!!")  # Exit the program
            break
        else:
            print("Unknown Input!!")

if __name__ == "__main__":
    main()
