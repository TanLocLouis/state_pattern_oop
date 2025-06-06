#include <iostream>
#include <memory>

class VendingMachine;

// Giao dien trang thai
class State {
public:
    virtual void insertCoin(VendingMachine* machine) = 0;
    virtual void pressButton(VendingMachine* machine) = 0;
    virtual void dispense(VendingMachine* machine) = 0;
    virtual ~State() = default;
};

// Lop may ban hang (Context)
class VendingMachine {
private:
    std::shared_ptr<State> state;
public:
    VendingMachine();

    void setState(std::shared_ptr<State> newState) {
        state = newState;
    }

    void insertCoin() {
        state->insertCoin(this);
    }

    void pressButton() {
        state->pressButton(this);
    }

    void dispense() {
        state->dispense(this);
    }

    // Cac trang thai duoc dung chung
    static std::shared_ptr<State> noCoinState;
    static std::shared_ptr<State> hasCoinState;
    static std::shared_ptr<State> soldState;
};


// Dinh nghia trang thai cu the
class NoCoinState : public State {
public:
    void insertCoin(VendingMachine* machine) override {
        std::cout << "Coin inserted.\n";
        machine->setState(VendingMachine::hasCoinState);
    }
    void pressButton(VendingMachine*) override {
        std::cout << "Please insert coin first.\n";
    }
    void dispense(VendingMachine*) override {
        std::cout << "Cannot dispense without coin.\n";
    }
};

class HasCoinState : public State {
public:
    void insertCoin(VendingMachine*) override {
        std::cout << "Coin already inserted.\n";
    }
    void pressButton(VendingMachine* machine) override {
        std::cout << "Button pressed. Preparing to dispense item...\n";
        machine->setState(VendingMachine::soldState);
    }
    void dispense(VendingMachine*) override {
        std::cout << "Press button to dispense.\n";
    }
};

class SoldState : public State {
public:
    void insertCoin(VendingMachine*) override {
        std::cout << "Please wait, dispensing in progress...\n";
    }
    void pressButton(VendingMachine*) override {
        std::cout << "Already dispensing...\n";
    }
    void dispense(VendingMachine* machine) override {
        std::cout << "Item dispensed.\n";
        machine->setState(VendingMachine::noCoinState);
    }
};






// Khoi tao trang thai tĩnh
std::shared_ptr<State> VendingMachine::noCoinState = std::make_shared<NoCoinState>();
std::shared_ptr<State> VendingMachine::hasCoinState = std::make_shared<HasCoinState>();
std::shared_ptr<State> VendingMachine::soldState = std::make_shared<SoldState>();
// Constructor
VendingMachine::VendingMachine() {
    state = noCoinState;
}
int main() {
    VendingMachine machine;

    std::cout << "=== Test 1: Nhan nut khi chua dua xu ===\n";
    machine.pressButton();   // Should print: Please insert coin first

    std::cout << "\n=== Test 2: Dua xu, nhan nut, nhan hang ===\n";
    machine.insertCoin();    // Should print: Coin inserted
    machine.pressButton();   // Should print: Button pressed...
    machine.dispense();      // Should print: Item dispensed

    std::cout << "\n=== Test 3: Dua xu 2 lan lien tiep ===\n";
    machine.insertCoin();    // Should print: Coin inserted
    machine.insertCoin();    // Should print: Coin already inserted
    machine.pressButton();   // Should print: Button pressed...
    machine.dispense();      // Should print: Item dispensed

    std::cout << "\n=== Test 4: Nhan nut nhieu lan lien tiep khong dua xu ===\n";
    machine.pressButton();   // Should print: Please insert coin first
    machine.pressButton();   // Should print: Please insert coin first

    std::cout << "\n=== Test 5: Dua xu -> nhan nut -> khong goi dispense ===\n";
    machine.insertCoin();    // Should print: Coin inserted
    machine.pressButton();   // Should print: Button pressed...
    machine.insertCoin();    // Should print: Please wait, dispensing...
    machine.pressButton();   // Should print: Already dispensing...
    machine.dispense();      // Should print: Item dispensed

    return 0;
}

 