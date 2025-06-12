#if defined(WF1)
  #include "hd-wf1-esp32s2-config.h"
#elif defined(WF2)
  #include "hd-wf2-esp32s3-config.h"
#else
  #error "Please define either WF1 or WF2"
#endif

#include <Arduino.h>
#include <ESP32-HUB75-MatrixPanel-I2S-DMA.h>
#include <Bounce2.h>

/*-------------------------- HUB75E DMA Setup -----------------------------*/
#define PANEL_RES_X 64      // Number of pixels wide of each INDIVIDUAL panel module. 
#define PANEL_RES_Y 32     // Number of pixels tall of each INDIVIDUAL panel module.
#define PANEL_CHAIN 1      // Total number of panels chained one to another


#if defined(WF1)

HUB75_I2S_CFG::i2s_pins _pins_x1 = {WF1_R1_PIN, WF1_G1_PIN, WF1_B1_PIN, WF1_R2_PIN, WF1_G2_PIN, WF1_B2_PIN, WF1_A_PIN, WF1_B_PIN, WF1_C_PIN, WF1_D_PIN, WF1_E_PIN, WF1_LAT_PIN, WF1_OE_PIN, WF1_CLK_PIN};

#else

HUB75_I2S_CFG::i2s_pins _pins_x1 = {WF2_X1_R1_PIN, WF2_X1_G1_PIN, WF2_X1_B1_PIN, WF2_X1_R2_PIN, WF2_X1_G2_PIN, WF2_X1_B2_PIN, WF2_A_PIN, WF2_B_PIN, WF2_C_PIN, WF2_D_PIN, WF2_X1_E_PIN, WF2_LAT_PIN, WF2_OE_PIN, WF2_CLK_PIN};
HUB75_I2S_CFG::i2s_pins _pins_x2 = {WF2_X2_R1_PIN, WF2_X2_G1_PIN, WF2_X2_B1_PIN, WF2_X2_R2_PIN, WF2_X2_G2_PIN, WF2_X2_B2_PIN, WF2_A_PIN, WF2_B_PIN, WF2_C_PIN, WF2_D_PIN, WF2_X2_E_PIN, WF2_LAT_PIN, WF2_OE_PIN, WF2_CLK_PIN};

#endif

MatrixPanel_I2S_DMA *dma_display = nullptr;
Bounce2::Button button = Bounce2::Button();

// ROS Task management
TaskHandle_t Task1;
TaskHandle_t Task2;

#include "led_pwm_handler.h"

volatile bool buttonPressed = false;

IRAM_ATTR void toggleButtonPressed() {
  // This function will be called when the interrupt occurs on pin PUSH_BUTTON_PIN
  buttonPressed = true;
  ESP_LOGI("toggleButtonPressed", "Interrupt Triggered.");

   esp_deep_sleep_start();      // Sleep for e.g. 30 minutes
  // Do something here
}

#define START_BYTE 0xAA

enum CommandType : uint8_t {
    CMD_DRAW_PIXEL = 0x01,
    CMD_FILL_SCREEN = 0x02,
    CMD_DRAW_LINE = 0x03,
    CMD_DRAW_RECT = 0x04,
    CMD_DRAW_TEXT = 0x05,
    CMD_CLEAR = 0x06,
};

void setupMatrix() {
    // Module configuration
    HUB75_I2S_CFG mxconfig(
      PANEL_RES_X,   // module width
      PANEL_RES_Y,   // module height
      PANEL_CHAIN,   // Chain length
      _pins_x1       // pin mapping for port X1
    );
    mxconfig.i2sspeed = HUB75_I2S_CFG::HZ_20M;  
    mxconfig.latch_blanking = 4;
    //mxconfig.clkphase = false;
    //mxconfig.driver = HUB75_I2S_CFG::FM6126A;
    //mxconfig.double_buff = false;  
    //mxconfig.min_refresh_rate = 30;


    // Display Setup
    dma_display = new MatrixPanel_I2S_DMA(mxconfig);
    dma_display->begin();
    dma_display->setBrightness8(128); //0-255
    dma_display->clearScreen();
}

void handleCommand() {
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

        // Add more cases for CMD_DRAW_LINE, CMD_DRAW_RECT, etc.

        default:
            break;
    }
}

void setup() {
    Serial.begin(115200);
    setupMatrix();
}

void loop() {
    handleCommand();
}
