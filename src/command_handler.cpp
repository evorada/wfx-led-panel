#include "command_handler.h"

CommandHandler::CommandHandler(MatrixPanel_I2S_DMA* display) : dma_display(display) {}

void CommandHandler::sendAck(uint8_t cmd, bool success, const char* message) {
    // Send acknowledgment packet: START_BYTE + ACK_BYTE + CMD + SUCCESS + optional message
    Serial.write(START_BYTE);
    Serial.write(0xAC); // ACK byte
    Serial.write(cmd);
    Serial.write(success ? 0x01 : 0x00);
    
    if (message != nullptr) {
        uint8_t msgLen = strlen(message);
        Serial.write(msgLen);
        Serial.write(message, msgLen);
    } else {
        Serial.write(0x00); // No message
    }
}

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
                sendAck(cmd, true, "Pixel drawn");
            } else {
                sendAck(cmd, false, "Invalid pixel data");
            }
            break;

        case CMD_FILL_SCREEN:
            if (len >= 3) {
                uint8_t r = data[0];
                uint8_t g = data[1];
                uint8_t b = data[2];
                dma_display->fillScreenRGB888(r, g, b);
                sendAck(cmd, true, "Screen filled");
            } else {
                sendAck(cmd, false, "Invalid fill data");
            }
            break;

        case CMD_DRAW_LINE:
            if (len >= 7) {
                int x0 = data[0];
                int y0 = data[1];
                int x1 = data[2];
                int y1 = data[3];
                uint8_t r = data[4];
                uint8_t g = data[5];
                uint8_t b = data[6];
                dma_display->drawLine(x0, y0, x1, y1, dma_display->color565(r, g, b));
                sendAck(cmd, true, "Line drawn");
            } else {
                sendAck(cmd, false, "Invalid line data");
            }
            break;

        case CMD_DRAW_RECT:
            if (len >= 7) {
                int x = data[0];
                int y = data[1];
                int w = data[2];
                int h = data[3];
                uint8_t r = data[4];
                uint8_t g = data[5];
                uint8_t b = data[6];
                dma_display->drawRect(x, y, w, h, dma_display->color565(r, g, b));
                sendAck(cmd, true, "Rectangle drawn");
            } else {
                sendAck(cmd, false, "Invalid rectangle data");
            }
            break;

        case CMD_CLEAR:
            dma_display->clearScreen();
            sendAck(cmd, true, "Screen cleared");
            break;

        case CMD_SET_BRIGHTNESS:
            if (len >= 1) {
                uint8_t brightness = data[0];
                dma_display->setBrightness8(brightness);
                sendAck(cmd, true, "Brightness set");
            } else {
                sendAck(cmd, false, "Invalid brightness data");
            }
            break;

        case CMD_PRINT:
            if (len >= 1) {
                // Convert the data to a null-terminated string
                char text[65] = {0};  // 64 chars + null terminator
                memcpy(text, data, len);
                dma_display->print(text);
                sendAck(cmd, true, "Text printed");
            } else {
                sendAck(cmd, false, "Invalid text data");
            }
            break;

        case CMD_SET_CURSOR:
            if (len >= 2) {
                int x = data[0];
                int y = data[1];
                dma_display->setCursor(x, y);
                sendAck(cmd, true, "Cursor set");
            } else {
                sendAck(cmd, false, "Invalid cursor data");
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
                sendAck(cmd, true, "Rectangle filled");
            } else {
                sendAck(cmd, false, "Invalid rectangle data");
            }
            break;

        case CMD_DRAW_FAST_VLINE:
            if (len >= 6) {
                int x = data[0];
                int y = data[1];
                int h = data[2];
                uint8_t r = data[3];
                uint8_t g = data[4];
                uint8_t b = data[5];
                dma_display->drawFastVLine(x, y, h, dma_display->color565(r, g, b));
                sendAck(cmd, true, "Vertical line drawn");
            } else {
                sendAck(cmd, false, "Invalid vertical line data");
            }
            break;

        case CMD_DRAW_FAST_HLINE:
            if (len >= 6) {
                int x = data[0];
                int y = data[1];
                int w = data[2];
                uint8_t r = data[3];
                uint8_t g = data[4];
                uint8_t b = data[5];
                dma_display->drawFastHLine(x, y, w, dma_display->color565(r, g, b));
                sendAck(cmd, true, "Horizontal line drawn");
            } else {
                sendAck(cmd, false, "Invalid horizontal line data");
            }
            break;

        case CMD_DRAW_BITMAP:
            if (len >= 4) {
                int x = data[0];
                int y = data[1];
                int width = data[2];
                int height = data[3];

                int payload_size = width * height * 2; // RGB565 = 2 bytes per pixel
                uint8_t bitmap_data[payload_size];
                
                // Read and draw bitmap data pixel by pixel as it arrives
                int total_read = 0;
                int timeout_ms = 5000; // 5 second timeout
                unsigned long start_time = millis();
                uint8_t pixel_buffer[2]; // 2 bytes for RGB565 pixel
                
                while (total_read < payload_size) {
                    // Check for timeout
                    if (millis() - start_time > timeout_ms) {
                        sendAck(cmd, false, "Bitmap data read timeout");
                        break;
                    }
                    
                    // Wait for data to be available and manage buffer
                    if (Serial.available() < 2) {
                        // If buffer is getting full, flush it to make room
                        if (Serial.available() > 0) {
                            Serial.flush();
                        }
                        delay(1);
                        continue;
                    }
                    
                    // Read one pixel (2 bytes)
                    int read_size = Serial.readBytes(pixel_buffer, 2);
                    if (read_size == 2) {
                        // Calculate pixel position
                        int pixel_index = total_read / 2;
                        int py = pixel_index / width;
                        int px = pixel_index % width;
                        
                        // Only draw if within bounds
                        if (py < height && px < width) {
                            // Read RGB565 color (2 bytes)
                            uint16_t color = (pixel_buffer[0] << 8) | pixel_buffer[1];
                            dma_display->drawPixel(x + px, y + py, color);
                        }
                        total_read += 2;
                        
                        // Send simple flow control every 64 pixels to keep data flowing
                        // But not after the last chunk to avoid interfering with final ACK
                        if ((total_read / 2) % 64 == 0 && total_read < payload_size - 2) {
                            // Send a simple "ready" byte to keep the sender going
                            Serial.write(0xFF); // Simple ready signal (different from ACK protocol)
                        }
                    }
                }
                sendAck(cmd, true, "");
            } else {
                sendAck(cmd, false, "Invalid bitmap header");
            }
            break;

        default:
            sendAck(cmd, false, "Unknown command");
            break;
    }
} 