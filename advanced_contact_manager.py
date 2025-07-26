import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Entry, Button

class Contact:
    """Represents a single contact with name, phone, and email."""
    def __init__(self, name, phone, email):
        if not name or not phone:
            raise ValueError("Name and Phone are required for a contact.")
        self.name = name.strip()
        self.phone = phone.strip()
        self.email = email.strip()

    def __str__(self):
        """String representation for display in the listbox."""
        return f"{self.name} | {self.phone} | {self.email}"

    def to_dict(self):
        """Converts contact to a dictionary for (future) saving."""
        return {"name": self.name, "phone": self.phone, "email": self.email}

class ContactManagerGUI:
    """Manages the GUI and contact operations."""
    def __init__(self, master):
        self.master = master
        master.title("Advanced Contact Manager")
        master.geometry("600x550")
        master.resizable(False, False)

        self.contacts = [] # List to store Contact objects

        self._create_widgets()
        self._load_sample_data() # Load some initial data for demonstration
        self.sort_contacts() # Initial sort

    def _create_widgets(self):
        """Initializes all GUI elements."""
        # --- Input Frame ---
        input_frame = tk.LabelFrame(self.master, text="Add New Contact", padx=10, pady=10)
        input_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.name_entry = tk.Entry(input_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.phone_entry = tk.Entry(input_frame, width=40)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.email_entry = tk.Entry(input_frame, width=40)
        self.email_entry.grid(row=2, column=1, padx=5, pady=2)

        add_button = tk.Button(input_frame, text="Add Contact", command=self.add_contact)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Contact List Frame ---
        list_frame = tk.LabelFrame(self.master, text="Your Contacts", padx=10, pady=10)
        list_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.contact_listbox = tk.Listbox(list_frame, width=80, height=12)
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.contact_listbox.bind("<Double-Button-1>", self._edit_selected_contact) # Double-click to edit

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.contact_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_listbox.config(yscrollcommand=scrollbar.set)

        # --- Action Buttons Frame ---
        action_frame = tk.Frame(self.master, padx=10, pady=5)
        action_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        edit_button = tk.Button(action_frame, text="Edit Selected", command=self._edit_selected_contact)
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(action_frame, text="Delete Selected", command=self.delete_selected_contact)
        delete_button.pack(side=tk.LEFT, padx=5)

        # --- Search and Sort Frame ---
        search_sort_frame = tk.LabelFrame(self.master, text="Search & Sort", padx=10, pady=10)
        search_sort_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Label(search_sort_frame, text="Search:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.search_entry = tk.Entry(search_sort_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=2)
        search_button = tk.Button(search_sort_frame, text="Search", command=self.search_contacts)
        search_button.grid(row=0, column=2, padx=5, pady=2)
        clear_search_button = tk.Button(search_sort_frame, text="Clear Search", command=self.refresh_contact_list)
        clear_search_button.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(search_sort_frame, text="Sort By:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.sort_var = tk.StringVar(self.master)
        self.sort_var.set("Name") # default value
        sort_option_menu = tk.OptionMenu(search_sort_frame, self.sort_var, "Name", "Phone", "Email", command=self.sort_contacts)
        sort_option_menu.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky="ew")

    def _load_sample_data(self):
        """Loads a few sample contacts for demonstration."""
        sample_contacts_data = [
            {"name": "Alice Smith", "phone": "123-456-7890", "email": "alice@example.com"},
            {"name": "Bob Johnson", "phone": "098-765-4321", "email": "bob@example.com"},
            {"name": "Charlie Brown", "phone": "111-222-3333", "email": "charlie@example.com"},
            {"name": "David Lee", "phone": "555-123-4567", "email": "david@example.com"},
        ]
        for data in sample_contacts_data:
            try:
                self.contacts.append(Contact(data["name"], data["phone"], data["email"]))
            except ValueError as e:
                print(f"Error loading sample contact: {e}") # For debugging

    def add_contact(self):
        """Adds a new contact to the list."""
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        try:
            new_contact = Contact(name, phone, email)
            self.contacts.append(new_contact)
            messagebox.showinfo("Success", "Contact added successfully!")
            self._clear_entries()
            self.sort_contacts() # Re-sort to maintain order
        except ValueError as e:
            messagebox.showwarning("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def _clear_entries(self):
        """Clears the input fields."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def refresh_contact_list(self, contact_list=None):
        """Refreshes the listbox display, optionally with a filtered list."""
        self.contact_listbox.delete(0, tk.END)
        display_list = contact_list if contact_list is not None else self.contacts
        if not display_list:
            self.contact_listbox.insert(tk.END, "No contacts to display.")
        else:
            for i, contact in enumerate(display_list):
                self.contact_listbox.insert(tk.END, contact.__str__())
        self.search_entry.delete(0, tk.END) # Clear search field after displaying results

    def search_contacts(self):
        """Searches contacts based on a query string."""
        query = self.search_entry.get().strip().lower()
        if not query:
            self.refresh_contact_list() # Show all if search query is empty
            return

        found_contacts = []
        for contact in self.contacts:
            if query in contact.name.lower() or \
               query in contact.phone.lower() or \
               query in contact.email.lower():
                found_contacts.append(contact)
        self.refresh_contact_list(found_contacts)
        if not found_contacts and query: # Only show message if query was not empty
            messagebox.showinfo("Search Results", f"No contacts found matching '{query}'.")

    def sort_contacts(self, *args):
        """Sorts the contacts list based on the selected criteria."""
        sort_by = self.sort_var.get()
        if sort_by == "Name":
            self.contacts.sort(key=lambda contact: contact.name.lower())
        elif sort_by == "Phone":
            self.contacts.sort(key=lambda contact: contact.phone)
        elif sort_by == "Email":
            self.contacts.sort(key=lambda contact: contact.email.lower())
        self.refresh_contact_list()

    def _edit_selected_contact(self, event=None):
        """Opens a dialog to edit the selected contact."""
        selection_indices = self.contact_listbox.curselection()
        if not selection_indices:
            messagebox.showwarning("No Selection", "Please select a contact to edit.")
            return

        # Get the actual Contact object based on the currently displayed list.
        # This is crucial for correctly editing filtered/sorted lists.
        selected_display_text = self.contact_listbox.get(selection_indices[0])
        original_contact = None
        for contact in self.contacts:
            if str(contact) == selected_display_text:
                original_contact = contact
                break

        if not original_contact:
            messagebox.showerror("Error", "Could not find selected contact for editing.")
            return

        # --- Create a new Toplevel window for editing ---
        edit_window = Toplevel(self.master)
        edit_window.title("Edit Contact")
        edit_window.transient(self.master) # Make it a modal dialog
        edit_window.grab_set() # Grab focus
        edit_window.focus_set()

        Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        edit_name_entry = Entry(edit_window, width=30)
        edit_name_entry.insert(0, original_contact.name)
        edit_name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(edit_window, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        edit_phone_entry = Entry(edit_window, width=30)
        edit_phone_entry.insert(0, original_contact.phone)
        edit_phone_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(edit_window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        edit_email_entry = Entry(edit_window, width=30)
        edit_email_entry.insert(0, original_contact.email)
        edit_email_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_changes():
            new_name = edit_name_entry.get()
            new_phone = edit_phone_entry.get()
            new_email = edit_email_entry.get()

            try:
                # Update the original contact object directly
                original_contact.name = new_name
                original_contact.phone = new_phone
                original_contact.email = new_email
                messagebox.showinfo("Success", "Contact updated successfully!")
                edit_window.destroy()
                self.sort_contacts() # Re-sort and refresh display
            except ValueError as e:
                messagebox.showwarning("Input Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        save_button = Button(edit_window, text="Save Changes", command=save_changes)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

        edit_window.wait_window(edit_window) # Wait for the edit window to close

    def delete_selected_contact(self):
        """Deletes the selected contact from the list."""
        selection_indices = self.contact_listbox.curselection()
        if not selection_indices:
            messagebox.showwarning("No Selection", "Please select a contact to delete.")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete the selected contact?"
        )
        if confirm:
            # Similar to edit, get the actual contact object
            selected_display_text = self.contact_listbox.get(selection_indices[0])
            contact_to_delete = None
            for contact in self.contacts:
                if str(contact) == selected_display_text:
                    contact_to_delete = contact
                    break

            if contact_to_delete:
                self.contacts.remove(contact_to_delete)
                messagebox.showinfo("Success", "Contact deleted.")
                self.refresh_contact_list() # Refresh to update display
            else:
                messagebox.showerror("Error", "Could not find selected contact to delete.")

    def _save_data_placeholder(self):
        """Acknowledge data saving, but can't implement true file I/O reliably
           under strict 'no terminal/installations' without explicit user interaction."""
        messagebox.showinfo(
            "Save Feature (Conceptual)",
            "In a real application, data would be saved to a file (e.g., JSON, CSV).\n"
            "Due to current constraints (no terminal/direct file system access in IDLE), "
            "this version operates in-memory only. "
            "Restarting the application will reset the data (except for sample data)."
        )
        # Example of how you *would* save data if file I/O were freely available:
        # import json
        # with open("contacts.json", "w") as f:
        #     json.dump([c.to_dict() for c in self.contacts], f, indent=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerGUI(root)
    root.mainloop()
