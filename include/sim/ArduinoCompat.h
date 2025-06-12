#pragma once

#include <string>
#include <cstdint>
#include <cstring>

// Forward declarations
class Print;
class String;
class __FlashStringHelper;

// Arduino String class
class String {
public:
    String() {}
    String(const char* str) : str_(str) {}
    String(const std::string& str) : str_(str) {}
    const char* c_str() const { return str_.c_str(); }
    operator const char*() const { return c_str(); }
    String& operator+=(const String& rhs) {
        str_ += rhs.str_;
        return *this;
    }
    String& operator+=(const char* rhs) {
        str_ += rhs;
        return *this;
    }
private:
    std::string str_;
};

// Arduino Print class
class Print {
public:
    virtual size_t write(uint8_t) = 0;
    virtual size_t write(const uint8_t* buffer, size_t size) {
        size_t n = 0;
        while (size--) {
            if (write(*buffer++)) n++;
            else break;
        }
        return n;
    }
    virtual size_t print(const char* str) {
        return write((const uint8_t*)str, strlen(str));
    }
    virtual size_t print(const String& str) {
        return print(str.c_str());
    }
    virtual size_t println(const char* str) {
        size_t n = print(str);
        n += print("\r\n");
        return n;
    }
    virtual size_t println(const String& str) {
        return println(str.c_str());
    }
    virtual ~Print() {}
};

// Arduino FlashStringHelper type
class __FlashStringHelper {
public:
    __FlashStringHelper(const char* str) : str_(str) {}
    operator const char*() const { return str_; }
private:
    const char* str_;
};

// Arduino F() macro
#define F(x) __FlashStringHelper(x)

// Arduino types
typedef uint8_t boolean;
typedef uint16_t word; 