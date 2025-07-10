#ifdef SIMULATOR
#include "SimMatrixPanel.h"

SimMatrixPanel::SimMatrixPanel(uint16_t width, uint16_t height)
: Adafruit_GFX(width, height) {
    // Initialize member variables explicitly
    window = nullptr;
    renderer = nullptr;
    canvas = nullptr;
}

SimMatrixPanel::~SimMatrixPanel() {
    if (canvas) {
        SDL_DestroyTexture(canvas);
        canvas = nullptr;
    }
    if (renderer) {
        SDL_DestroyRenderer(renderer);
        renderer = nullptr;
    }
    if (window) {
        SDL_DestroyWindow(window);
        window = nullptr;
    }
    SDL_Quit();
}

void SimMatrixPanel::begin() {
    SDL_Init(SDL_INIT_VIDEO);
    
    // Debug output to see what dimensions we're working with
    printf("Creating window with dimensions: %dx%d (scale: %d)\n", _width, _height, scale);
    printf("Window size will be: %dx%d\n", _width * scale, _height * scale);
    
    window = SDL_CreateWindow("WFx LED Panel Simulator", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, _width * scale, _height * scale, 0);
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    
    // Create canvas texture at native resolution
    canvas = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, _width, _height);
    
    // Set render target to canvas
    SDL_SetRenderTarget(renderer, canvas);
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);
    
    // Reset render target to default
    SDL_SetRenderTarget(renderer, nullptr);
    
    // Initial present
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
    SDL_SetRenderTarget(renderer, canvas);
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_RenderClear(renderer);
    SDL_SetRenderTarget(renderer, nullptr);
}

uint16_t SimMatrixPanel::color565(uint8_t r, uint8_t g, uint8_t b) {
    // Convert RGB888 to RGB565
    // R: 8 bits -> 5 bits (shift right by 3)
    // G: 8 bits -> 6 bits (shift right by 2) 
    // B: 8 bits -> 5 bits (shift right by 3)
    uint16_t r565 = (r >> 3) & 0x1F;
    uint16_t g565 = (g >> 2) & 0x3F;
    uint16_t b565 = (b >> 3) & 0x1F;
    return (r565 << 11) | (g565 << 5) | b565;
}

void SimMatrixPanel::color565ToRGB888(uint16_t color, uint8_t& r, uint8_t& g, uint8_t& b) {
    // Convert RGB565 to RGB888
    r = ((color >> 11) & 0x1F) << 3;
    g = ((color >> 5) & 0x3F) << 2;
    b = (color & 0x1F) << 3;
}

void SimMatrixPanel::drawPixel(int16_t x, int16_t y, uint16_t color) {
    uint8_t r, g, b;
    color565ToRGB888(color, r, g, b);
    drawPixelRGB888(x, y, r, g, b);
}

void SimMatrixPanel::drawPixelRGB888(int16_t x, int16_t y, uint8_t r, uint8_t g, uint8_t b) {
    if (x < 0 || y < 0 || x >= _width || y >= _height) return;
    SDL_SetRenderTarget(renderer, canvas);
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_Rect rect = { x, y, 1, 1 };
    SDL_RenderFillRect(renderer, &rect);
    SDL_SetRenderTarget(renderer, nullptr);
}

void SimMatrixPanel::drawLine(int16_t x0, int16_t y0, int16_t x1, int16_t y1, uint16_t color) {
    uint8_t r, g, b;
    color565ToRGB888(color, r, g, b);
    SDL_SetRenderTarget(renderer, canvas);
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_RenderDrawLine(renderer, x0, y0, x1, y1);
    SDL_SetRenderTarget(renderer, nullptr);
}

void SimMatrixPanel::drawRect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color) {
    uint8_t r, g, b;
    color565ToRGB888(color, r, g, b);
    SDL_SetRenderTarget(renderer, canvas);
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_Rect rect = { x, y, w, h };
    SDL_RenderDrawRect(renderer, &rect);
    SDL_SetRenderTarget(renderer, nullptr);
}

void SimMatrixPanel::fillRect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color) {
    uint8_t r, g, b;
    color565ToRGB888(color, r, g, b);
    SDL_SetRenderTarget(renderer, canvas);
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_Rect rect = { x, y, w, h };
    SDL_RenderFillRect(renderer, &rect);
    SDL_SetRenderTarget(renderer, nullptr);
}

void SimMatrixPanel::drawFastVLine(int16_t x, int16_t y, int16_t h, uint16_t color) {
    uint8_t r, g, b;
    color565ToRGB888(color, r, g, b);
    SDL_SetRenderTarget(renderer, canvas);
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_Rect rect = { x, y, 1, h };
    SDL_RenderFillRect(renderer, &rect);
    SDL_SetRenderTarget(renderer, nullptr);
}

void SimMatrixPanel::drawFastHLine(int16_t x, int16_t y, int16_t w, uint16_t color) {
    uint8_t r, g, b;
    color565ToRGB888(color, r, g, b);
    SDL_SetRenderTarget(renderer, canvas);
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_Rect rect = { x, y, w, 1 };
    SDL_RenderFillRect(renderer, &rect);
    SDL_SetRenderTarget(renderer, nullptr);
}

void SimMatrixPanel::setCursor(int16_t x, int16_t y) {
    cursor_x = x;
    cursor_y = y;
}

size_t SimMatrixPanel::print(const char* text) {
    // Simple text rendering - just draw each character as a colored pixel
    // This is a basic implementation for the simulator
    int16_t x = cursor_x;
    int16_t y = cursor_y;
    size_t chars_written = 0;
    
    for (int i = 0; text[i] != '\0'; i++) {
        if (text[i] == '\n') {
            x = cursor_x;
            y += 8;
        } else if (text[i] == '\r') {
            x = cursor_x;
        } else {
            // Draw a simple character representation
            uint16_t color = color565(255, 255, 255); // White text
            drawPixel(x, y, color);
            x += 6; // Character width
            
            if (x >= _width) {
                x = cursor_x;
                y += 8;
            }
        }
        chars_written++;
    }
    
    cursor_x = x;
    cursor_y = y;
    return chars_written;
}

void SimMatrixPanel::present() {
    // Copy canvas to renderer with proper scaling
    SDL_Rect destRect = {0, 0, _width * scale, _height * scale};
    SDL_RenderCopy(renderer, canvas, nullptr, &destRect);
    SDL_RenderPresent(renderer);
}
#endif