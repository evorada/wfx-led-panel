#pragma once

#include <cstdint>
#include <cstring>
#include "ArduinoCompat.h"

// Forward declarations
class Print;
class String;
class __FlashStringHelper;

// Arduino compatibility defines
#define ARDUINO 100
#define HIGH 0x1
#define LOW  0x0
#define INPUT 0x0
#define OUTPUT 0x1
#define INPUT_PULLUP 0x2

// Arduino compatibility functions
inline void pinMode(uint8_t pin, uint8_t mode) {}
inline void digitalWrite(uint8_t pin, uint8_t val) {}
inline int digitalRead(uint8_t pin) { return 0; }
inline void delay(unsigned long ms) {}
inline unsigned long millis() { return 0; }
inline unsigned long micros() { return 0; }

// Arduino compatibility types
typedef uint8_t byte;
typedef bool boolean;
typedef uint16_t word; 