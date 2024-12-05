import tkinter as tk
from tkinter import messagebox
from ticket_system import TicketBookingSystem, Customer, Admin, SingleDayPass, TwoDayPass, AnnualMembership, ChildTicket, GroupTicket, VIPExperiencePass

class TicketBookingGUI:
    def __init__(self, master):
        # Initialize the Ticket Booking System and the GUI
        self.system = TicketBookingSystem()
        self.master = master
        self.master.title("Adventure Land Ticket Booking")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.user = None  # Currently logged-in user
        self.login_screen()  # Start with the login screen

    def login_screen(self):
        # Clear the frame and show the login/registration screen
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
            # Show an error if fields are empty
            messagebox.showerror("Error", "Both fields are required!")
            return

        user_id = f"{name.lower().replace(' ', '')}_{email.split('@')[0]}"
        user = self.system.get_user(user_id)
        if user:
            # Existing user, log them in
            self.user = user
            messagebox.showinfo("Welcome Back", f"Welcome back, {self.user.get_name()}!")
        else:
            # New user, register them
            self.user = Customer(user_id, name, email)
            self.system.register_user(self.user)
            messagebox.showinfo("Registration Successful", f"Account created for {self.user.get_name()}!")

        self.ticket_selection_screen()

    def ticket_selection_screen(self):
        # Show the ticket selection screen
        self.clear_frame()

        tk.Label(self.frame, text="Select a Ticket").pack(pady=10)

        self.ticket_var = tk.StringVar()  # Variable to hold selected ticket type
        for ticket_class in [SingleDayPass, TwoDayPass, AnnualMembership, ChildTicket, GroupTicket, VIPExperiencePass]:
            ticket = ticket_class(ticket_class.__name__)
            # Display ticket options as radio buttons
            tk.Radiobutton(
                self.frame, text=f"{ticket.get_description()} - {ticket.get_price()} DHS",
                variable=self.ticket_var, value=ticket_class.__name__
            ).pack(anchor="w")

        tk.Button(self.frame, text="Purchase", command=self.purchase_ticket).pack(pady=10)

    def purchase_ticket(self):
        # Handle ticket purchase
        ticket_class_name = self.ticket_var.get()
        if not ticket_class_name:
            # Show an error if no ticket is selected
            messagebox.showerror("Error", "Please select a ticket!")
            return

        ticket_class = globals()[ticket_class_name]
        ticket = ticket_class(f"T{len(self.system.get_tickets()) + 1}")  # Create a new ticket
        self.user.add_to_history(ticket)  # Add ticket to user's purchase history
        self.system.add_ticket(ticket)  # Add ticket to the system
        messagebox.showinfo("Success", f"Purchased: {ticket.get_description()}!")
        self.invoice_screen()

    def invoice_screen(self):
        # Show the invoice screen
        self.clear_frame()

        tk.Label(self.frame, text="Invoice").pack(pady=10)
        for ticket in self.user.get_purchase_history():
            # Display all purchased tickets
            tk.Label(self.frame, text=ticket.display_ticket_info()).pack(anchor="w")

        tk.Button(self.frame, text="Logout", command=self.login_screen).pack(pady=10)

    def clear_frame(self):
        # Clear all widgets from the current frame
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    app = TicketBookingGUI(root)  # Initialize the Ticket Booking GUI
    root.mainloop()  # Start the main GUI event loop
