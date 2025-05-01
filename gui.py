from tkinter import *
from tkinter import messagebox
from AppController import *

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
    root.geometry("600x500")
    root.title("IM - Message")

    # Create frame for messages display
    messages_frame = Frame(root)
    messages_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Scrollbar for message history
    scrollbar = Scrollbar(messages_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Text widget to display messages
    msg_display = Text(messages_frame, wrap=WORD, yscrollcommand=scrollbar.set, state=DISABLED)
    msg_display.pack(fill=BOTH, expand=True)
    scrollbar.config(command=msg_display.yview)

    # Frame for message input and send button
    input_frame = Frame(root)
    input_frame.pack(fill=X, padx=10, pady=10)

    # Message input field
    message_var = StringVar()
    message_entry = Entry(input_frame, textvariable=message_var, width=50)
    message_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
    message_entry.focus()

    # Function to update message display
    def update_message_display():
        # Enable text widget for editing
        msg_display.config(state=NORMAL)
        msg_display.delete(1.0, END)  # Clear current content
        
        for msg in message_history:
            if msg['type'] == 'sent':
                # Format sent messages
                msg_display.insert(END, f"You: {msg['plaintext']}\n", 'sent')
                msg_display.tag_configure('sent', foreground='blue')
            else:
                # Format received messages
                msg_display.insert(END, f"Them: {msg['plaintext']}\n", 'received')
                msg_display.tag_configure('received', foreground='green')
        
        # Disable text widget to prevent editing
        msg_display.config(state=DISABLED)
        
        # Scroll to the bottom to show latest messages
        msg_display.see(END)
    
    # Function to send a message
    def send_message_gui():
        message = message_var.get().strip()
        if message:
            # From app controller
            if send_message(message):
                message_var.set("")  # Clear input field
                update_message_display()  # Update the display
    
    # Send button
    send_button = Button(input_frame, text="Send", command=send_message_gui)
    send_button.pack(side=RIGHT)
    
    # Bind Enter key to send message
    message_entry.bind("<Return>", lambda event: send_message_gui())
    
    # Function to periodically update the message display
    def periodic_update():
        update_message_display()
        root.after(1000, periodic_update)  # Schedule next update in 1 second
    
    # Start periodic updates
    periodic_update()
    
    # Function to handle window close
    def on_closing():
        disconnect()
        root.destroy()
    
    # Set the window close handler
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()