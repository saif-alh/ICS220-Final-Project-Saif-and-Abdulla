import tkinter as tk
from tkinter import messagebox
from ticket_booking_system import Ticket, User, TicketBookingSystem, Admin

# Initialize the system
system = TicketBookingSystem()

# Add sample tickets (if not already loaded)
if not system.tickets:
    system.add_ticket(Ticket("Single-Day Pass", 275, "1 Day", "Access for one day"))
    system.add_ticket(Ticket("Two-Day Pass", 480, "2 Days", "Access for two consecutive days", discount=10))
    system.add_ticket(Ticket("Annual Membership", 1840, "1 Year", "Unlimited access for one year", discount=15))
    system.add_ticket(Ticket("Child Ticket", 185, "1 Day", "Discounted ticket for children aged 3-12"))
    system.add_ticket(Ticket("VIP Experience Pass", 550, "1 Day", "Includes expedited access and reserved seating for shows"))

# Add an admin (if not already loaded)
if not system.admins:
    admin = Admin(1, "Admin User")
    system.add_admin(admin)


# GUI Functions
def register_user():
    name = name_entry.get()
    email = email_entry.get()
    if name and email:
        user_id = len(system.users) + 1
        user = User(user_id, name, email)
        system.register_user(user)
        messagebox.showinfo("Success", f"User registered successfully! User ID: {user_id}")
    else:
        messagebox.showerror("Error", "Please provide both name and email!")


def purchase_ticket():
    try:
        user_id = int(user_id_entry.get())
        ticket_type = ticket_type_entry.get()
        if not ticket_type:
            raise ValueError("Please specify a ticket type.")
        system.purchase_ticket(user_id, ticket_type)
        messagebox.showinfo("Success", f"Ticket '{ticket_type}' purchased successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def view_purchase_history():
    try:
        user_id = int(user_id_entry.get())
        user = next((u for u in system.users if u.user_id == user_id), None)
        if not user:
            raise ValueError("User not found!")
        history = "\n".join([f"{ticket.ticket_type} - {ticket.calculate_discounted_price()} DHS"
                             for ticket in user.view_purchase_history()])
        if history:
            messagebox.showinfo(f"Purchase History for User {user_id}", history)
        else:
            messagebox.showinfo(f"Purchase History for User {user_id}", "No purchases found.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def view_ticket_sales():
    sales = system.view_ticket_sales()
    sales_text = "\n".join([f"{ticket}: {count}" for ticket, count in sales.items()])
    if sales_text:
        messagebox.showinfo("Ticket Sales", sales_text)
    else:
        messagebox.showinfo("Ticket Sales", "No tickets sold yet.")


# GUI Setup
root = tk.Tk()
root.title("Adventure Land Ticket Booking System")

# User Registration
tk.Label(root, text="User Registration").grid(row=0, column=0, columnspan=2)
tk.Label(root, text="Name:").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="Email:").grid(row=2, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

tk.Button(root, text="Register User", command=register_user).grid(row=3, column=0, columnspan=2)

# Ticket Purchase
tk.Label(root, text="Purchase Ticket").grid(row=4, column=0, columnspan=2)
tk.Label(root, text="User ID:").grid(row=5, column=0)
user_id_entry = tk.Entry(root)
user_id_entry.grid(row=5, column=1)

tk.Label(root, text="Ticket Type:").grid(row=6, column=0)
ticket_type_entry = tk.Entry(root)
ticket_type_entry.grid(row=6, column=1)

tk.Button(root, text="Purchase Ticket", command=purchase_ticket).grid(row=7, column=0, columnspan=2)

# View Purchase History
tk.Button(root, text="View Purchase History", command=view_purchase_history).grid(row=8, column=0, columnspan=2)

# View Ticket Sales
tk.Button(root, text="View Ticket Sales", command=view_ticket_sales).grid(row=9, column=0, columnspan=2)

# Start GUI
root.mainloop()
