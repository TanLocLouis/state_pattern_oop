import tkinter as tk
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk

# ------------------------ CONTEXT: VENDING MACHINE ----------------------------
class VendingMachine:
    def __init__(self, ui):
        self.money = 0
        self.stock = 4  # Default 4 products
        self.ui = ui
        self.set_state(NoCoinState())

    def set_state(self, state):
        self.state = state
        self.ui.update_status(f"{state.__class__.__name__}")
        self.ui.update_stock(self.stock)
        self.ui.update_money(self.money)

    def insert_coin(self, amount):
        self.state.insert_coin(self, amount)

    def select_product(self, product):
        self.state.select_product(self, product)

    def dispense(self):
        self.state.dispense(self)

    def add_money(self, amount):
        self.money += amount
        self.ui.update_money(self.money)

    def return_change(self):
        if self.money > 0:
            self.ui.log_message(f"Returning change: {self.money} VND")
            self.money = 0
            self.ui.update_money(self.money)

    def decrease_stock(self):
        if self.stock > 0:
            self.stock -= 1
            self.ui.update_stock(self.stock)

# ------------------------ STATES ----------------------------
class State:
    def insert_coin(self, machine, amount): pass
    def select_product(self, machine, product): pass
    def dispense(self, machine): pass

class NoCoinState(State):
    def insert_coin(self, machine, amount):
        machine.ui.log_message(f"Received {amount} VND.")
        machine.add_money(amount)
        machine.set_state(HasCoinState())

    def select_product(self, machine, product):
        machine.ui.log_message("Please insert coin first.")

    def dispense(self, machine):
        machine.ui.log_message("No coin inserted.")

class HasCoinState(State):
    def insert_coin(self, machine, amount):
        machine.ui.log_message(f"Added {amount} VND more.")
        machine.add_money(amount)

    def select_product(self, machine, product):
        price = 10000
        machine.ui.log_message(f"Selected product: {product}")
        if machine.money >= price:
            change = machine.money - price
            if change > 0:
                machine.ui.log_message(f"Dispensing product and returning {change} VND change.")
            else:
                machine.ui.log_message("Dispensing product...")
            machine.add_money(-price)
            machine.return_change()
            machine.set_state(DispensingState())
            machine.dispense()
        else:
            machine.ui.log_message("Not enough money. Please add more.")

    def dispense(self, machine):
        machine.ui.log_message("Please select a product first.")

class DispensingState(State):
    def insert_coin(self, machine, amount):
        machine.ui.log_message("Currently dispensing. Please wait.")

    def select_product(self, machine, product):
        machine.ui.log_message("Currently dispensing. Please wait.")

    def dispense(self, machine):
        machine.decrease_stock()
        machine.ui.log_message("Product dispensed. Thank you!")
        if machine.stock == 0:
            machine.set_state(SoldOutState())
        else:
            machine.set_state(NoCoinState())

class SoldOutState(State):
    def insert_coin(self, machine, amount):
        machine.ui.log_message("Sold out. Cannot accept money.")

    def select_product(self, machine, product):
        machine.ui.log_message("Sold out. No product available.")

    def dispense(self, machine):
        machine.ui.log_message("Sold out.")

# ------------------------ UI ----------------------------
class VendingMachineUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")
        self.root.geometry("700x500")  # Fixed window size
        self.root.resizable(False, False)

        # Status label
        self.status_label = tk.Label(root, text="Status: ", font=("Arial", 12))
        self.status_label.pack()

        self.stock_label = tk.Label(root, text="Stock: ", font=("Arial", 12))
        self.stock_label.pack()

        # Coin frame with icon and money label
        self.coin_frame = tk.Frame(root)
        self.coin_frame.pack(pady=5)

        self.coin_image = None
        self.coin_img_label = tk.Label(self.coin_frame)
        self.coin_img_label.pack(side=tk.LEFT)

        self.money_label = tk.Label(self.coin_frame, text="Money: 0 VND", font=("Arial", 12))
        self.money_label.pack(side=tk.LEFT, padx=5)

        # Buttons
        tk.Button(root, text="Insert 5000 VND", command=lambda: self.machine.insert_coin(5000)).pack(pady=2)
        tk.Button(root, text="Insert 10000 VND", command=lambda: self.machine.insert_coin(10000)).pack(pady=2)
        tk.Button(root, text="Select Product (Pepsi) - 10000 VND", command=lambda: self.machine.select_product("Pepsi")).pack(pady=5)

        # Pepsi image display
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(pady=5)

        # Log area
        self.log_text = tk.Text(root, height=10, width=70)
        self.log_text.pack(pady=5)

        # Load images
        self.pepsi_image = None
        self.load_images()

        # Init machine
        self.machine = VendingMachine(self)

    def load_images(self):
        if os.path.exists("pepsi.png"):
            img = Image.open("pepsi.png")
            img = img.resize((60, 90))  # Resize product image
            self.pepsi_image = ImageTk.PhotoImage(img)
        else:
            self.log_message("Missing pepsi.png")

        if os.path.exists("coin.png"):
            img = Image.open("coin.png")
            img = img.resize((30, 30))  # Resize coin image
            self.coin_image = ImageTk.PhotoImage(img)
            self.coin_img_label.config(image=self.coin_image)
        else:
            self.log_message("Missing coin.png")

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def update_money(self, money):
        self.money_label.config(text=f"Money: {money} VND")

    def update_stock(self, stock):
        self.stock_label.config(text=f"Stock: {stock}")
        self.display_pepsi_stock(stock)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def display_pepsi_stock(self, count):
        # Clear old images
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        if self.pepsi_image:
            for i in range(count):
                label = tk.Label(self.image_frame, image=self.pepsi_image)
                label.pack(side=tk.LEFT, padx=2)
        else:
            self.log_message("Cannot display Pepsi images (image not loaded)")

# ------------------------ MAIN ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineUI(root)
    root.mainloop()
