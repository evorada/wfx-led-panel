#include "command_handler.h"

CommandHandler::CommandHandler(MatrixPanel_I2S_DMA *display) : dma_display(display)
{
    // Initialize all sprites as inactive
    for (int i = 0; i < MAX_SPRITES; i++)
    {
        sprites[i].active = false;
        sprites[i].x = 0;
        sprites[i].y = 0;
        sprites[i].width = 0;
        sprites[i].height = 0;
        sprites[i].last_x = 0;
        sprites[i].last_y = 0;
    }
}

void CommandHandler::sendAck(uint8_t cmd, bool success, const char *message)
{
    // Send acknowledgment packet: START_BYTE + ACK_BYTE + CMD + SUCCESS + optional message
    Serial.write(START_BYTE);
    Serial.write(0xAC); // ACK byte
    Serial.write(cmd);
    Serial.write(success ? 0x01 : 0x00);

    if (message != nullptr)
    {
        uint8_t msgLen = strlen(message);
        Serial.write(msgLen);
        Serial.write(message, msgLen);
    }
    else
    {
        Serial.write(0x00); // No message
    }
}

void CommandHandler::handleCommand()
{
    if (Serial.available() < 3)
        return;

    if (Serial.read() != START_BYTE)
        return;

    uint8_t cmd = Serial.read();
    uint8_t len = Serial.read();

    while (Serial.available() < len)
    {
        delay(1);
    }

    uint8_t data[64];
    Serial.readBytes(data, len);

    switch (cmd)
    {
    case CMD_DRAW_PIXEL:
        if (len >= 5)
        {
            int x = data[0];
            int y = data[1];
            uint8_t r = data[2];
            uint8_t g = data[3];
            uint8_t b = data[4];
            dma_display->drawPixelRGB888(x, y, r, g, b);
            sendAck(cmd, true, "Pixel drawn");
        }
        else
        {
            sendAck(cmd, false, "Invalid pixel data");
        }
        break;

    case CMD_FILL_SCREEN:
        if (len >= 3)
        {
            uint8_t r = data[0];
            uint8_t g = data[1];
            uint8_t b = data[2];
            dma_display->fillScreenRGB888(r, g, b);
            sendAck(cmd, true, "Screen filled");
        }
        else
        {
            sendAck(cmd, false, "Invalid fill data");
        }
        break;

    case CMD_DRAW_LINE:
        if (len >= 7)
        {
            int x0 = data[0];
            int y0 = data[1];
            int x1 = data[2];
            int y1 = data[3];
            uint8_t r = data[4];
            uint8_t g = data[5];
            uint8_t b = data[6];
            dma_display->drawLine(x0, y0, x1, y1, dma_display->color565(r, g, b));
            sendAck(cmd, true, "Line drawn");
        }
        else
        {
            sendAck(cmd, false, "Invalid line data");
        }
        break;

    case CMD_DRAW_RECT:
        if (len >= 7)
        {
            int x = data[0];
            int y = data[1];
            int w = data[2];
            int h = data[3];
            uint8_t r = data[4];
            uint8_t g = data[5];
            uint8_t b = data[6];
            dma_display->drawRect(x, y, w, h, dma_display->color565(r, g, b));
            sendAck(cmd, true, "Rectangle drawn");
        }
        else
        {
            sendAck(cmd, false, "Invalid rectangle data");
        }
        break;

    case CMD_CLEAR:
        dma_display->clearScreen();
        sendAck(cmd, true, "Screen cleared");
        break;

    case CMD_SET_BRIGHTNESS:
        if (len >= 1)
        {
            uint8_t brightness = data[0];
            dma_display->setBrightness8(brightness);
            sendAck(cmd, true, "Brightness set");
        }
        else
        {
            sendAck(cmd, false, "Invalid brightness data");
        }
        break;

    case CMD_PRINT:
        if (len >= 1)
        {
            // Convert the data to a null-terminated string
            char text[65] = {0}; // 64 chars + null terminator
            memcpy(text, data, len);
            dma_display->print(text);
            sendAck(cmd, true, "Text printed");
        }
        else
        {
            sendAck(cmd, false, "Invalid text data");
        }
        break;

    case CMD_SET_CURSOR:
        if (len >= 2)
        {
            int x = data[0];
            int y = data[1];
            dma_display->setCursor(x, y);
            sendAck(cmd, true, "Cursor set");
        }
        else
        {
            sendAck(cmd, false, "Invalid cursor data");
        }
        break;

    case CMD_FILL_RECT:
        if (len >= 7)
        {
            int x = data[0];
            int y = data[1];
            int w = data[2];
            int h = data[3];
            uint8_t r = data[4];
            uint8_t g = data[5];
            uint8_t b = data[6];
            dma_display->fillRect(x, y, w, h, dma_display->color565(r, g, b));
            sendAck(cmd, true, "Rectangle filled");
        }
        else
        {
            sendAck(cmd, false, "Invalid rectangle data");
        }
        break;

    case CMD_DRAW_FAST_VLINE:
        if (len >= 6)
        {
            int x = data[0];
            int y = data[1];
            int h = data[2];
            uint8_t r = data[3];
            uint8_t g = data[4];
            uint8_t b = data[5];
            dma_display->drawFastVLine(x, y, h, dma_display->color565(r, g, b));
            sendAck(cmd, true, "Vertical line drawn");
        }
        else
        {
            sendAck(cmd, false, "Invalid vertical line data");
        }
        break;

    case CMD_DRAW_FAST_HLINE:
        if (len >= 6)
        {
            int x = data[0];
            int y = data[1];
            int w = data[2];
            uint8_t r = data[3];
            uint8_t g = data[4];
            uint8_t b = data[5];
            dma_display->drawFastHLine(x, y, w, dma_display->color565(r, g, b));
            sendAck(cmd, true, "Horizontal line drawn");
        }
        else
        {
            sendAck(cmd, false, "Invalid horizontal line data");
        }
        break;

    case CMD_DRAW_BITMAP:
        if (len >= 4)
        {
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

            while (total_read < payload_size)
            {
                // Check for timeout
                if (millis() - start_time > timeout_ms)
                {
                    sendAck(cmd, false, "Bitmap data read timeout");
                    break;
                }

                // Wait for data to be available and manage buffer
                if (Serial.available() < 2)
                {
                    // If buffer is getting full, flush it to make room
                    if (Serial.available() > 0)
                    {
                        Serial.flush();
                    }
                    delay(1);
                    continue;
                }

                // Read one pixel (2 bytes)
                int read_size = Serial.readBytes(pixel_buffer, 2);
                if (read_size == 2)
                {
                    // Calculate pixel position
                    int pixel_index = total_read / 2;
                    int py = pixel_index / width;
                    int px = pixel_index % width;

                    // Only draw if within bounds
                    if (py < height && px < width)
                    {
                        // Read RGB565 color (2 bytes)
                        uint16_t color = (pixel_buffer[0] << 8) | pixel_buffer[1];
                        dma_display->drawPixel(x + px, y + py, color);
                    }
                    total_read += 2;

                    // Send simple flow control every 64 pixels to keep data flowing
                    // But not after the last chunk to avoid interfering with final ACK
                    if ((total_read / 2) % 64 == 0 && total_read < payload_size - 2)
                    {
                        // Send a simple "ready" byte to keep the sender going
                        Serial.write(0xFF); // Simple ready signal (different from ACK protocol)
                    }
                }
            }
            sendAck(cmd, true, "");
        }
        else
        {
            sendAck(cmd, false, "Invalid bitmap header");
        }
        break;

    case CMD_SET_SPRITE:
        if (len >= 4)
        {
            uint8_t sprite_id = data[0];
            int x = data[1];
            int y = data[2];
            int width = data[3];
            int height = data[4];

            if (sprite_id >= MAX_SPRITES)
            {
                sendAck(cmd, false, "Invalid sprite ID");
                break;
            }

            int payload_size = width * height * 2; // RGB565 = 2 bytes per pixel
            if (payload_size > MAX_SPRITE_SIZE)
            {
                sendAck(cmd, false, "Sprite too large");
                break;
            }

            // Clear the sprite area if it was previously active
            if (sprites[sprite_id].active)
            {
                clearSpriteArea(sprite_id);
            }

            // Read sprite data with flow control
            int total_read = 0;
            int timeout_ms = 5000;
            unsigned long start_time = millis();
            uint8_t pixel_buffer[2];

            while (total_read < payload_size)
            {
                if (millis() - start_time > timeout_ms)
                {
                    sendAck(cmd, false, "Sprite data read timeout");
                    break;
                }

                if (Serial.available() < 2)
                {
                    if (Serial.available() > 0)
                    {
                        Serial.flush();
                    }
                    delay(1);
                    continue;
                }

                int read_size = Serial.readBytes(pixel_buffer, 2);
                if (read_size == 2)
                {
                    sprites[sprite_id].data[total_read] = pixel_buffer[0];
                    sprites[sprite_id].data[total_read + 1] = pixel_buffer[1];
                    total_read += 2;

                    if ((total_read / 2) % 64 == 0 && total_read < payload_size - 2)
                    {
                        Serial.write(0xFF);
                    }
                }
            }

            // Set sprite properties
            sprites[sprite_id].active = true;
            sprites[sprite_id].x = x;
            sprites[sprite_id].y = y;
            sprites[sprite_id].width = width;
            sprites[sprite_id].height = height;
            sprites[sprite_id].last_x = x;
            sprites[sprite_id].last_y = y;

            sendAck(cmd, true, "Sprite set");
        }
        else
        {
            sendAck(cmd, false, "Invalid sprite data");
        }
        break;

    case CMD_CLEAR_SPRITE:
        if (len >= 1)
        {
            uint8_t sprite_id = data[0];
            if (sprite_id >= MAX_SPRITES)
            {
                sendAck(cmd, false, "Invalid sprite ID");
                break;
            }

            if (sprites[sprite_id].active)
            {
                clearSpriteArea(sprite_id);
                sprites[sprite_id].active = false;
                sendAck(cmd, true, "Sprite cleared");
            }
            else
            {
                sendAck(cmd, false, "Sprite not active");
            }
        }
        else
        {
            sendAck(cmd, false, "Invalid sprite ID");
        }
        break;

    case CMD_DRAW_SPRITE:
        if (len >= 3)
        {
            uint8_t sprite_id = data[0];
            int x = data[1];
            int y = data[2];

            if (sprite_id >= MAX_SPRITES)
            {
                sendAck(cmd, false, "Invalid sprite ID");
                break;
            }

            if (!sprites[sprite_id].active)
            {
                sendAck(cmd, false, "Sprite not active");
                break;
            }

            drawSpriteAt(sprite_id, x, y);
            sendAck(cmd, true, "Sprite drawn");
        }
        else
        {
            sendAck(cmd, false, "Invalid draw sprite data");
        }
        break;

    case CMD_MOVE_SPRITE:
        if (len >= 3)
        {
            uint8_t sprite_id = data[0];
            int x = data[1];
            int y = data[2];

            if (sprite_id >= MAX_SPRITES)
            {
                sendAck(cmd, false, "Invalid sprite ID");
                break;
            }

            if (!sprites[sprite_id].active)
            {
                sendAck(cmd, false, "Sprite not active");
                break;
            }

            drawSpriteAt(sprite_id, x, y);
            sprites[sprite_id].x = x;
            sprites[sprite_id].y = y;
            sendAck(cmd, true, "Sprite moved");
        }
        else
        {
            sendAck(cmd, false, "Invalid move sprite data");
        }
        break;

    default:
        sendAck(cmd, false, "Unknown command");
        break;
    }
}

void CommandHandler::clearSpriteArea(int sprite_id)
{
    if (sprite_id < 0 || sprite_id >= MAX_SPRITES || !sprites[sprite_id].active)
    {
        return;
    }

    Sprite &sprite = sprites[sprite_id];
    // Clear the area where the sprite was last drawn
    dma_display->fillRect(sprite.last_x, sprite.last_y, sprite.width, sprite.height, 0x0000);
}

void CommandHandler::drawSpriteAt(int sprite_id, int x, int y)
{
    if (sprite_id < 0 || sprite_id >= MAX_SPRITES || !sprites[sprite_id].active)
    {
        return;
    }

    Sprite &sprite = sprites[sprite_id];

    // Clear the previous position if it was different
    if (sprite.last_x != x || sprite.last_y != y)
    {
        clearSpriteArea(sprite_id);
    }

    // Draw the sprite at the new position
    for (int py = 0; py < sprite.height; py++)
    {
        for (int px = 0; px < sprite.width; px++)
        {
            int pixel_index = (py * sprite.width + px) * 2;
            if (pixel_index + 1 < sprite.width * sprite.height * 2)
            {
                uint16_t color = (sprite.data[pixel_index] << 8) | sprite.data[pixel_index + 1];
                dma_display->drawPixel(x + px, y + py, color);
            }
        }
    }

    // Update position tracking
    sprite.last_x = x;
    sprite.last_y = y;
}