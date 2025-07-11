#ifdef SIMULATOR
#include "SimMatrixPanel.h"
#include "SimSerial.h"
#else
#if defined(WF1)
#include "hd_wf1_esp32s2_config.h"
#elif defined(WF2)
#include "hd_wf2_esp32s3_config.h"
#endif
#include <Arduino.h>
#include <ESP32-HUB75-MatrixPanel-I2S-DMA.h>
#include <Bounce2.h>
#endif

#include "command_handler.h"

/*-------------------------- HUB75E DMA Setup -----------------------------*/
#define PANEL_RES_X 64 // Number of pixels wide of each INDIVIDUAL panel module.
#define PANEL_RES_Y 64 // Number of pixels tall of each INDIVIDUAL panel module.
#define PANEL_CHAIN 1  // Total number of panels chained one to another

#ifdef SIMULATOR
SimMatrixPanel *dma_display = nullptr;
#else
#if defined(WF1)
HUB75_I2S_CFG::i2s_pins _pins_x1 = {WF1_R1_PIN, WF1_G1_PIN, WF1_B1_PIN, WF1_R2_PIN, WF1_G2_PIN, WF1_B2_PIN, WF1_A_PIN, WF1_B_PIN, WF1_C_PIN, WF1_D_PIN, WF1_E_PIN, WF1_LAT_PIN, WF1_OE_PIN, WF1_CLK_PIN};
#elif defined(WF2)
HUB75_I2S_CFG::i2s_pins _pins_x1 = {WF2_X1_R1_PIN, WF2_X1_G1_PIN, WF2_X1_B1_PIN, WF2_X1_R2_PIN, WF2_X1_G2_PIN, WF2_X1_B2_PIN, WF2_A_PIN, WF2_B_PIN, WF2_C_PIN, WF2_D_PIN, WF2_X1_E_PIN, WF2_LAT_PIN, WF2_OE_PIN, WF2_CLK_PIN};
HUB75_I2S_CFG::i2s_pins _pins_x2 = {WF2_X2_R1_PIN, WF2_X2_G1_PIN, WF2_X2_B1_PIN, WF2_X2_R2_PIN, WF2_X2_G2_PIN, WF2_X2_B2_PIN, WF2_A_PIN, WF2_B_PIN, WF2_C_PIN, WF2_D_PIN, WF2_X2_E_PIN, WF2_LAT_PIN, WF2_OE_PIN, WF2_CLK_PIN};
#endif

Bounce2::Button button = Bounce2::Button();

// ROS Task management
TaskHandle_t Task1;
TaskHandle_t Task2;
#include "led_pwm_handler.h"

MatrixPanel_I2S_DMA *dma_display = nullptr;
#endif
CommandHandler *commandHandler = nullptr;

void setupMatrix()
{
#ifdef SIMULATOR
    dma_display = new SimMatrixPanel(PANEL_RES_X, PANEL_RES_Y);
    dma_display->begin();
#else
    // Module configuration
    HUB75_I2S_CFG mxconfig(
        PANEL_RES_X, // module width
        PANEL_RES_Y, // module height
        PANEL_CHAIN, // Chain length
        _pins_x2     // pin mapping for port X1
    );
    mxconfig.i2sspeed = HUB75_I2S_CFG::HZ_10M;
    mxconfig.latch_blanking = 8;

    // Display Setup
    dma_display = new MatrixPanel_I2S_DMA(mxconfig);
    dma_display->begin();
#endif
    dma_display->setBrightness8(32); // 0-255
    dma_display->clearScreen();

    // Initialize command handler
    commandHandler = new CommandHandler(dma_display);
}

void setup()
{
    Serial.begin(115200);
    setupMatrix();

#ifdef SIMULATOR
    std::string serial_port = Serial.init();
    printf("Simulator ready. Serial port: %s\n", serial_port.c_str());

    dma_display->present(); // Present the drawing immediately
#else
    // BUTTON SETUP
    button.attach(PUSH_BUTTON_PIN, INPUT); // USE EXTERNAL PULL-UP
    button.interval(5);                    // DEBOUNCE INTERVAL IN MILLISECONDS
    button.setPressedState(LOW);           // INDICATE THAT THE LOW STATE CORRESPONDS TO PHYSICALLY PRESSING THE BUTTON

    /*-------------------- LEDC Controller --------------------*/
    // Prepare and then apply the LEDC PWM timer configuration
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .duty_resolution = LEDC_TIMER_13_BIT,
        .timer_num = LEDC_TIMER_0,
        .freq_hz = 4000, // Set output frequency at 4 kHz
        .clk_cfg = LEDC_AUTO_CLK};
    ESP_ERROR_CHECK(ledc_timer_config(&ledc_timer));

    // Prepare and then apply the LEDC PWM channel configuration
    ledc_channel_config_t ledc_channel = {
        .gpio_num = RUN_LED_PIN,
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .channel = LEDC_CHANNEL_0,
        .intr_type = LEDC_INTR_DISABLE,
        .timer_sel = LEDC_TIMER_0,
        .duty = 0, // Set duty to 0%
        .hpoint = 0};
    ESP_ERROR_CHECK(ledc_channel_config(&ledc_channel));

    // Start fading that LED
    xTaskCreatePinnedToCore(
        ledFadeTask,   /* Task function. */
        "ledFadeTask", /* name of task. */
        1000,          /* Stack size of task */
        NULL,          /* parameter of the task */
        1,             /* priority of the task */
        &Task1,        /* Task handle to keep track of created task */
        0);            /* Core */
#endif
}

void loop()
{
#ifdef SIMULATOR
    dma_display->present();
#else
    button.update();
    if (button.pressed())
    {
        ESP.restart();
    }
#endif
    commandHandler->handleCommand();
}

#ifdef SIMULATOR
int main() {
    setup();
    
    while (true) {
        // Handle SDL events
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                SDL_Quit();
                return 0;
            }
        }
        
        // Handle commands (non-blocking)
        commandHandler->handleCommand();
        
        // Present the display regularly
        dma_display->present();
        
        SDL_Delay(16); // ~60 FPS
    }
    return 0;
}
#endif
