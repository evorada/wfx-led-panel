#pragma once

#ifdef SIMULATOR
#include "SimMatrixPanel.h"
#include "SimSerial.h"
#else
#include <Arduino.h>
#include <ESP32-HUB75-MatrixPanel-I2S-DMA.h>
#endif

#define START_BYTE 0xAA
#define MAX_SPRITES 16
#define MAX_SPRITE_SIZE 64*64*2  // 64x64 pixels in RGB565 format

// Sprite structure
struct Sprite {
    bool active;
    int x, y;
    int width, height;
    uint8_t data[MAX_SPRITE_SIZE];
    int last_x, last_y;  // For tracking position changes
};

enum CommandType : uint8_t {
    CMD_DRAW_PIXEL = 0x01,
    CMD_FILL_SCREEN = 0x02,
    CMD_DRAW_LINE = 0x03,
    CMD_DRAW_RECT = 0x04,
    CMD_DRAW_TEXT = 0x05,
    CMD_CLEAR = 0x06,
    CMD_SET_BRIGHTNESS = 0x07,
    CMD_PRINT = 0x08,
    CMD_SET_CURSOR = 0x09,
    CMD_FILL_RECT = 0x0A,
    CMD_DRAW_FAST_VLINE = 0x0B,
    CMD_DRAW_FAST_HLINE = 0x0C,
    CMD_DRAW_BITMAP = 0x0D,
    // Sprite commands
    CMD_SET_SPRITE = 0x0E,
    CMD_CLEAR_SPRITE = 0x0F,
    CMD_DRAW_SPRITE = 0x10,
    CMD_MOVE_SPRITE = 0x11,
};

class CommandHandler {
public:
    CommandHandler(MatrixPanel_I2S_DMA* display);
    void handleCommand();

private:
    MatrixPanel_I2S_DMA* dma_display;
    Sprite sprites[MAX_SPRITES];
    void sendAck(uint8_t cmd, bool success, const char* message = nullptr);
    void clearSpriteArea(int sprite_id);
    void drawSpriteAt(int sprite_id, int x, int y);
}; 