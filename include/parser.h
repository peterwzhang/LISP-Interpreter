#ifndef PARSER_H
#define PARSER_H

#include <list>
#include <map>
#include <string>

enum class TokenType {
    // Single-character tokens.
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE,
    COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR,

    // One or two character tokens.
    BANG, BANG_EQUAL,
    EQUAL, EQUAL_EQUAL,
    GREATER, GREATER_EQUAL,
    LESS, LESS_EQUAL,

    // Literals.
    IDENTIFIER, STRING, NUMLIT,

    // Keywords.
    AND, CLASS, ELSE, FALSE, FUN, FOR, IF, NIL, OR,
    PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE, SET, 
    BEGIN, CONS, CAR, CDR, NUMBER, SYSMBOL, LIST, T,

    END_OF_FILE,
    DNE
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
    std::map<std::string, TokenType> keywords{ 
    {"and",    TokenType::AND},
    {"class",  TokenType::CLASS},
    {"else",   TokenType::ELSE},
    {"false",  TokenType::FALSE},
    {"for",    TokenType::FOR},
    {"fun",    TokenType::FUN},
    {"if",     TokenType::IF},
    {"nil",    TokenType::NIL},
    {"or",     TokenType::OR},
    {"print",  TokenType::PRINT},
    {"return", TokenType::RETURN},
    {"super",  TokenType::SUPER},
    {"this",   TokenType::THIS},
    {"true",   TokenType::TRUE},
    {"var",    TokenType::VAR},
    {"while",  TokenType::WHILE}};

    std::string source;
    std::list<Token> tokens;
    int start = 0;
    int current = 0;
    // int line = 1;
    
    void scanToken();
    void identifier();
    void number();
    void string();
    bool match(char exp);
    char peek();
    char peekNext();
    bool isAlpha(char c);
    bool isAlphaNumeric(char c);
    bool isDigit(char c);
    bool isAtEnd();
    char advance();
    void addToken(TokenType t);
    void addToken(TokenType t, std::string sl);
    void addToken(TokenType t, int nl);
    

   public:
    Scanner(std::string src);
    std::list<Token> scanTokens();
};

void run(std::string src);

#endif