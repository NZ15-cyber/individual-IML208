import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from datetime import datetime

# Lab Booking System
class LabBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Booking System")
        self.root.geometry("900x600")
        self.root.config(bg="#f4f4f9")

        self.bookings = []

        # Title Section
        title_frame = tk.Frame(root, bg="#5e6a73")
        title_frame.pack(fill="x", pady=10)

        title_label = tk.Label(title_frame, text="Lab Booking System", font=("Helvetica", 24, "bold"), bg="#5e6a73", fg="white")
        title_label.pack(pady=10)

        # Input Section
        input_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="sunken")
        input_frame.pack(padx=20, pady=10, fill="x")

        self.name_label = tk.Label(input_frame, text="Name:", font=("Arial", 12))
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(input_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.date_label = tk.Label(input_frame, text="Date (YYYY-MM-DD):", font=("Arial", 12))
        self.date_label.grid(row=1, column=0, padx=10, pady=10)
        self.date_entry = tk.Entry(input_frame, width=40)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)

        self.time_label = tk.Label(input_frame, text="Time (HH:MM):", font=("Arial", 12))
        self.time_label.grid(row=2, column=0, padx=10, pady=10)
        self.time_entry = tk.Entry(input_frame, width=40)
        self.time_entry.grid(row=2, column=1, padx=10, pady=10)

        self.duration_label = tk.Label(input_frame, text="Duration (Hours):", font=("Arial", 12))
        self.duration_label.grid(row=3, column=0, padx=10, pady=10)
        self.duration_entry = tk.Entry(input_frame, width=40)
        self.duration_entry.grid(row=3, column=1, padx=10, pady=10)

        self.equipment_label = tk.Label(input_frame, text="Lab Equipment:", font=("Arial", 12))
        self.equipment_label.grid(row=4, column=0, padx=10, pady=10)
        self.equipment_combobox = ttk.Combobox(input_frame, values=["Projector", "Microphone", "Laptop", "Whiteboard", "Camera"], width=37)
        self.equipment_combobox.grid(row=4, column=1, padx=10, pady=10)

        # Button Section
        button_frame = tk.Frame(root, bg="#f4f4f9")
        button_frame.pack(pady=20)

        self.create_button = tk.Button(button_frame, text="Create Data", command=self.create_data, bg="#28a745", fg="white", width=15, font=("Arial", 12))
        self.create_button.grid(row=0, column=0, padx=10)

        self.read_button = tk.Button(button_frame, text="Read Data", command=self.read_data, bg="#007bff", fg="white", width=15, font=("Arial", 12))
        self.read_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Update Data", command=self.update_data, bg="#fd7e14", fg="white", width=15, font=("Arial", 12))
        self.update_button.grid(row=1, column=0, padx=10)

        self.delete_button = tk.Button(button_frame, text="Delete Data", command=self.delete_data, bg="#dc3545", fg="white", width=15, font=("Arial", 12))
        self.delete_button.grid(row=1, column=1, padx=10)

        # Data Display Table
        self.treeview = ttk.Treeview(root, columns=("Name", "Date", "Time", "Duration", "Equipment"), show="headings", height=10)
        self.treeview.pack(pady=10, fill="x")

        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col, anchor="center")
            self.treeview.column(col, anchor="center", width=150)

    def create_data(self):
        name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        duration = self.duration_entry.get()
        equipment = self.equipment_combobox.get()

        if not name or not date or not time or not duration or not equipment:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
            int(duration)
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time/duration format!")
            return

        booking = (name, date, time, duration, equipment)
        self.bookings.append(booking)

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.equipment_combobox.set('')

        messagebox.showinfo("Success", "Booking Created Successfully!")
        self.update_treeview()

    def read_data(self):
        if not self.bookings:
            messagebox.showinfo("No Data", "No bookings available.")
        else:
            for booking in self.bookings:
                print(booking)

    def update_data(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to update.")
            return

        # Get updated data
        updated_name = askstring("Update", "Enter updated Name:")
        updated_date = askstring("Update", "Enter updated Date (YYYY-MM-DD):")
        updated_time = askstring("Update", "Enter updated Time (HH:MM):")
        updated_duration = askstring("Update", "Enter updated Duration (Hours):")
        updated_equipment = askstring("Update", "Enter updated Lab Equipment:")

        for item in selected_item:
            idx = self.treeview.index(item)
            self.bookings[idx] = (updated_name, updated_date, updated_time, updated_duration, updated_equipment)

        messagebox.showinfo("Success", "Booking Updated Successfully!")
        self.update_treeview()

    def delete_data(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to delete.")
            return

        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this booking?")
        if response == "yes":
            for item in selected_item:
                idx = self.treeview.index(item)
                del self.bookings[idx]
            messagebox.showinfo("Success", "Booking Deleted Successfully!")
            self.update_treeview()

    def update_treeview(self):
        # Clear existing data in the Treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Insert new data into Treeview
        for booking in self.bookings:
            self.treeview.insert("", "end", values=booking)


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = LabBookingSystem(root)
    root.mainloop()
