#ifdef SIMULATOR
#include "SimSerial.h"
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <util.h>
#include <cstring>
#include <errno.h>
#include <sys/time.h>

SimSerialClass Serial;

std::string SimSerialClass::init() {
    // Create a pseudo-terminal (PTY) for communication
    int master_fd, slave_fd;
    char slave_name[256];
    
    if (openpty(&master_fd, &slave_fd, slave_name, NULL, NULL) == -1) {
        perror("openpty failed");
        exit(1);
    }
    
    // Configure the slave terminal for immediate data transfer
    struct termios slave_termios;
    tcgetattr(slave_fd, &slave_termios);
    slave_termios.c_lflag &= ~(ICANON | ECHO | ECHOE | ECHOK | ECHONL | ISIG);
    slave_termios.c_iflag &= ~(IXON | IXOFF | IXANY);
    slave_termios.c_oflag &= ~OPOST;
    slave_termios.c_cc[VMIN] = 0;
    slave_termios.c_cc[VTIME] = 0;
    tcsetattr(slave_fd, TCSANOW, &slave_termios);
    
    // Configure the master terminal as well
    struct termios master_termios;
    tcgetattr(master_fd, &master_termios);
    master_termios.c_lflag &= ~(ICANON | ECHO | ECHOE | ECHOK | ECHONL | ISIG);
    master_termios.c_iflag &= ~(IXON | IXOFF | IXANY);
    master_termios.c_oflag &= ~OPOST;
    master_termios.c_cc[VMIN] = 0;
    master_termios.c_cc[VTIME] = 0;
    tcsetattr(master_fd, TCSANOW, &master_termios);
    
    // Set the master fd for our simulator
    this->master_fd = master_fd;
    
    // Keep slave fd open to maintain PTY connection
    this->slave_fd = slave_fd;
    
    // Also open the slave device from the master side to establish connection
    int test_slave = open(slave_name, O_RDWR | O_NONBLOCK);
    if (test_slave != -1) {
        printf("Opened slave device for testing: %d\n", test_slave);
        close(test_slave);
    } else {
        printf("Failed to open slave device: %s\n", strerror(errno));
    }
    
    // Set non-blocking mode on master
    int flags = fcntl(master_fd, F_GETFL, 0);
    fcntl(master_fd, F_SETFL, flags | O_NONBLOCK);
    
    // Initialize peek buffer
    peek_count = 0;
    
    printf("Serial port created: %s\n", slave_name);
    return std::string(slave_name);
}

int SimSerialClass::available() {
    // If we have peeked bytes, return the count
    if (peek_count > 0) {
        return peek_count;
    }
    
    // Try to read all available bytes
    char temp_buffer[256];
    int total_read = 0;
    
    while (total_read < 256) {
        int n = ::read(master_fd, &temp_buffer[total_read], 1);
        if (n <= 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                break; // No more data available
            }
            printf("read error in available(): %s\n", strerror(errno));
            break;
        }
        total_read++;
    }
    
    if (total_read > 0) {
        // Store all read bytes in peek buffer
        memcpy(peek_buffer, temp_buffer, total_read);
        peek_count = total_read;
        return peek_count;
    }
    
    return 0;
}

int SimSerialClass::read() {
    // If we have peeked bytes, return the first one
    if (peek_count > 0) {
        char c = peek_buffer[0];
        // Shift remaining bytes
        for (int i = 0; i < peek_count - 1; i++) {
            peek_buffer[i] = peek_buffer[i + 1];
        }
        peek_count--;
        return static_cast<uint8_t>(c);
    }
    
    // Otherwise read from the file descriptor
    char c;
    int n = ::read(master_fd, &c, 1);
    if (n <= 0) {
        if (errno == EAGAIN || errno == EWOULDBLOCK) {
            return -1; // No data available
        }
        printf("read error: %s\n", strerror(errno));
        return -1; // Error
    }
    return static_cast<uint8_t>(c);
}

size_t SimSerialClass::write(uint8_t b) {
    return ::write(master_fd, &b, 1);
}

size_t SimSerialClass::write(const char* message, uint8_t msgLen) {
    return ::write(master_fd, message, msgLen);
}

size_t SimSerialClass::readBytes(uint8_t* buffer, uint8_t len) {
    size_t total_read = 0;
    
    // First, use any bytes from the peek buffer
    while (total_read < len && peek_count > 0) {
        buffer[total_read] = static_cast<uint8_t>(peek_buffer[0]);
        // Shift remaining bytes
        for (int i = 0; i < peek_count - 1; i++) {
            peek_buffer[i] = peek_buffer[i + 1];
        }
        peek_count--;
        total_read++;
    }
    
    // If we still need more bytes, read from the file descriptor
    while (total_read < len) {
        int n = ::read(master_fd, buffer + total_read, len - total_read);
        if (n <= 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                break; // No more data available
            }
            break; // Error
        }
        total_read += n;
    }

    return total_read;
}

void SimSerialClass::print(const char* s) {
    ::write(master_fd, s, strlen(s));
}

void SimSerialClass::println(const char* s) {
    ::write(master_fd, s, strlen(s));
    ::write(master_fd, "\r\n", 2);
}

void SimSerialClass::flush() {
    // Force flush of PTY buffer
    tcdrain(master_fd);
}

void SimSerialClass::closeSlave() {
    if (slave_fd != -1) {
        close(slave_fd);
        slave_fd = -1;
        printf("Slave fd closed\n");
    }
}
#endif