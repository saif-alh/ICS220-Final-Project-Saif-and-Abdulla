import tkinter as tk
from tkinter import ttk, messagebox
from ticket_system import TicketBookingSystem, Customer, SingleDayPass, TwoDayPass, AnnualMembership, ChildTicket, GroupTicket, VIPExperiencePass, Payment, Booking

class TicketBookingGUI:
    def __init__(self, master):
        # Initialize the GUI and Ticket Booking System
        self.system = TicketBookingSystem()
        self.master = master
        self.master.title("Adventure Land Ticket Booking")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.user = None  # Current logged-in user
        self.selected_tickets = []  # Store tickets selected for purchase

        self.login_screen()  # Start with the login screen

    def login_screen(self):
        # Login or Registration screen
        self.clear_frame()

        tk.Label(self.frame, text="Adventure Land Ticket Booking").pack(pady=10)
        tk.Label(self.frame, text="Name:").pack()
        self.name_entry = tk.Entry(self.frame)  # Entry for name
        self.name_entry.pack()
        tk.Label(self.frame, text="Email:").pack()
        self.email_entry = tk.Entry(self.frame)  # Entry for email
        self.email_entry.pack()
        tk.Button(self.frame, text="Register/Login", command=self.register_or_login).pack(pady=10)

    def register_or_login(self):
        # Handle user registration or login
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not name or not email:
            # Show error if fields are empty
            messagebox.showerror("Error", "Both fields are required!")
            return

        user_id = f"{name.lower().replace(' ', '')}_{email.split('@')[0]}"
        user = self.system.get_user(user_id)

        if user:
            # User exists, log in
            self.user = user
            messagebox.showinfo("Welcome Back", f"Welcome back, {self.user.get_name()}!")
        else:
            # Register new user
            self.user = Customer(user_id, name, email)
            self.system.register_user(self.user)
            messagebox.showinfo("Account Created", f"Account created for {self.user.get_name()}!")

        self.ticket_selection_screen()

    def ticket_selection_screen(self):
        # Screen for selecting tickets
        self.clear_frame()

        tk.Label(self.frame, text="Select Tickets").pack(pady=10)

        self.ticket_quantities = {}  # Dictionary to store ticket type and quantities
        for ticket_class in [SingleDayPass, TwoDayPass, AnnualMembership, ChildTicket, GroupTicket, VIPExperiencePass]:
            ticket = ticket_class("temp_id")  # Create a temporary ticket to display info
            quantity_var = tk.IntVar(value=0)
            self.ticket_quantities[ticket_class] = quantity_var
            tk.Label(self.frame, text=f"{ticket.get_description()} - {ticket.get_price()} DHS").pack(anchor="w")
            tk.Spinbox(self.frame, from_=0, to=10, textvariable=quantity_var, width=5).pack(anchor="w")

        tk.Button(self.frame, text="Proceed to Payment", command=self.payment_page).pack(pady=10)

    def payment_page(self):
        # Screen for entering payment details
        self.selected_tickets = []

        # Collect selected tickets
        for ticket_class, quantity_var in self.ticket_quantities.items():
            quantity = quantity_var.get()
            for _ in range(quantity):
                ticket_id = f"T{len(self.system.get_tickets()) + len(self.selected_tickets) + 1}"
                ticket = ticket_class(ticket_id)
                self.selected_tickets.append(ticket)

        if not self.selected_tickets:
            # Show error if no tickets selected
            messagebox.showerror("Error", "Please select at least one ticket!")
            return

        self.clear_frame()
        tk.Label(self.frame, text="Payment Page").pack(pady=10)

        # Payment form fields
        tk.Label(self.frame, text="Payment Method:").pack()
        self.payment_method = ttk.Combobox(self.frame, values=["Credit Card", "Debit Card", "PayPal", "Apple Pay"])
        self.payment_method.pack()
        tk.Label(self.frame, text="Name on Card:").pack()
        self.name_on_card_entry = tk.Entry(self.frame)
        self.name_on_card_entry.pack()
        tk.Label(self.frame, text="Card Number:").pack()
        self.card_number_entry = tk.Entry(self.frame)
        self.card_number_entry.pack()
        tk.Label(self.frame, text="Expiry Date:").pack()
        self.expiry_date_entry = tk.Entry(self.frame)
        self.expiry_date_entry.pack()
        tk.Label(self.frame, text="CVC:").pack()
        self.cvc_entry = tk.Entry(self.frame)
        self.cvc_entry.pack()
        tk.Button(self.frame, text="Submit Payment", command=self.process_payment).pack(pady=10)

    def process_payment(self):
        # Process payment and complete booking
        payment_method = self.payment_method.get()
        name_on_card = self.name_on_card_entry.get()
        card_number = self.card_number_entry.get()
        expiry_date = self.expiry_date_entry.get()
        cvc = self.cvc_entry.get()

        if not all([payment_method, name_on_card, card_number, expiry_date, cvc]):
            # Show error if any field is empty
            messagebox.showerror("Error", "All payment fields are required!")
            return

        # Create payment object
        payment = Payment(payment_method, name_on_card, card_number, expiry_date, cvc)
        booking_id = f"B{len(self.system.get_bookings()) + 1}"
        booking = Booking(booking_id, self.user, self.selected_tickets, payment)

        # Save booking and tickets
        self.user.add_to_history(self.selected_tickets)
        self.system.add_tickets(self.selected_tickets)
        self.system.add_booking(booking)

        # Display invoice
        self.invoice_screen(booking)

    def invoice_screen(self, booking):
        # Screen to display the invoice
        self.clear_frame()

        tk.Label(self.frame, text="Invoice").pack(pady=10)
        tk.Label(self.frame, text=booking.display_booking()).pack(anchor="w")
        tk.Button(self.frame, text="Logout", command=self.login_screen).pack(pady=10)

    def clear_frame(self):
        # Clear all widgets from the current frame
        for widget in self.frame.winfo_children():
            widget.destroy()

# Main entry point for the GUI application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = TicketBookingGUI(root)  # Initialize the GUI
    root.mainloop()  # Start the Tkinter event loop
