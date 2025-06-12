#ifdef SIMULATOR
#include "SimMatrixPanel.h"

SimMatrixPanel::SimMatrixPanel(uint16_t width, uint16_t height)
: Adafruit_GFX(width, height) {}

void SimMatrixPanel::begin() {
    SDL_Init(SDL_INIT_VIDEO);
    window = SDL_CreateWindow("Matrix Simulator", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, _width * scale, _height * scale, 0);
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);
}

void SimMatrixPanel::clearScreen() {
    fillScreenRGB888(0, 0, 0);
}

void SimMatrixPanel::setBrightness8(uint8_t brightness) {
    // TODO: Implement brightness setting
}

void SimMatrixPanel::fillScreen(uint16_t color) {
    fillScreenRGB888((color >> 11) << 3, ((color >> 5) & 0x3F) << 2, (color & 0x1F) << 3);
}

void SimMatrixPanel::fillScreenRGB888(uint8_t r, uint8_t g, uint8_t b) {
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);
}

void SimMatrixPanel::drawPixel(int16_t x, int16_t y, uint16_t color) {
    uint8_t r = (color >> 11) << 3;
    uint8_t g = ((color >> 5) & 0x3F) << 2;
    uint8_t b = (color & 0x1F) << 3;
    drawPixelRGB888(x, y, r, g, b);
}

void SimMatrixPanel::drawPixelRGB888(int16_t x, int16_t y, uint8_t r, uint8_t g, uint8_t b) {
    if (x < 0 || y < 0 || x >= _width || y >= _height) return;
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_Rect rect = { x * scale, y * scale, scale, scale };
    SDL_RenderFillRect(renderer, &rect);
    SDL_RenderPresent(renderer);
}
#endif