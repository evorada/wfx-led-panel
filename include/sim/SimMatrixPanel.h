#pragma once

#include <SDL.h>
#include "Adafruit_GFX.h"

class SimMatrixPanel : public Adafruit_GFX {
public:
    SimMatrixPanel(uint16_t width, uint16_t height);
    ~SimMatrixPanel();
    void begin();
    void clearScreen();
    void setBrightness8(uint8_t brightness);
    void fillScreen(uint16_t color);
    void drawPixel(int16_t x, int16_t y, uint16_t color) override;
    void drawPixelRGB888(int16_t x, int16_t y, uint8_t r, uint8_t g, uint8_t b);
    void fillScreenRGB888(uint8_t r, uint8_t g, uint8_t b);
    uint16_t color565(uint8_t r, uint8_t g, uint8_t b);
    void color565ToRGB888(uint16_t color, uint8_t& r, uint8_t& g, uint8_t& b);
    void drawLine(int16_t x0, int16_t y0, int16_t x1, int16_t y1, uint16_t color);
    void drawRect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color);
    void fillRect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color);
    void drawFastVLine(int16_t x, int16_t y, int16_t h, uint16_t color);
    void drawFastHLine(int16_t x, int16_t y, int16_t w, uint16_t color);
    void setCursor(int16_t x, int16_t y);
    size_t print(const char* text);
    void present();

private:
    SDL_Window* window = nullptr;
    SDL_Renderer* renderer = nullptr;
    SDL_Texture* canvas = nullptr;
    static const int scale = 10;
};

#define MatrixPanel_I2S_DMA SimMatrixPanel