#include "sapi.h"
#include "arm_math.h"

uint32_t tick	= 0   ;
uint16_t tone	= 100 ;
uint16_t B		= 2000;
uint16_t sweept = 5;

struct header_struct {
   char		pre[8];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   uint32_t maxIndex;
   uint32_t minIndex;
   q15_t maxValue;
   q15_t minValue;
   q15_t rms;
   char  pos[4];
} header={"*header*",0,256,10000,0,0,0,0,0,"end*"};

void trigger(int16_t threshold)
{
   while((adcRead(CH1)-512)>threshold)
	  ;
   while((adcRead(CH1)-512)<threshold)
	  ;
   return;
}

int main ( void ) {
   uint16_t sample = 0;
   int16_t adc [ header.N ];
   boardConfig (				  );
   uartConfig  ( UART_USB, 460800 );
   adcConfig   ( ADC_ENABLE		  );
   dacConfig   ( DAC_ENABLE		  );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );
   while(1) {
	  cyclesCounterReset();
	  adc[sample] = ((adcRead(CH1)-512))<<6;
	  uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample] ,sizeof(adc[0]) );
	  float t=((tick%(sweept*header.fs))/(float)header.fs);
	  tick++;
	  dacWrite( DAC, 512*arm_sin_f32 (t*B/2*(t/sweept)*2*PI)+512); // sweept
	  if ( ++sample==header.N ) {
		 gpioToggle ( LEDR ); // este led blinkea a fs/N
		 arm_max_q15 ( adc, header.N, &header.maxValue,&header.maxIndex );
		 arm_min_q15 ( adc, header.N, &header.minValue,&header.minIndex );
		 arm_rms_q15 ( adc, header.N, &header.rms						);
//		 trigger(2);
		 header.id++;
		 uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(header ));
		 adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
		 sample = 0;
	  }
	  gpioToggle ( LED1 );											 // este led blinkea a fs/2
	  while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/header.fs) // el clk de la CIAA es 204000000
		 ;
   }
}
