#include <iostream>
#include <string>

// Function to add two numbers
int addNumbers(int a, int b) {
    return a + b;
}

int main() {
    // Variables
    int number1, number2;
    std::string name;

    // Input and Output
    std::cout << "Enter your name: ";
    std::cin >> name;
    std::cout << "Hello, " << name << "!" << std::endl;

    std::cout << "Enter two numbers to add:" << std::endl;
    std::cout << "Number 1: ";
    std::cin >> number1;
    std::cout << "Number 2: ";
    std::cin >> number2;

    // Function call
    int sum = addNumbers(number1, number2);

    // Conditional statement
    if (sum > 10) {
        std::cout << "The sum is greater than 10!" << std::endl;
    } else {
        std::cout << "The sum is 10 or less." << std::endl;
    }

    // Loop
    std::cout << "Counting from 1 to 5:" << std::endl;
    for (int i = 1; i <= 5; i++) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    return 0;
}