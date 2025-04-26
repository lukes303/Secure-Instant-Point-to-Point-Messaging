from tkinter import *
from tkinter import messagebox

# Password window
def password_window():

    user_config = {}

    # Config main password window
    password_window = Tk()
    password_window.geometry("400x300")
    password_window.title("IM - Password")


    # Password Instructions
    password_instruction = Label(password_window, text="Please enter your password below:")
    password_instruction.pack(pady=10)

    # Create a StringVar to track the password entry content
    password_var = StringVar()

    # Password entry
    password_entry = Entry(password_window, textvariable=password_var, width=35)
    password_entry.pack(pady=10)

    # mode - default to client
    mode = IntVar(value=0)

    # Function for toggling IP address field
    def toggle_ip_field():
        if mode.get() == 0:  # Client selected
            ip_entry.config(state=NORMAL)
        else:  # Server selected
            ip_entry.config(state=DISABLED)

    # Run options
    Radiobutton(password_window, text="Run as Client", variable=mode, value=0, command=toggle_ip_field).pack() # 0 - client
    Radiobutton(password_window, text="Run as Server", variable=mode, value=1, command=toggle_ip_field).pack() # 1 - server

    # Create a StringVar to track the IP entry content
    ip_var = StringVar()
    
    # Ip Instructions
    ip_instruction = Label(password_window, text="Please enter IP address below if you are the client:")
    ip_instruction.pack(pady=10)

    # Ip Address entry
    ip_entry = Entry(password_window, textvariable=ip_var, width=35)
    ip_entry.pack(pady=10)


    # Function for validation and connecting
    def validate_and_connect():
        password = password_var.get()
        ip = ip_var.get()
        
        # Password validation
        if not password.strip():
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        
        # IP address validation
        if mode.get() == 0 and not ip.strip():
            messagebox.showerror("Error", "IP address cannot be empty if client.")
            return
        
        # Connection comfirmation
        if mode.get() == 0:
            messagebox.showinfo("Success", f"Connecting as client with valid password.")
        else:
            messagebox.showinfo("Success", f"Connecting as server with valid password.")
        
        # Populate the result dictionary
        user_config["mode"] = mode.get()
        user_config["password"] = password
        user_config["ip"] = ip if mode.get() == 0 else None

        password_window.destroy()  # Close the password window

    # Function to handle cancel
    def cancel_connection():
        user_config.clear()  # Clear any existing configuration
        password_window.destroy()  # Close the window
    # Connect button
    connect_button = Button(password_window, text="Connect", command=validate_and_connect)
    connect_button.pack(padx=10)

    # Cancel button
    connect_button = Button(password_window, text="Cancel", command=cancel_connection)
    connect_button.pack(padx=10)

    toggle_ip_field()  # Set initial state
    password_window.mainloop()
        
    # Return dictionary with pass
    return user_config

# Main window
def message_window():

    root = Tk()
    root.geometry("420x420")
    root.title("IM - Message")

    root.mainloop()