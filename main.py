import tkinter as tk
from abc import ABC, abstractmethod

# Forward declaration
class VendingMachine:
    pass

# Abstract State class
class State(ABC):
    @abstractmethod
    def insert_coin(self, machine):
        pass

    @abstractmethod
    def press_button(self, machine):
        pass

    @abstractmethod
    def dispense(self, machine):
        pass

# Concrete States
class NoCoinState(State):
    def insert_coin(self, machine):
        machine.set_state(machine.has_coin_state)
        machine.set_output("Coin inserted.")

    def press_button(self, machine):
        machine.set_output("Please insert coin first.")

    def dispense(self, machine):
        machine.set_output("Cannot dispense without coin.")

class HasCoinState(State):
    def insert_coin(self, machine):
        machine.set_output("Coin already inserted.")

    def press_button(self, machine):
        machine.set_state(machine.sold_state)
        machine.set_output("Button pressed. Preparing to dispense item...")

    def dispense(self, machine):
        machine.set_output("Press button to dispense.")

class SoldState(State):
    def insert_coin(self, machine):
        machine.set_output("Please wait, dispensing in progress...")

    def press_button(self, machine):
        machine.set_output("Already dispensing...")

    def dispense(self, machine):
        machine.set_state(machine.no_coin_state)
        machine.set_output("Item dispensed.")

# VendingMachine (Context)
class VendingMachine:
    def __init__(self, output_callback):
        self.no_coin_state = NoCoinState()
        self.has_coin_state = HasCoinState()
        self.sold_state = SoldState()

        self.state = self.no_coin_state
        self.output_callback = output_callback

    def set_state(self, new_state):
        self.state = new_state

    def insert_coin(self):
        self.state.insert_coin(self)

    def press_button(self):
        self.state.press_button(self)

    def dispense(self):
        self.state.dispense(self)

    def set_output(self, message):
        self.output_callback(message)

# GUI
class VendingMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")

        self.output_label = tk.Label(root, text="Welcome to Vending Machine!", font=("Arial", 14), wraplength=300)
        self.output_label.pack(pady=20)

        self.machine = VendingMachine(self.update_output)

        tk.Button(root, text="Insert Coin", command=self.machine.insert_coin, width=20).pack(pady=5)
        tk.Button(root, text="Press Button", command=self.machine.press_button, width=20).pack(pady=5)
        tk.Button(root, text="Dispense", command=self.machine.dispense, width=20).pack(pady=5)

    def update_output(self, message):
        self.output_label.config(text=message)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineApp(root)
    root.mainloop()
