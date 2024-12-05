import pickle

# Base Ticket class
class Ticket:
    # Ticket attributes include ID, price, validity, and description
    def __init__(self, ticket_id, price, validity, description):
        self._ticket_id = ticket_id
        self._price = price
        self._validity = validity
        self._description = description

    # Getters for Ticket attributes
    def get_ticket_id(self):
        return self._ticket_id

    def get_price(self):
        return self._price

    def get_validity(self):
        return self._validity

    def get_description(self):
        return self._description

    # Setters for Ticket attributes
    def set_ticket_id(self, ticket_id):
        self._ticket_id = ticket_id

    def set_price(self, price):
        self._price = price

    def set_validity(self, validity):
        self._validity = validity

    def set_description(self, description):
        self._description = description

    # Method to display ticket information
    def display_ticket_info(self):
        return f"ID: {self._ticket_id}, Price: {self._price} DHS, Validity: {self._validity}, Description: {self._description}"

# Subclasses for specific ticket types
class SingleDayPass(Ticket):
    # Single day pass ticket with fixed attributes
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 275, "1 Day", "Access for one day.")

class TwoDayPass(Ticket):
    # Two day pass ticket with fixed attributes
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 480, "2 Days", "Access for two consecutive days.")

class AnnualMembership(Ticket):
    # Annual membership with fixed attributes
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 1840, "1 Year", "Unlimited access for one year.")

class ChildTicket(Ticket):
    # Discounted ticket for children
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 185, "1 Day", "Discounted ticket for children (3-12 years).")

class GroupTicket(Ticket):
    # Group ticket with fixed attributes
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 220, "1 Day", "Special rate for groups of 10 or more.")

class VIPExperiencePass(Ticket):
    # VIP experience pass with fixed attributes
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 550, "1 Day", "Includes expedited access and reserved seating.")

# Base User class
class User:
    # User attributes include ID, name, email, and purchase history
    def __init__(self, user_id, name, email):
        self._user_id = user_id
        self._name = name
        self._email = email

    # Getters for User attributes
    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    # Setters for User attributes
    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_name(self, name):
        self._name = name

    def set_email(self, email):
        self._email = email

    # Method to display user information
    def display_user_info(self):
        return f"User ID: {self._user_id}, Name: {self._name}, Email: {self._email}"

# Admin subclass inherits from User
class Admin(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)

# Customer subclass inherits from User
class Customer(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self._purchase_history = []

    # Getters and setters for purchase history
    def get_purchase_history(self):
        return self._purchase_history

    def set_purchase_history(self, purchase_history):
        self._purchase_history = purchase_history

    # Add a ticket to purchase history
    def add_to_history(self, ticket):
        self._purchase_history.append(ticket)

    # View all tickets in purchase history
    def view_purchase_history(self):
        return [ticket.display_ticket_info() for ticket in self._purchase_history]

# TicketBookingSystem class manages users and tickets
class TicketBookingSystem:
    def __init__(self):
        self._users = {}
        self._tickets = []
        self.load_data()  # Load data from file if it exists

    # Getters and setters for tickets and users
    def get_users(self):
        return self._users

    def get_tickets(self):
        return self._tickets

    def set_users(self, users):
        self._users = users

    def set_tickets(self, tickets):
        self._tickets = tickets

    # Register a new user
    def register_user(self, user):
        self._users[user.get_user_id()] = user
        self.save_data()

    # Add a ticket to the system
    def add_ticket(self, ticket):
        self._tickets.append(ticket)
        self.save_data()

    # Save data to file using pickle
    def save_data(self):
        with open("data.pkl", "wb") as file:
            pickle.dump({"users": self._users, "tickets": self._tickets}, file)

    # Load data from pickle file
    def load_data(self):
        try:
            with open("data.pkl", "rb") as file:
                data = pickle.load(file)
                self._users = data["users"]
                self._tickets = data["tickets"]
        except FileNotFoundError:
            self._users = {}
            self._tickets = []

    # Retrieve a user by ID
    def get_user(self, user_id):
        return self._users.get(user_id)

    # Delete a user by ID
    def delete_user(self, user_id):
        if user_id in self._users:
            del self._users[user_id]
            self.save_data()

    # Modify user details
    def modify_user(self, user_id, new_name, new_email):
        if user_id in self._users:
            user = self._users[user_id]
            user.set_name(new_name)
            user.set_email(new_email)
            self.save_data()
