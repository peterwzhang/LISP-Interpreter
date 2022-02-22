#ifndef PARSER_H
#define PARSER_H

#include <list>
#include <string>

enum class TokenType {
    // Single-character tokens.
    LEFT_PAREN,
    RIGHT_PAREN,
    LEFT_BRACE,
    RIGHT_BRACE,
    COMMA,
    DOT,
    MINUS,
    PLUS,
    SEMICOLON,
    SLASH,
    STAR,

    // One or two character tokens.
    BANG,
    BANG_EQUAL,
    EQUAL,
    EQUAL_EQUAL,
    GREATER,
    GREATER_EQUAL,
    LESS,
    LESS_EQUAL,

    // Literals.
    IDENTIFIER,
    STRING,
    NUMLIT,

    // Keywords.
    IF,
    WHILE,
    SET,
    BEGIN,
    CONS,
    CAR,
    CDR,
    NUMBER,
    SYSMBOL,
    LIST,
    NIL,
    PRINT,
    T,

    END_OF_FILE
};

std::string getType(TokenType tt);

union Object {
    std::string s;
    int num;
};

class Token {
   public:
    TokenType type;
    std::string lexeme;
    int numlit;
    std::string stringlit;
    bool isNum;
    // int line;

    Token(TokenType t, std::string l, int nl);
    Token(TokenType t, std::string l, std::string sl);

    void print();
};

class Scanner {
    std::string source;
    std::list<Token> tokens;
    int start = 0;
    int current = 0;
    // int line = 1;
    bool isAtEnd();
    char advance();
    void scanToken();

   public:
    Scanner(std::string src);
    std::list<Token> scanTokens();
};

void run(std::string src);

#endif