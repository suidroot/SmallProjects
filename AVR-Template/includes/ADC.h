/*
	

*/

#define ADC0_MUX 	0
#define ADC1_MUX 	1
#define ADC2_MUX 	2
#define ADC3_MUX 	3
#define ADC4_MUX 	4
#define ADC5_MUX 	5
#define ADC6_MUX 	6
#define ADC7_MUX 	7
#define TEMP_MUX 	8

#define ADC_PRESCALE_2 2
#define ADC_PRESCALE_4 4
#define ADC_PRESCALE_8 8
#define ADC_PRESCALE_16 16
#define ADC_PRESCALE_32 32
#define ADC_PRESCALE_64 64
#define ADC_PRESCALE_128 128

#define STARTADC ADCSRA |= (1 << ADSC);

void initFreeRunADC (uint8_t port);
void initSingleADC0 (uint8_t port);
void setADCMUXPort (uint8_t port);

