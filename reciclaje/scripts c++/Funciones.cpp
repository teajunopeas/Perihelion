#include <iostream>
#include <string>

// Function to add two numbers
int addNumbers(int a, int b) {
    return a + b;
}

// Function to multiply two numbers
int multiplyNumbers(int a, int b) {
    return a * b;
}

// Function to greet the user
void greetUser(const std::string& name) {
    std::cout << "Welcome, " << name << "!" << std::endl;
}

int main() {
    int number1, number2;
    std::string name;

    // Input and Output
    std::cout << "Enter your name: ";
    std::cin >> name;
    greetUser(name); // Call greetUser function

    std::cout << "Enter two numbers to multiply:" << std::endl;
    std::cout << "Number 1: ";
    std::cin >> number1;
    std::cout << "Number 2: ";
    std::cin >> number2;

    // Call multiplyNumbers function
    int product = multiplyNumbers(number1, number2);
    std::cout << "The product of the numbers is: " << product << std::endl;

    return 0;
}