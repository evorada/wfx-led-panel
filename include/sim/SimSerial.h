#pragma once

#include <string>

class SimSerialClass {
public:
    bool begin(unsigned long) { return true; }
    int available();
    int read();
    size_t write(uint8_t b);
    size_t write(const char* message, uint8_t msgLen);
    size_t readBytes(uint8_t* buffer, uint8_t len);
    void flush();
    void println(const char* s);
    void print(const char* s);
    void closeSlave();

    std::string init();
private:
    int master_fd = -1;
    int slave_fd = -1;
    char peek_buffer[256]; // Buffer for peeked bytes
    int peek_count = 0;    // Number of bytes in peek buffer
};
extern SimSerialClass Serial;
