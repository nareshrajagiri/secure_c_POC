
 #ifndef STATUS_INDICATOR_H
 #define STATUS_INDICATOR_H
 #include <stdint.h>
 #define STATUS_INDICATOR_NUM  (6U) /* LEDs: 0 to 5, for positions */
 void StatusIndicator_Init(void);
 void StatusIndicator_Update(uint8_t position_valid, uint8_t logical_position);
 void StatusIndicator_SetPowerLED(uint8_t onoff);
 #endif /* STATUS_INDICATOR_H */

