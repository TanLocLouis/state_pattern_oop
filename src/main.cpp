#include <iostream>
#include <string>

class VendingMachine;

class State {
public:
    virtual void insertCoin(VendingMachine* machine, int amount) = 0;
    virtual void selectProduct(VendingMachine* machine, const std::string& product) = 0;
    virtual void dispense(VendingMachine* machine) = 0;
    virtual ~State() = default;
};

class VendingMachine {
    State* currentState;
    int money = 0;
    int productStock = 1;

public:
    static State* noCoinState;
    static State* hasCoinState;
    static State* soldOutState;
    static State* dispensingState;

    VendingMachine();

    void setState(State* state) { currentState = state; }
    void insertCoin(int amount) { currentState->insertCoin(this, amount); }
    void selectProduct(const std::string& product) { currentState->selectProduct(this, product); }
    void dispense() { currentState->dispense(this); }

    int getMoney() const { return money; }
    void addMoney(int amount) { money += amount; }
    void returnChange() {
        if (money > 0) {
            std::cout << "Returning change: " << money << " VND\n";
            money = 0;
        }
    }

    int getStock() const { return productStock; }
    void decreaseStock() { if (productStock > 0) productStock--; }
};

class NoCoinState : public State {
public:
    void insertCoin(VendingMachine* machine, int amount) override {
        std::cout << "Received " << amount << " VND.\n";
        machine->addMoney(amount);
        machine->setState(VendingMachine::hasCoinState);
    }

    void selectProduct(VendingMachine* machine, const std::string& product) override {
        std::cout << "Please insert coin first.\n";
    }

    void dispense(VendingMachine* machine) override {
        std::cout << "No coin inserted.\n";
    }
};

class HasCoinState : public State {
public:
    void insertCoin(VendingMachine* machine, int amount) override {
        std::cout << "Added " << amount << " VND more.\n";
        machine->addMoney(amount);
    }

    void selectProduct(VendingMachine* machine, const std::string& product) override {
        const int price = 10000;
        std::cout << "Selected product: " << product << "\n";

        if (machine->getMoney() >= price) {
            int change = machine->getMoney() - price;

            if (change > 0)
                std::cout << "Dispensing product and returning " << change << " VND change.\n";
            else
                std::cout << "Dispensing product...\n";

            machine->addMoney(-price);
            machine->returnChange();
            machine->setState(VendingMachine::dispensingState);
            machine->dispense();
        }
        else {
            std::cout << "Not enough money. Please add more.\n";
        }
    }

    void dispense(VendingMachine* machine) override {
        std::cout << "Please select a product first.\n";
    }
};

class DispensingState : public State {
public:
    void insertCoin(VendingMachine* machine, int amount) override {
        std::cout << "Currently dispensing. Please wait.\n";
    }

    void selectProduct(VendingMachine* machine, const std::string& product) override {
        std::cout << "Currently dispensing. Please wait.\n";
    }

    void dispense(VendingMachine* machine) override {
        machine->decreaseStock();
        std::cout << "Product dispensed. Thank you!\n";

        if (machine->getStock() == 0) {
            machine->setState(VendingMachine::soldOutState);
        }
        else {
            machine->setState(VendingMachine::noCoinState);
        }
    }
};

class SoldOutState : public State {
public:
    void insertCoin(VendingMachine* machine, int amount) override {
        std::cout << "Sold out. Cannot accept money.\n";
    }

    void selectProduct(VendingMachine* machine, const std::string& product) override {
        std::cout << "Sold out. No product available.\n";
    }

    void dispense(VendingMachine* machine) override {
        std::cout << "Sold out.\n";
    }
};

// Initialize static members
State* VendingMachine::noCoinState = new NoCoinState();
State* VendingMachine::hasCoinState = new HasCoinState();
State* VendingMachine::soldOutState = new SoldOutState();
State* VendingMachine::dispensingState = new DispensingState();

VendingMachine::VendingMachine() {
    currentState = productStock > 0 ? noCoinState : soldOutState;
}

// -------------------------- MAIN -----------------------------

int main() {
    VendingMachine vm;

    std::cout << "\n---> [1] Test NoCoinState (Chưa nhận tiền):\n";
    vm.selectProduct("Pepsi"); // Không được phép chọn món
    vm.dispense();             // Không có tác dụng

    std::cout << "\n---> [2] Test HasCoinState (Đã nhận tiền):\n";
    vm.insertCoin(7000);       // Chưa đủ tiền
    vm.selectProduct("Pepsi"); // Không đủ tiền

    vm.insertCoin(5000);       // Tổng đủ tiền
    vm.selectProduct("Pepsi"); // Sẽ phân phối sản phẩm

    std::cout << "\n---> [3] Test DispensingState (Đang phân phối):\n";
    vm.insertCoin(5000);       // Bị từ chối vì đang giao hàng
    vm.selectProduct("Pepsi"); // Bị từ chối
    // Tự động chuyển về NoCoin hoặc SoldOut sau dispense

    std::cout << "\n---> [4] Test HasCoinState tiếp tục mua hàng:\n";
    vm.insertCoin(10000);      // Trạng thái HasCoin
    vm.selectProduct("Pepsi"); // Mua lần thứ 2

    std::cout << "\n---> [5] Test SoldOutState (Hết hàng):\n";
    vm.insertCoin(5000);       // Không nhận
    vm.selectProduct("Pepsi"); // Không xử lý

    std::cout << "\n---> [6] Test sau khi hết hàng:\n";
    vm.insertCoin(10000);      // Không nhận
    vm.selectProduct("Pepsi"); // Không xử lý

    return 0;
}

