#include <iostream>
#include <list>
#include <memory>
#include <unordered_map>
#include <string>
#include <vector>
#include "../include/fmt/format.h"

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
  IF, WHILE, SET, BEGIN, CONS, CAR, CDR, NUMBER, SYSMBOL, LIST, NIL, PRINT, T,

  END_OF_FILE
};

std::string getType(TokenType tt){
    switch (tt){
        case TokenType::LEFT_PAREN:
        return "LEFT_PAREN";
        default:
        return "SOMETHING";
    }
}

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
        //int line;

        Token(TokenType t, std::string l, int nl){
            type = t;
            lexeme = l;
            numlit = nl;
            isNum = true;
        }
        Token(TokenType t, std::string l, std::string sl){
            type = t;
            lexeme = l;
            stringlit = sl;
            isNum = false;
        }

        void print(){
            if (isNum)
                fmt::print("{} {} {}\n", getType(type), lexeme, numlit);
            else
                fmt::print("{} {} {}\n", getType(type), lexeme, stringlit);
        }
};

class Scanner{
    std::string source;
    std::list<TokenType> tokens;
    int start = 0;
    int current = 0;
    //int line = 1;
    bool isAtEnd(){
        return current >= source.length();
    }
    public:
        Scanner(std::string src){
            source = src;
        }
        std::list<Token> scanTokens(){
            while (!isAtEnd()){
                start = current;
                // scanToken();
            }
        }
};

void run(std::string src){

}


int main(){
    using namespace std;
    string line;
    while (getline(cin, line)){
        fmt::print("input: {}\n", line);

    }
}