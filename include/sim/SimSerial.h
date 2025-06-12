#pragma once

#include <string>

class SimSerialClass {
public:
    bool begin(unsigned long) { return true; }
    int available();
    int read();
    size_t write(uint8_t b);
    void flush() {}
    void println(const char* s);
    void print(const char* s);

    std::string init();
private:
    int master_fd = -1;
};
extern SimSerialClass Serial;
