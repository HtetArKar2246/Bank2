import pymongo

class Node:
    # data structure
    def __init__(self, data, info: str):
        self.data = data
        self.ncc = info  # user input
        self.next = None

class Linked:
    def __init__(self, collection):
        self.head = None
        self.collection = collection

    def add_user(self, username, password):
        new_user = Node({'password': password, 'balance': 0}, username)
        if not self.head:
            self.head = new_user
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_user

        user_data = {
            "username": username,
            "password": password,
            "balance": 0
        }
        self.collection.insert_one(user_data)

    def find_user(self, username):
        current = self.head
        while current:
            if current.ncc == username:
                return current
            current = current.next
        return None

class BankSystem:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["bank"]
        self.users = self.db["users"]
        self.linked_list = Linked(self.users)
        self.logged_in_user = None

    def register(self, username, password):
        if self.users.find_one({"username": username}):
            reply: str = "Username has been taken!!"
            return reply
        self.linked_list.add_user(username, password)
        reply: str = "Successfully Registered!!"
        return reply

    def login(self, username, password):
        user = self.users.find_one({"username": username, "password": password})
        if not user:
            reply: str = "Incorrect Username or Password!!"
            return reply
        self.logged_in_user = user
        reply: str = "Welcome"+username+"!!"
        return reply

    def add_amount(self, amount):
        if not self.logged_in_user:
            reply: str = "You Haven't Logged In!!"
            return reply

        self.users.update_one({"username": self.logged_in_user["username"]}, {"$inc": {"balance": amount}})
        reply: str = "Successfully Added!!"
        return reply

    def transfer(self, to_username, amount):
        if not self.logged_in_user:
            return "Please log in first."

        to_user = self.users.find_one({"username": to_username})
        if not to_user:
            reply: str = "Receiver Doesn't Exist!!"
            return reply

        if self.logged_in_user["balance"] < amount:
            reply: str = "Not Enough Money!!"
            return reply

        self.users.update_one({"username": self.logged_in_user["username"]}, {"$inc": {"balance": -amount}})
        self.users.update_one({"username": to_user["username"]}, {"$inc": {"balance": amount}})
        reply: str = "Successfully Transferred!!"
        return reply

def main():
    bank = BankSystem()

    while True:
        choice = input("1:Register\n2:Login\n3:Exit\n")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(bank.register(username, password))

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            reply: str = bank.login(username, password)
            print(reply)
            if reply == "Incorrect Username or Password!!":
                continue
            choice = input("1:Add Amount\n2:Transfer Money\n3:Menu\n")
            if choice == '1':
                if bank.logged_in_user:
                    amount = float(input("Enter amount to add: "))
                    print(bank.add_amount(amount))
                else:
                    print("You Haven't Logged In!!")

            elif choice == '2':
                if bank.logged_in_user:
                    to_username = input("Enter receiver's username: ")
                    amount = float(input("Enter amount to transfer: "))
                    print(bank.transfer(to_username, amount))
                else:
                    print("You Haven't Logged In!!")
            elif choice == '3':
                continue
            else:
                print("Unknown Input!!")
                continue

        elif choice == '3':
            print("Goodbye!!")
            break

        else:
            print("Unknown Input!!")

if __name__ == "__main__":
    main()
