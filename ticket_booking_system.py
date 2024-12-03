import pickle
import os


class Ticket:
    def __init__(self, ticket_type, price, validity, description, discount=None):
        self.ticket_type = ticket_type
        self.price = price
        self.validity = validity
        self.description = description
        self.discount = discount

    def calculate_discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.purchase_history = []

    def add_purchase(self, ticket):
        self.purchase_history.append(ticket)

    def view_purchase_history(self):
        return self.purchase_history


class Admin:
    def __init__(self, admin_id, name):
        self.admin_id = admin_id
        self.name = name


class TicketBookingSystem:
    def __init__(self):
        self.tickets = self.load_data("tickets.pkl") or []
        self.users = self.load_data("users.pkl") or []
        self.admins = self.load_data("admins.pkl") or []
        self.ticket_sales = self.load_data("sales.pkl") or {}

    def add_ticket(self, ticket):
        self.tickets.append(ticket)
        self.save_data("tickets.pkl", self.tickets)

    def register_user(self, user):
        self.users.append(user)
        self.save_data("users.pkl", self.users)

    def add_admin(self, admin):
        self.admins.append(admin)
        self.save_data("admins.pkl", self.admins)

    def purchase_ticket(self, user_id, ticket_type):
        user = next((u for u in self.users if u.user_id == user_id), None)
        if not user:
            raise ValueError("User not found.")
        ticket = next((t for t in self.tickets if t.ticket_type == ticket_type), None)
        if not ticket:
            raise ValueError("Ticket type not available.")
        user.add_purchase(ticket)
        self.ticket_sales[ticket_type] = self.ticket_sales.get(ticket_type, 0) + 1
        self.save_data("sales.pkl", self.ticket_sales)
        self.save_data("users.pkl", self.users)

    def view_ticket_sales(self):
        return self.ticket_sales

    @staticmethod
    def save_data(filename, data):
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    @staticmethod
    def load_data(filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)
        return None
