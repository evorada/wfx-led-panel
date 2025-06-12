#pragma once

#include <SDL2/SDL.h>
#include "Adafruit_GFX.h"

class SimMatrixPanel : public Adafruit_GFX {
public:
    SimMatrixPanel(uint16_t width, uint16_t height);
    void begin();
    void clearScreen();
    void setBrightness8(uint8_t brightness);
    void fillScreen(uint16_t color);
    void drawPixel(int16_t x, int16_t y, uint16_t color) override;
    void drawPixelRGB888(int16_t x, int16_t y, uint8_t r, uint8_t g, uint8_t b);
    void fillScreenRGB888(uint8_t r, uint8_t g, uint8_t b);
    void present();

private:
    SDL_Window* window = nullptr;
    SDL_Renderer* renderer = nullptr;
    int scale = 10;
};

#define MatrixPanel_I2S_DMA SimMatrixPanel