#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"

#define MAX_FFT_LENGTH 2048         // maxima longitud para la fft y chunk de samples
#define BITS 10                     // cantidad de bits usado para cuantizar

int16_t fftLength = 32;             // longitud de la fft y samples variable
int16_t adc [ MAX_FFT_LENGTH ];     // guarda los samples
q15_t fftIn [ MAX_FFT_LENGTH ];     // guarda copia de samples en Q15 como in para la fft.La fft corrompe los datos de la entrada!
q15_t fftOut[ MAX_FFT_LENGTH*2 ];   // salida de la fft
q15_t fftMag[ MAX_FFT_LENGTH/2+1 ]; // magnitud de la FFT
uint32_t maxIndex = 0;              // indexador de maxima energia por cada fft
q15_t maxValue    = 0;              // maximo valor de energia del bin por cada fft
arm_rfft_instance_q15 S;
uint16_t sample   = 0;              // contador para samples

int main ( void ) {
   boardConfig        (                          );
   uartConfig         ( UART_USB, 460800         );
   adcConfig          ( ADC_ENABLE               );
   cyclesCounterInit  ( EDU_CIAA_NXP_CLOCK_SPEED );
   while(1) {
      cyclesCounterReset();                                                          // inicializa el conteo de ciclos de reloj
      uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample]    ,sizeof(adc[0]) );   // envia el sample ANTERIOR
      uartWriteByteArray ( UART_USB ,(uint8_t* )&fftOut[sample] ,sizeof(fftOut[0])); // envia la fft del sample ANTERIO
      //TODO hay que mandar fftLength/2 "+1" y solo estoy mandando fftLength/2. revisar
      adc[sample]   =(((int16_t )adcRead(CH1)-512)>>(10-BITS))<<(6+10-BITS);         // PISA el sample que se acaba de mandar con una nueva muestra
      fftIn[sample] = adc[sample];                                                   // copia del adc porque la fft corrompe el arreglo de entrada
      if ( ++sample==fftLength ) {                                                   // si es el ultimo
         sample = 0;                                                                 // arranca de nuevo
         uartWriteByteArray ( UART_USB ,(uint8_t* )&maxValue ,2);
         uartWriteByteArray ( UART_USB ,(uint8_t* )&maxIndex ,2);
         uartWriteByteArray ( UART_USB ,"header" ,6 );                               // manda el header que casualmente se llama "header" con lo que arranca una nueva trama
         uartWriteByteArray ( UART_USB ,(uint8_t* )&fftLength ,sizeof(fftLength));   // manda el largo de la fft que es variable
         arm_rfft_init_q15 ( &S ,fftLength ,0 ,1 );                                  // inicializa una estructira que usa la funcion fft para procesar los datos. Notar el /2 para el largo
         arm_rfft_q15      ( &S ,fftIn     ,fftOut    );                             // por fin.. ejecuta la rfft REAL fft
         arm_cmplx_mag_squared_q15 ( fftOut ,fftMag ,fftLength/2+1 );
         arm_max_q15 ( fftMag ,fftLength/2+1 ,&maxValue ,&maxIndex );
         gpioToggle( LEDR);
         if ( gpioRead(TEC1 )==0) {
            gpioToggle(LEDB);
            if((fftLength<<=1)>MAX_FFT_LENGTH)
               fftLength=32;
            while(gpioRead(TEC1)==0)
               ;
         }
      }
      while(cyclesCounterRead()< 20400) //clk de 204000000 => 10k samples x seg.
         ;
   }
}

//guitard air chord freq
//1ra (E): 329,63 Hz
//2da (B): 246,94 Hz
//3ra (G): 196,00 Hz
//4ta (D): 146,83 Hz
//5ta (A): 110,00 Hz
//6ta (E): 82,41 Hz
