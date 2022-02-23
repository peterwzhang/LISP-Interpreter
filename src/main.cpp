#include <iostream>
#include <string>

#include "../include/fmt/format.h"
#include "../include/parser.h"

int main() {
    fmt::print(">>> ");
    std::string input;
    std::cin >> input;
    Scanner scanner(input);
    return 0;
}