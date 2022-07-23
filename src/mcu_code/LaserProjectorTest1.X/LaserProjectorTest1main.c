
// PIC32MZ0512EFE064 Configuration Bit Settings

// 'C' source line config statements

// DEVCFG3
// USERID = No Setting
#pragma config FMIIEN = OFF             // Ethernet RMII/MII Enable (RMII Enabled)
#pragma config FETHIO = OFF             // Ethernet I/O Pin Select (Alternate Ethernet I/O)
#pragma config PGL1WAY = OFF            // Permission Group Lock One Way Configuration (Allow multiple reconfigurations)
#pragma config PMDL1WAY = ON            // Peripheral Module Disable Configuration (Allow only one reconfiguration)
#pragma config IOL1WAY = ON             // Peripheral Pin Select Configuration (Allow only one reconfiguration)
#pragma config FUSBIDIO = OFF           // USB USBID Selection (Controlled by Port Function)

// DEVCFG2
#pragma config FPLLIDIV = DIV_1         // System PLL Input Divider (1x Divider)
#pragma config FPLLRNG = RANGE_34_68_MHZ// System PLL Input Range (34-68 MHz Input)
#pragma config FPLLICLK = PLL_FRC       // System PLL Input Clock Selection (FRC is input to the System PLL)
#pragma config FPLLMULT = MUL_50        // System PLL Multiplier (PLL Multiply by 50)
#pragma config FPLLODIV = DIV_2         // System PLL Output Clock Divider (2x Divider)
#pragma config UPLLFSEL = FREQ_24MHZ    // USB PLL Input Frequency Selection (USB PLL input is 24 MHz)

// DEVCFG1
#pragma config FNOSC = SPLL             // Oscillator Selection Bits (System PLL)
#pragma config DMTINTV = WIN_127_128    // DMT Count Window Interval (Window/Interval value is 127/128 counter value)
#pragma config FSOSCEN = OFF            // Secondary Oscillator Enable (Disable SOSC)
#pragma config IESO = ON                // Internal/External Switch Over (Enabled)
#pragma config POSCMOD = OFF            // Primary Oscillator Configuration (Primary osc disabled)
#pragma config OSCIOFNC = OFF           // CLKO Output Signal Active on the OSCO Pin (Disabled)
#pragma config FCKSM = CSECME           // Clock Switching and Monitor Selection (Clock Switch Enabled, FSCM Enabled)
#pragma config WDTPS = PS1048576        // Watchdog Timer Postscaler (1:1048576)
#pragma config WDTSPGM = STOP           // Watchdog Timer Stop During Flash Programming (WDT stops during Flash programming)
#pragma config WINDIS = NORMAL          // Watchdog Timer Window Mode (Watchdog Timer is in non-Window mode)
#pragma config FWDTEN = OFF             // Watchdog Timer Enable (WDT Disabled)
#pragma config FWDTWINSZ = WINSZ_25     // Watchdog Timer Window Size (Window size is 25%)
#pragma config DMTCNT = DMT31           // Deadman Timer Count Selection (2^31 (2147483648))
#pragma config FDMTEN = OFF             // Deadman Timer Enable (Deadman Timer is disabled)

// DEVCFG0
#pragma config DEBUG = OFF              // Background Debugger Enable (Debugger is disabled)
#pragma config JTAGEN = ON              // JTAG Enable (JTAG Port Enabled)
#pragma config ICESEL = ICS_PGx1        // ICE/ICD Comm Channel Select (Communicate on PGEC1/PGED1)
#pragma config TRCEN = ON               // Trace Enable (Trace features in the CPU are enabled)
#pragma config BOOTISA = MIPS32         // Boot ISA Selection (Boot code and Exception code is MIPS32)
#pragma config FECCCON = OFF_UNLOCKED   // Dynamic Flash ECC Configuration (ECC and Dynamic ECC are disabled (ECCCON bits are writable))
#pragma config FSLEEP = OFF             // Flash Sleep Mode (Flash is powered down when the device is in Sleep mode)
#pragma config DBGPER = PG_ALL          // Debug Mode CPU Access Permission (Allow CPU access to all permission regions)
#pragma config SMCLR = MCLR_NORM        // Soft Master Clear Enable bit (MCLR pin generates a normal system Reset)
#pragma config SOSCGAIN = GAIN_2X       // Secondary Oscillator Gain Control bits (2x gain setting)
#pragma config SOSCBOOST = ON           // Secondary Oscillator Boost Kick Start Enable bit (Boost the kick start of the oscillator)
#pragma config POSCGAIN = GAIN_2X       // Primary Oscillator Gain Control bits (2x gain setting)
#pragma config POSCBOOST = ON           // Primary Oscillator Boost Kick Start Enable bit (Boost the kick start of the oscillator)
#pragma config EJTAGBEN = NORMAL        // EJTAG Boot (Normal EJTAG functionality)

// DEVCP0
#pragma config CP = OFF                 // Code Protect (Protection Disabled)

// SEQ3

// DEVADC0

// DEVADC1

// DEVADC2

// DEVADC3

// DEVADC4

// DEVADC7

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

#include <xc.h>




void spiInit(){
    /*set up the spi module let's start with a 10 MBps speed, 16 bit spi*/
    
    RPD2R = 0b0101;//setup SDO1 pin
    //setup peripheral clock speed
    //Setup SPI control register
    //enable SPI module
    
    int rData;
    IEC0CLR=0x03800000; 
    // disable all interruptsSPI1CON = 0;
    // Stops and resets the SPI1. 
    rData=SPI1BUF; 
    SPI1BRG=0xFF; //divide the clock speed by 2
    // use FPB/4 clock frequency
    SPI1STATCLR=0x40; 
    // clear the Overflow
    SPI1CONbits.CKE = 1;
    SPI1CONbits.MODE16 = 1;
    SPI1CONbits.MSTEN = 1;
    SPI1CONbits.ON = 1;
    // SPI ON, 8 bits transfer, SMP=1, Master mode// from now on, the device is ready to transmit and receive data
   //SPI1BUF= 'A';           // transmit an A character
    //pull chip select lines high
    LATDbits.LATD4 = 1;
    LATDbits.LATD5 = 1;
    LATDbits.LATD9 = 1;
}

void spiSendWord(unsigned int data){
    
    SPI1BUF = data; //send data to the buffer
}

void setDAC(unsigned int data){
    LATDbits.LATD3 = 1;//disable latch (pull high)
    LATDbits.LATD4 = 0;//pull chip select low (we'll first only care about the first dac)
    unsigned int cmd = 0b0011;//first we'll only focus on channel A.
    spiSendWord((cmd << 12) | data); //combine the command and data bytes, and send it via the spi port
    int j = 0;
    for(j = 0;  j < 1500; j++){
        Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
        }
    LATDbits.LATD4 = 1; //release the DAC from the SPI bus
    LATDbits.LATD3 = 0; //latch the DACs
     j = 0;
    for(j = 0;  j < 100; j++){
        Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
        }
    LATDbits.LATD3 = 1;
    
}

void init(){
    /*Alright, here's what we got:
     -RD1 is set to SCK1
     -RD2 is set to SDO1
     -RD3-RD6 are digital outputs*/
    
    PB1DIVbits.PBDIV = 5; //divide clock source by 10
    //hmm//PB1DIVbits.ON = 1;
    TRISDbits.TRISD3 = 0;
    TRISDbits.TRISD4 = 0;
    TRISDbits.TRISD5 = 0;
    TRISDbits.TRISD9 = 0;
    spiInit();
    
    setDAC(2000);
}

int main(){
    
    init(); //initialize everything.
    
    while(1){
       /* setDAC(4095);
        int j = 0;
        for(j = 0;  j < 10000; j++){
        Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
        }*/
        
        //test our ability to make a triangle wave
        
        int voltage = 0;
        for(voltage = 0; voltage < 4096; voltage++){
            setDAC(voltage);
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
        }
        for(voltage = 4095; voltage >= 0; voltage--){
            setDAC(voltage);
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
            Nop();
        }
    }
    
    return 0;
}