
 #ifndef POSITION_SENSING_H
 #define POSITION_SENSING_H
 #include <stdint.h>
 #define FLAP_POSITION_NUM   (6U) /* 0 to 5 */
 #define FLAP_POSITION_INVALID (0xFFU)
 typedef struct
 {
     uint16_t adc_min;
     uint16_t adc_max;
 } PositionRange_t;
 void PositionSensing_Init(void);
 void PositionSensing_Update(void);
 uint8_t PositionSensing_GetPosition(uint8_t *pos_out);
 uint8_t PositionSensing_IsValid(void);
 uint8_t PositionSensing_IsAtTarget(uint8_t target);

 #endif /* POSITION_SENSING_H */

