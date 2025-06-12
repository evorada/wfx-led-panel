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

        case CMD_SET_BRIGHTNESS:
            if (len >= 1) {
                uint8_t brightness = data[0];
                dma_display->setBrightness8(brightness);
            }
            break;

        case CMD_PRINT:
            if (len >= 1) {
                // Convert the data to a null-terminated string
                char text[65] = {0};  // 64 chars + null terminator
                memcpy(text, data, len);
                dma_display->print(text);
            }
            break;

        case CMD_SET_CURSOR:
            if (len >= 2) {
                int x = data[0];
                int y = data[1];
                dma_display->setCursor(x, y);
            }
            break;

        case CMD_FILL_RECT:
            if (len >= 7) {
                int x = data[0];
                int y = data[1];
                int w = data[2];
                int h = data[3];
                uint8_t r = data[4];
                uint8_t g = data[5];
                uint8_t b = data[6];
                dma_display->fillRect(x, y, w, h, dma_display->color565(r, g, b));
            }
            break;

        default:
            break;
    }
} 