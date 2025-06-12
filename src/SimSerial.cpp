#ifdef SIMULATOR
#include "SimSerial.h"
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <util.h>
#include <stdio.h>
#include <sys/ioctl.h>

SimSerialClass Serial;

std::string SimSerialClass::init() {
    int slave_fd;
    char slave_name[128];

    if (openpty(&master_fd, &slave_fd, slave_name, NULL, NULL) == -1) {
        perror("openpty failed");
        exit(1);
    }

    printf("Fake serial port created: %s\n", slave_name);
    close(slave_fd);
    return std::string(slave_name);
}

int SimSerialClass::available() {
    int bytes;
    ioctl(master_fd, FIONREAD, &bytes);
    return bytes;
}

int SimSerialClass::read() {
    char c;
    int n = ::read(master_fd, &c, 1);
    if (n <= 0) return -1;
    return static_cast<uint8_t>(c);
}

size_t SimSerialClass::write(uint8_t b) {
    return ::write(master_fd, &b, 1);
}

void SimSerialClass::print(const char* s) {
    ::write(master_fd, s, strlen(s));
}

void SimSerialClass::println(const char* s) {
    ::write(master_fd, s, strlen(s));
    ::write(master_fd, "\r\n", 2);
}
#endif