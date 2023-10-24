import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import json

"""
Create a json file named "kbl_stocks.json" with below
[
    {
        "White Cap Can 500ml Local": "672419"
    },
    {
        "Senator Dark 50L": "688295"
    }
]
"""
# Define the base URL of your Flask API
API_BASE_URL = 'http://localhost:5001/api_tutorial/kbl_stocks'  # uses flask api tutorial app, it must be running


def load_kbl_stocks():
    try:
        with open('kbl_stocks.json', 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []


def add_stock():
    material_description = material_description_entry.get()
    material_code = material_code_entry.get()

    if not material_description or not material_code:
        messagebox.showerror("Error", "Both Material Description and Material Code are required.")
        return

    params = {
        'material_description': material_description,
        'material_code': material_code
    }

    response = requests.get(f'{API_BASE_URL}/add_stock', params=params)

    if response.status_code == 201:
        messagebox.showinfo("Success", "Stock added successfully.")
    else:
        messagebox.showerror("Error", f"Failed to add stock: {response.json()['error']}")

    material_description_entry.delete(0, tk.END)
    material_code_entry.delete(0, tk.END)


def delete_stock():
    material_code = delete_material_code_entry.get()

    if not material_code:
        messagebox.showerror("Error", "Material Code is required.")
        return

    data = {
        'material_code': material_code
    }

    response = requests.post(f'{API_BASE_URL}/delete_stock', data=data)

    if response.status_code == 200:
        messagebox.showinfo("Success", "Stock deleted successfully.")
    else:
        messagebox.showerror("Error", f"Failed to delete stock: {response.json()['error']}")

    delete_material_code_entry.delete(0, tk.END)


def show_all_stocks():
    stocks = load_kbl_stocks()

    if stocks:
        stocks_text.config(state=tk.NORMAL)
        stocks_text.delete(1.0, tk.END)
        stocks_text.insert(tk.END, json.dumps(stocks, indent=4))
        stocks_text.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("Info", "No stocks available.")


# Create the main application window
app = tk.Tk()
app.title("AGL-NCD BEER STOCK MANAGEMENT")

# Create and configure GUI widgets
material_description_label = tk.Label(app, text="Material Description:")
material_description_entry = tk.Entry(app)

material_code_label = tk.Label(app, text="Material Code:")
material_code_entry = tk.Entry(app)

add_stock_button = tk.Button(app, text="Add Stock", command=add_stock, background="green", fg="white")

delete_material_code_label = tk.Label(app, text="Material Code:")
delete_material_code_entry = tk.Entry(app)

delete_stock_button = tk.Button(app, text="Delete Stock", command=delete_stock, background="red", fg="white")
space_in_between = tk.Label(app)
show_all_stocks_button = tk.Button(app, text="Show All Stocks", command=show_all_stocks, background="yellow", fg="black")

stocks_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=10, background="grey", fg="yellow")
stocks_text.config(state=tk.DISABLED)

# Place widgets on the grid
material_description_label.grid(row=0, column=0)
material_description_entry.grid(row=0, column=1)
material_code_label.grid(row=1, column=0)
material_code_entry.grid(row=1, column=1)
add_stock_button.grid(row=2, column=0, columnspan=2)

delete_material_code_label.grid(row=3, column=0)
delete_material_code_entry.grid(row=3, column=1)
delete_stock_button.grid(row=4, column=0, columnspan=2)
space_in_between.grid(row=5, column=0, columnspan=2)
show_all_stocks_button.grid(row=7, column=0, columnspan=2)

stocks_text.grid(row=8, column=0, columnspan=2)

# Start the Tkinter main loop
app.mainloop()