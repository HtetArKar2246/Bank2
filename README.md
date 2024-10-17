# Bank System

A simple bank management system implemented in Python using MongoDB for data storage. This application allows users to register, log in, add funds, withdraw money, transfer funds to other users, and check their balance.

## Features

- **User Registration**: Users can create an account with a username and password.
- **User Login**: Users can log in to access their account.
- **Add Amount**: Users can deposit money into their account.
- **Withdraw Amount**: Users can withdraw money from their account.
- **Transfer Money**: Users can transfer money to another user's account.
- **Check Balance**: Users can view their current balance.

## Technologies Used

- Python
- MongoDB
- Hashlib (for password hashing)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/htetarkar2246/server-client-vote-app.git
    cd your-repo-name
    ```

2. **Install dependencies**:
    Make sure you have Python installed, and then install `pymongo`:
    ```bash
    pip install pymongo
    ```

3. **Set up MongoDB**:
    - Ensure MongoDB is installed and running on your local machine. You can download it from [MongoDB's official website](https://www.mongodb.com/try/download/community).
    - Create a database named `bank`.

## Usage

1. Run the application:
    ```bash
    python bank_system.py
    ```

2. Follow the on-screen instructions to register, log in, and perform banking operations.

## Example Usage

- Register a new user:
    ```
    1:Register
    Enter username: user1
    Enter password: password123
    Successfully Registered!!
    ```

- Log in to the account:
    ```
    2:Login
    Enter username: user1
    Enter password: password123
    Welcome user1!!
    ```

- Add funds:
    ```
    1:Add Amount
    Enter amount to add: 100
    Successfully Added! New balance: 100
    ```

- Check balance:
    ```
    4:Check Balance
    Your current balance is: 100
    ```

- Withdraw funds:
    ```
    2:Withdraw Amount
    Enter amount to withdraw: 50
    Successfully Withdrawn! New balance: 50
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.
