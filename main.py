# thinter is a GUI python lib
import tkinter as tk

# ------------------------ (Context) VENDING MACHINE ----------------------------
class VendingMachine:
    def __init__(self, ui):
        self.money = 0
        self.stock = 3 #[DEMO] Default 0 products for demo
        self.ui = ui
        self.set_state(NoCoinState()) #[DEMO] Default no coins

    def set_state(self, state):
        self.state = state

        # Update in UI
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

    # def add_stock_item(self):
    #     self.stock += 1

    #     # Update in UI
    #     self.ui.update_stock(self.stock)

    def return_change(self):
        if self.money > 0:
            self.money = 0

            # Update in UI
            self.ui.log_message(f"Returning change: {self.money} VND")
            self.ui.update_money(self.money)

    def decrease_stock(self):
        if self.stock > 0:
            self.stock -= 1

            # Update in UI
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

        # Giao diện hiển thị trạng thái, tiền và hàng
        self.status_label = tk.Label(root, text="Status: ", font=("Arial", 12))
        self.status_label.pack()

        self.stock_label = tk.Label(root, text="Stock: ", font=("Arial", 12))
        self.stock_label.pack()

        self.money_label = tk.Label(root, text="Money: 0 VND", font=("Arial", 12))
        self.money_label.pack()

        # Nút thao tác
        # tk.Button(root, text="Add stock item", command=lambda: self.machine.add_stock_item()).pack(pady=2)
        tk.Button(root, text="Insert 5000 VND", command=lambda: self.machine.insert_coin(5000)).pack(pady=2)
        tk.Button(root, text="Insert 10000 VND", command=lambda: self.machine.insert_coin(10000)).pack(pady=2)
        tk.Button(root, text="Select Product (Pepsi) cost 10000 VND", command=lambda: self.machine.select_product("Pepsi")).pack(pady=5)

        # Ô log để hiển thị thông báo
        self.log_text = tk.Text(root, height=10, width=50)
        self.log_text.pack(pady=5)

        # Khởi tạo máy sau khi giao diện đã sẵn sàng
        self.machine = VendingMachine(self)

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def update_money(self, money):
        self.money_label.config(text=f"Money: {money} VND")

    def update_stock(self, stock):
        self.stock_label.config(text=f"Stock: {stock}")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)


# ------------------------ MAIN ----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineUI(root)
    root.mainloop()
