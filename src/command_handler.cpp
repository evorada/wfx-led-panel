#include "command_handler.h"

CommandHandler::CommandHandler(MatrixPanel_I2S_DMA* display) : dma_display(display) {}

void CommandHandler::handleCommand() {
    if (Serial.available() < 3) return;

    if (Serial.read() != START_BYTE) return;

    uint8_t cmd = Serial.read();
    uint8_t len = Serial.read();

    while (Serial.available() < len) {
        delay(1);
    }

    uint8_t data[64];
    Serial.readBytes(data, len);

    switch (cmd) {
        case CMD_DRAW_PIXEL:
            if (len >= 5) {
                int x = data[0];
                int y = data[1];
                uint8_t r = data[2];
                uint8_t g = data[3];
                uint8_t b = data[4];
                dma_display->drawPixelRGB888(x, y, r, g, b);
            }
            break;

        case CMD_FILL_SCREEN:
            if (len >= 3) {
                uint8_t r = data[0];
                uint8_t g = data[1];
                uint8_t b = data[2];
                dma_display->fillScreenRGB888(r, g, b);
            }
            break;

        case CMD_CLEAR:
            dma_display->clearScreen();
            break;

        default:
            break;
    }
} 