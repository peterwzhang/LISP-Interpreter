#include <iostream>
#include <list>
#include <map>
#include <memory>
#include <string>
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

Scanner::Scanner(std::string src) { source = src; }

std::list<Token> Scanner::scanTokens() {
    while (!isAtEnd()) {
        start = current;
        scanToken();
    }

    tokens.push_back(Token(TokenType::END_OF_FILE, "", NULL));
    return tokens;
}

void Scanner::scanToken() {
    char c = advance();
    switch (c) {
        case '(':
            addToken(TokenType::LEFT_PAREN);
            break;
        case ')':
            addToken(TokenType::RIGHT_PAREN);
            break;
        case '{':
            addToken(TokenType::LEFT_BRACE);
            break;
        case '}':
            addToken(TokenType::RIGHT_BRACE);
            break;
        case ',':
            addToken(TokenType::COMMA);
            break;
        case '.':
            addToken(TokenType::DOT);
            break;
        case '-':
            addToken(TokenType::MINUS);
            break;
        case '+':
            addToken(TokenType::PLUS);
            break;
        case ';':
            addToken(TokenType::SEMICOLON);
            break;
        case '*':
            addToken(TokenType::STAR);
            break;  // [slash]
                    //> two-char-tokens
        case '!':
            addToken(match('=') ? TokenType::BANG_EQUAL : TokenType::BANG);
            break;
        case '=':
            addToken(match('=') ? TokenType::EQUAL_EQUAL : TokenType::EQUAL);
            break;
        case '<':
            addToken(match('=') ? TokenType::LESS_EQUAL : TokenType::LESS);
            break;
        case '>':
            addToken(match('=') ? TokenType::GREATER_EQUAL
                                : TokenType::GREATER);
            break;
            //< two-char-tokens
            //> slash
        case '/':
            if (match('/')) {
                // A comment goes until the end of the line.
                while (peek() != '\n' && !isAtEnd()) advance();
            } else {
                addToken(TokenType::SLASH);
            }
            break;
            //< slash
            //> whitespace

        case ' ':
        case '\r':
        case '\t':
            // Ignore whitespace.
            break;

        case '\n':
            // line++;
            break;
            //< whitespace
            //> string-start

        case '"':
            string();
            break;
            //< string-start
            //> char-error

        default:
            /* Scanning char-error < Scanning digit-start
                    Lox.error(line, "Unexpected character.");
            */
            //> digit-start
            if (isDigit(c)) {
                number();
                //> identifier-start
            } else if (isAlpha(c)) {
                identifier();
                //< identifier-start
            } else {
                // Lox.error(line, "Unexpected character.");
            }
            //< digit-start
            break;
            //< char-error
    }
}

void Scanner::identifier() {
    while (isAlphaNumeric(peek())) advance();
    std::string text = source.substr(start, current);
    TokenType type = keywords[text];
    if (type == TokenType::DNE)
        type = TokenType::IDENTIFIER;  //! come back later! maybe? add dne to
                                       //! map
    addToken(type);
}

void Scanner::number() {
    while (isDigit(peek())) advance();

    if (peek() == '.' && isDigit(peekNext())) {
        // Consume the '.'
        advance();

        while (isDigit(peek())) advance();
    }

    addToken(TokenType::NUMBER, std::stod(source.substr(start, current)));
}
void Scanner::string() {
    while (peek() != '"' && !isAtEnd()) {
        // if (peek() == '\n') line++;
        advance();
    }

    if (isAtEnd()) {
        // Lox.error(line, "Unterminated string.");
        return;
    }

    // The closing ".
    advance();

    // Trim the surrounding quotes.
    std::string value = source.substr(start + 1, current - 1);
    addToken(TokenType::STRING, value);
}
bool Scanner::match(char exp) {
    if (isAtEnd()) return false;
    if (source[current] != exp) return false;

    current++;
    return true;
}
char Scanner::peek() {
    if (isAtEnd()) return '\0';
    return source[current];
}
char Scanner::peekNext() {
    if (current + 1 >= source.length()) return '\0';
    return source[current + 1];
}
bool Scanner::isAlpha(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}
bool Scanner::isAlphaNumeric(char c) { return isAlpha(c) || isDigit(c); }
bool Scanner::isDigit(char c) { return c >= '0' && c <= '9'; }
bool Scanner::isAtEnd() { return current >= source.length(); }
char Scanner::advance() { return source[current++]; }
void Scanner::addToken(TokenType t) { addToken(t, NULL); }
void Scanner::addToken(TokenType t, std::string sl) {
    std::string text = source.substr(start, current);
    Token tok(t, text, sl);
    tokens.push_back(tok);
}
void Scanner::addToken(TokenType t, int nl) {
    std::string text = source.substr(start, current);
    Token tok(t, text, nl);
    tokens.push_back(tok);
}

// void run(std::string src) {}
