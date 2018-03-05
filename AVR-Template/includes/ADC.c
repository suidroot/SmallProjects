/*


*/


#include <avr/io.h>
#include "ADC.h"


void setADCMUXPort(uint8_t port) {

	switch(port) { 
	    case 0: 
	        ADMUX |= (0 << MUX3) | (0 << MUX2) | (0 << MUX1) | (0 << MUX0); /* Set ADC0 */ 
	        break; 
	    case 1: 
	        ADMUX |= (0 << MUX3) | (0 << MUX2) | (0 << MUX1) | (1 << MUX0); /* Set ADC1 */ 
	        break; 
	    case 2: 
	        ADMUX |= (0 << MUX3) | (0 << MUX2) | (1 << MUX1) | (0 << MUX0); /* Set ADC2 */ 
	        break; 
	    case 3: 
	        ADMUX |= (0 << MUX3) | (0 << MUX2) | (1 << MUX1) | (1 << MUX0); /* Set ADC3 */ 
	        break; 
	    case 4: 
	        ADMUX |= (0 << MUX3) | (1 << MUX2) | (0 << MUX1) | (0 << MUX0); /* Set ADC4 */ 
	        break; 
	    case 5: 
	        ADMUX |= (0 << MUX3) | (1 << MUX2) | (0 << MUX1) | (1 << MUX0); /* Set ADC5 */ 
	        break; 
	    case 6: 
	        ADMUX |= (0 << MUX3) | (1 << MUX2) | (1 << MUX1) | (0 << MUX0); /* Set ADC6 */ 
	        break; 
	    case 7: 
	        ADMUX |= (0 << MUX3) | (1 << MUX2) | (1 << MUX1) | (1 << MUX0); /* Set ADC7 */ 
	        break; 
	    case 8: 
	        ADMUX |= (1 << MUX3) | (0 << MUX2) | (0 << MUX1) | (0 << MUX0); /* Set Tempurature Sensor */ 
	        break; 
	}
}



void setADCPrescale(uint8_t scale) {


	switch(port) { 
	    case 2: 
	        ADCSRA |= (0 << ADPS2) | (0 << ADPS1) |(0 << ADPS0);
	        break; 
	    case 4: 
	        ADCSRA |= (0 << ADPS2) | (1 << ADPS1) |(0 << ADPS0);
	        break; 
	    case 8: 
	        ADCSRA |= (0 << ADPS2) | (1 << ADPS1) |(1 << ADPS0);
	        break; 
	    case 16: 
	        ADCSRA |= (1 << ADPS2) | (0 << ADPS1) |(0 << ADPS0);
	        break; 
	    case 32: 
	        ADCSRA |= (1 << ADPS2) | (0 << ADPS1) |(1 << ADPS0);
	        break; 
	    case 64: 
	        ADCSRA |= (1 << ADPS2) | (1 << ADPS1) |(0 << ADPS0);
	        break; 
	    case 128: 
	        ADCSRA |= (1 << ADPS2) | (1 << ADPS1) |(1 << ADPS0);
	        break; 
	    default: 
	        break; 

	}
}




void initSingleADC0 (uint8_t port) {

	setADCMUXPort(port);

	// Reference Voltage on AVCC
	ADMUX |= (1 << REFS0);
	// Enable ADC Clock prescaler 
	ADCSRA |= (1 << ADPS2) | (1 << ADPS0);  // /32 - Prescale
	// Enable ADC
	ADCSRA |= (1 << ADEN);

}

void initFreeRunADC (uint8_t port) {

	setADCMUXPort(port);

	ADMUX |= (1 << REFS0);                     /* reference voltage on AVCC */
	ADCSRA |= (1 << ADPS2) | (1 << ADPS0);     /* ADC clock prescaler /32 */
	ADMUX |= (1 << ADLAR);                     /* left-adjust result, 
												  return only 8 bits */

	ADCSRA |= (1 << ADIE);                     /* ADC Interupt enable */

	ADCSRA |= (1 << ADEN);                     /* enable ADC */
	ADCSRA |= (1 << ADATE);                    /* auto-trigger enable */
	ADCSRA |= (1 << ADSC);                     /* start first conversion */
}
