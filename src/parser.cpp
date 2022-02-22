#include <iostream>
#include <list>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

// clang-format off
#include "../include/fmt/format.h"
#include "../include/parser.h"
// clang-format on

std::string getType(TokenType tt) {
    switch (tt) {
        case TokenType::LEFT_PAREN:
            return "LEFT_PAREN";
        case TokenType::RIGHT_PAREN:
            return "RIGHT_PAREN";
        case TokenType::LEFT_BRACE:
            return "LEFT_BRACE";
        case TokenType::RIGHT_BRACE:
            return "RIGHT_BRACE";
        case TokenType::COMMA:
            return "COMMA";
        case TokenType::DOT:
            return "DOT";
        case TokenType::MINUS:
            return "MINUS";
        case TokenType::PLUS:
            return "PLUS";
        case TokenType::SEMICOLON:
            return "SEMICOLON";
        case TokenType::SLASH:
            return "SLASH";
        case TokenType::STAR:
            return "STAR";
        case TokenType::BANG:
            return "BANG";
        case TokenType::BANG_EQUAL:
            return "BANG_EQUAL";
        case TokenType::EQUAL:
            return "EQUAL";
        case TokenType::EQUAL_EQUAL:
            return "EQUAL_EQUAL";
        case TokenType::GREATER:
            return "GREATER";
        case TokenType::GREATER_EQUAL:
            return "GREATER_EQUAL";
        case TokenType::LESS:
            return "LESS";
        case TokenType::LESS_EQUAL:
            return "LESS_EQUAL";
        case TokenType::IDENTIFIER:
            return "IDENTIFIER";
        case TokenType::STRING:
            return "STRING";
        case TokenType::NUMLIT:
            return "NUMLIT";
        case TokenType::IF:
            return "IF";
        case TokenType::WHILE:
            return "WHILE";
        case TokenType::SET:
            return "SET";
        case TokenType::BEGIN:
            return "BEGIN";
        case TokenType::CONS:
            return "CONS";
        case TokenType::CAR:
            return "CAR";
        case TokenType::CDR:
            return "CDR";
        case TokenType::NUMBER:
            return "NUMBER";
        case TokenType::SYSMBOL:
            return "SYSMBOL";
        case TokenType::LIST:
            return "LIST";
        case TokenType::NIL:
            return "NIL";
        case TokenType::PRINT:
            return "PRINT";
        case TokenType::T:
            return "T";
        case TokenType::END_OF_FILE:
            return "END_OF_FILE";

        default:
            return "UNKNOWN";
    }
}

Token::Token(TokenType t, std::string l, int nl) {
    type = t;
    lexeme = l;
    numlit = nl;
    isNum = true;
}
Token::Token(TokenType t, std::string l, std::string sl) {
    type = t;
    lexeme = l;
    stringlit = sl;
    isNum = false;
}

void Token::print() {
    if (isNum)
        fmt::print("{} {} {}\n", getType(type), lexeme, numlit);
    else
        fmt::print("{} {} {}\n", getType(type), lexeme, stringlit);
}

bool Scanner::isAtEnd() { return current >= source.length(); }
char Scanner::advance() { return source.at(current++); }
void Scanner::scanToken() {
    char c = advance();
    switch (c) {
        // case '(':
        //   addToken(TokenType::LEFT_PAREN);
        //   break;
        // case ')':
        //   addToken(TokenType::RIGHT_PAREN);
        //   break;
        // case '{':
        //   addToken(TokenType::LEFT_BRACE);
        //   break;
        // case '}':
        //   addToken(RIGHT_BRACE);
        //   break;
        // case ',':
        //   addToken(COMMA);
        //   break;
        // case '.':
        //   addToken(DOT);
        //   break;
        // case '-':
        //   addToken(MINUS);
        //   break;
        // case '+':
        //   addToken(PLUS);
        //   break;
        // case ';':
        //   addToken(SEMICOLON);
        //   break;
        // case '*':
        //   addToken(STAR);
        //   break; // [slash]
        //          //> two-char-tokens
        // case '!':
        //   addToken(match('=') ? BANG_EQUAL : BANG);
        //   break;
        // case '=':
        //   addToken(match('=') ? EQUAL_EQUAL : EQUAL);
        //   break;
        // case '<':
        //   addToken(match('=') ? LESS_EQUAL : LESS);
        //   break;
        // case '>':
        //   addToken(match('=') ? GREATER_EQUAL : GREATER);
        //   break;
        //   //< two-char-tokens
        //   //> slash
        // case '/':
        //   if (match('/')) {
        //     // A comment goes until the end of the line.
        //     while (peek() != '\n' && !isAtEnd())
        //       advance();
        //   } else {
        //     addToken(SLASH);
        //   }
        //   break;
        //   //< slash
        //   //> whitespace

        // case ' ':
        // case '\r':
        // case '\t':
        //   // Ignore whitespace.
        //   break;

        // case '\n':
        //   line++;
        //   break;
        //   //< whitespace
        //   //> string-start

        // case '"':
        //   string();
        //   break;
        //   //< string-start
        //   //> char-error

        // default:
        //   /* Scanning char-error < Scanning digit-start
        //           Lox.error(line, "Unexpected character.");
        //   */
        //   //> digit-start
        //   if (isDigit(c)) {
        //     number();
        //     //> identifier-start
        //   } else if (isAlpha(c)) {
        //     identifier();
        //     //< identifier-start
        //   } else {
        //     Lox.error(line, "Unexpected character.");
        //   }
        //   //< digit-start
        //   break;
        //   //< char-error
    }
}

Scanner::Scanner(std::string src) { source = src; }
std::list<Token> Scanner::scanTokens() {
    while (!isAtEnd()) {
        start = current;
        // scanToken();
    }
}

void run(std::string src) {}
