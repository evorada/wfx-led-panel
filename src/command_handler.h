#pragma once

#include <Arduino.h>
#include "ESP32-HUB75-MatrixPanel-I2S-DMA.h"

#define START_BYTE 0xAA

enum CommandType : uint8_t {
    CMD_DRAW_PIXEL = 0x01,
    CMD_FILL_SCREEN = 0x02,
    CMD_DRAW_LINE = 0x03,
    CMD_DRAW_RECT = 0x04,
    CMD_DRAW_TEXT = 0x05,
    CMD_CLEAR = 0x06,
};

class CommandHandler {
public:
    CommandHandler(MatrixPanel_I2S_DMA* display);
    void handleCommand();

private:
    MatrixPanel_I2S_DMA* dma_display;
}; 