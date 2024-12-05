import pickle

# Base Ticket class
class Ticket:
    def __init__(self, ticket_id, price, validity, description):
        # Initialize ticket with ID, price, validity, and description
        self._ticket_id = ticket_id
        self._price = price
        self._validity = validity
        self._description = description

    # Getter methods
    def get_ticket_id(self):
        return self._ticket_id

    def get_price(self):
        return self._price

    def get_validity(self):
        return self._validity

    def get_description(self):
        return self._description

    # Setter methods
    def set_ticket_id(self, ticket_id):
        self._ticket_id = ticket_id

    def set_price(self, price):
        self._price = price

    def set_validity(self, validity):
        self._validity = validity

    def set_description(self, description):
        self._description = description

    # Display ticket details
    def display_ticket_info(self):
        return f"ID: {self._ticket_id}, Price: {self._price} DHS, Validity: {self._validity}, Description: {self._description}"

# Subclasses for specific ticket types
class SingleDayPass(Ticket):
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 275, "1 Day", "Access for one day.")

class TwoDayPass(Ticket):
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 480, "2 Days", "Access for two consecutive days.")

class AnnualMembership(Ticket):
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 1840, "1 Year", "Unlimited access for one year.")

class ChildTicket(Ticket):
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 185, "1 Day", "Discounted ticket for children (3-12 years).")

class GroupTicket(Ticket):
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 220, "1 Day", "Special rate for groups of 10 or more.")

class VIPExperiencePass(Ticket):
    def __init__(self, ticket_id):
        super().__init__(ticket_id, 550, "1 Day", "Includes expedited access and reserved seating.")

# Payment class for managing payment details
class Payment:
    def __init__(self, payment_method, name_on_card, card_number, expiry_date, cvc):
        # Initialize payment attributes
        self._payment_method = payment_method
        self._name_on_card = name_on_card
        self._card_number = card_number
        self._expiry_date = expiry_date
        self._cvc = cvc

    # Getter methods
    def get_payment_method(self):
        return self._payment_method

    def get_name_on_card(self):
        return self._name_on_card

    def get_card_number(self):
        return self._card_number

    def get_expiry_date(self):
        return self._expiry_date

    def get_cvc(self):
        return self._cvc

    # Setter methods
    def set_payment_method(self, payment_method):
        self._payment_method = payment_method

    def set_name_on_card(self, name_on_card):
        self._name_on_card = name_on_card

    def set_card_number(self, card_number):
        self._card_number = card_number

    def set_expiry_date(self, expiry_date):
        self._expiry_date = expiry_date

    def set_cvc(self, cvc):
        self._cvc = cvc

    # Display payment details (excluding sensitive information)
    def display_payment_info(self):
        return f"Payment Method: {self._payment_method}, Name on Card: {self._name_on_card}"

# Invoice class for generating invoices
class Invoice:
    def __init__(self, invoice_id, tickets, payment):
        # Initialize invoice with ID, tickets, and payment details
        self._invoice_id = invoice_id
        self._tickets = tickets
        self._payment = payment

    # Getter methods
    def get_invoice_id(self):
        return self._invoice_id

    def get_tickets(self):
        return self._tickets

    def get_payment(self):
        return self._payment

    # Setter methods
    def set_invoice_id(self, invoice_id):
        self._invoice_id = invoice_id

    def set_tickets(self, tickets):
        self._tickets = tickets

    def set_payment(self, payment):
        self._payment = payment

    # Display invoice details
    def display_invoice(self):
        tickets_info = "\n".join([ticket.display_ticket_info() for ticket in self._tickets])
        payment_info = self._payment.display_payment_info()
        return f"Invoice ID: {self._invoice_id}\nTickets:\n{tickets_info}\n{payment_info}"

# Booking class for managing user bookings
class Booking:
    def __init__(self, booking_id, user, tickets, payment=None):
        # Initialize booking with ID, user, tickets, and optional payment
        self._booking_id = booking_id
        self._user = user
        self._tickets = tickets
        self._payment = payment

    # Getter methods
    def get_booking_id(self):
        return self._booking_id

    def get_user(self):
        return self._user

    def get_tickets(self):
        return self._tickets

    def get_payment(self):
        return self._payment

    # Setter methods
    def set_booking_id(self, booking_id):
        self._booking_id = booking_id

    def set_user(self, user):
        self._user = user

    def set_tickets(self, tickets):
        self._tickets = tickets

    def set_payment(self, payment):
        self._payment = payment

    # Display booking details
    def display_booking(self):
        tickets_info = "\n".join([ticket.display_ticket_info() for ticket in self._tickets])
        payment_info = self._payment.display_payment_info() if self._payment else "No payment details available."
        return f"Booking ID: {self._booking_id}\nUser: {self._user.get_name()}\nTickets:\n{tickets_info}\nPayment:\n{payment_info}"

# Base User class
class User:
    def __init__(self, user_id, name, email):
        # Initialize user with ID, name, and email
        self._user_id = user_id
        self._name = name
        self._email = email

    # Getter methods
    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    # Setter methods
    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_name(self, name):
        self._name = name

    def set_email(self, email):
        self._email = email

# Admin subclass for system administrators
class Admin(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        # Additional admin-specific methods can be added here

# Customer subclass for ticket purchasers
class Customer(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self._purchase_history = []

    # Getter methods
    def get_purchase_history(self):
        return self._purchase_history

    # Setter methods
    def set_purchase_history(self, purchase_history):
        self._purchase_history = purchase_history

    # Add tickets to purchase history
    def add_to_history(self, tickets):
        self._purchase_history.extend(tickets)

# TicketBookingSystem class for managing the entire system
class TicketBookingSystem:
    def __init__(self):
        # Initialize system with users, tickets, and bookings
        self._users = {}
        self._tickets = []
        self._bookings = []
        self.load_data()  # Load system data from file

    # Getter methods
    def get_users(self):
        return self._users

    def get_tickets(self):
        return self._tickets

    def get_bookings(self):
        return self._bookings

    # Setter methods
    def set_users(self, users):
        self._users = users

    def set_tickets(self, tickets):
        self._tickets = tickets

    def set_bookings(self, bookings):
        self._bookings = bookings

    # Register a new user
    def register_user(self, user):
        self._users[user.get_user_id()] = user
        self.save_data()

    # Add tickets to the system
    def add_tickets(self, tickets):
        self._tickets.extend(tickets)
        self.save_data()

    # Add a booking to the system
    def add_booking(self, booking):
        self._bookings.append(booking)
        self.save_data()

    # Save system data to file
    def save_data(self):
        with open("data.pkl", "wb") as file:
            pickle.dump({"users": self._users, "tickets": self._tickets, "bookings": self._bookings}, file)

    # Load system data from file
    def load_data(self):
        try:
            with open("data.pkl", "rb") as file:
                data = pickle.load(file)
                self._users = data.get("users", {})
                self._tickets = data.get("tickets", [])
                self._bookings = data.get("bookings", [])
        except FileNotFoundError:
            self._users = {}
            self._tickets = []
            self._bookings = []

    # Get a user by ID
    def get_user(self, user_id):
        return self._users.get(user_id)
