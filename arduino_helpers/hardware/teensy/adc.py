import io
import pandas as pd


# Description of ADC registers
ADC_DESCRIPTIONS_TSV = '''
full_name	short_description	description
CLMD	ADC Minus-Side General Calibration Value Register
CLPS	ADC Plus-Side General Calibration Value Register
CLMS	ADC Minus-Side General Calibration Value Register
CLPD	ADC Plus-Side General Calibration Value Register
PG	ADC Plus-Side Gain Register
RB	ADC Data Result Register
RA	ADC Data Result Register
OFS	ADC Offset Correction Register
MG	ADC Minus-Side Gain Register
CLP1	ADC Plus-Side General Calibration Value Register
CLP0	ADC Plus-Side General Calibration Value Register
CLP3	ADC Plus-Side General Calibration Value Register
CLP2	ADC Plus-Side General Calibration Value Register
CV2	Compare Value Register
CLP4	ADC Plus-Side General Calibration Value Register
CV1	Compare Value Register
CLM2	ADC Minus-Side General Calibration Value Register
CLM3	ADC Minus-Side General Calibration Value Register
CLM0	ADC Minus-Side General Calibration Value Register
CLM1	ADC Minus-Side General Calibration Value Register
CLM4	ADC Minus-Side General Calibration Value Register
CFG2.MUXSEL	ADC mux select	 0: ADxxa channels selected, 1: ADxxb channels selected
CFG2.ADLSTS	Long sample time select	 0: 20 extra ADCK cycles (default), 1: 12 extra ADCK cycles, 2: 6 extra ADCK cycles, 3: 2 extra ADCK cycles
CFG2.ADHSC	High-speed configuration
CFG2.ADACKEN	Asynchronous clock output enable
CFG1.ADLSMP	Sample time configuration	 0: Short sample time, 1: Long sample time
CFG1.ADICLK	Input clock select	 0: Bus clock, 1: Bus clock/2, 2: Alternate clock (ALTCLK), 3: Asynchronous clock (ADACK)
CFG1.MODE	Conversion mode selection	 0: 8-bit, 1: 12-bit, 2: 10-bit, 3: 16-bit
CFG1.ADIV	Clock divide select	 0: /1, 1: /2, 2: /4, 3: /8
CFG1.ADLPC	Low-power configuration
SC1A.COCO	Conversion complete flag
SC1A.DIFF	Differential mode enable
SC1A.AIEN	Interrupt enable
SC1A.ADCH	Input channel select
SC1B.COCO	Conversion complete flag
SC1B.DIFF	Differential mode enable
SC1B.AIEN	Interrupt enable
SC1B.ADCH	Input channel select
PGA.PGAEN	PGA enable
PGA.PGALPb	PGA low-power mode control
PGA.PGAG	PGA Gain setting, $PGA~gain = 2^{PGAG}$	 0: 1, 1: 2, 2: 4, 3: 8, 4: 16, 5: 32, 6: 64
SC3.AVGE	Hardware average enable
SC3.ADCO	Continuous conversion enable
SC3.AVGS	Hardware average select	 Samples averaged - 0: 4, 1: 8, 0: 16, 0: 32
SC3.CALF	Calibration failed flag
SC3.CAL	Calibration
SC2.DMAEN	DMA enable	 1: 1 DMA is enabled and will assert the ADC DMA request during an ADC conversion complete event noted when any of the `SC1n[COCO]` flags is asserted.
SC2.REFSEL	Voltage reference selection	 0: Default, 1: Alternate, 2-3: Reserved
SC2.ADACT	Conversion active
SC2.ACFGT	Compare function greater than enable
SC2.ADTRG	Conversion trigger select	 0: Software trigger, 1: Hardware trigger
SC2.ACREN	Compare function range enable
SC2.ACFE	Compare function enable
'''.strip()

ADC_DESCRIPTIONS = pd.read_csv(io.BytesIO(ADC_DESCRIPTIONS_TSV),
                               sep='\t').set_index('full_name')
ADC_DESCRIPTIONS.loc[ADC_DESCRIPTIONS.description.isnull(), 'description'] = ''

# Mask for the channel selection in ADCx_SC1A,
# useful if you want to get the channel number from ADCx_SC1A
ADC_SC1A_CHANNELS = (0x1F)
# 0x1F=31 in the channel2sc1aADCx means the pin doesn't belong to the ADC
# module
ADC_SC1A_PIN_INVALID = (0x1F)
# max number of pins, size of channel2sc1aADCx
ADC_MAX_PIN = (44)
# Muxsel mask, pins in channel2sc1aADCx with bit 7 set use mux A.
ADC_SC1A_PIN_MUX = (0x80)
# Differential pin mask, pins in channel2sc1aADCx with bit 6 set are differential pins.
ADC_SC1A_PIN_DIFF = (0x40)
# PGA mask. The pins can use PGA on that ADC
ADC_SC1A_PIN_PGA = (0x80)


# New version, gives directly the sc1a number. 0x1F=31 deactivates the ADC.
CHANNEL_TO_SC1A_ADC0 = [
    # 0-13, we treat them as A0-A13
    5, 14, 8, 9, 13, 12, 6, 7, 15, 4, 0, 19, 3, 21,
    # 14-23 (A0-A9)
    5, 14, 8, 9, 13, 12, 6, 7, 15, 4,
    # 24-33
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
    ADC_SC1A_PIN_INVALID,
    # 34-37 (A10-A13)
    0 + ADC_SC1A_PIN_DIFF,
    19 + ADC_SC1A_PIN_DIFF,
    3 + ADC_SC1A_PIN_DIFF,
    21 + ADC_SC1A_PIN_DIFF,
    # 38-43: temp. sensor, VREF_OUT, A14, bandgap, VREFH, VREFL. A14 isn't
    # connected to anything in Teensy 3.0.
    26, 22, 23, 27, 29, 30
]

CHANNEL_TO_SC1A_DIFF_ADC0 = [
    # A10-A11 (DAD0, PGA0), A12-A13 (DAD3)
    0 + ADC_SC1A_PIN_PGA, 0 + ADC_SC1A_PIN_PGA, 3, 3
]

#define ADC0_SC1A		(*(volatile uint32_t *)0x4003B000) // ADC status and control registers 1
#define ADC0_SC1B		(*(volatile uint32_t *)0x4003B004) // ADC status and control registers 1

# Map Teensy `Ax` pin number to ADC Status and Control Register channel number.
# Add high-bit flags to signal:
#  - Which mux setting to use.
#  - Whether the channel supports differential mode.
CHANNEL_TO_SC1A_ADC1 = [
    # 0-13, we treat them as A0-A13
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, 8, 9, ADC_SC1A_PIN_INVALID,
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, 3, ADC_SC1A_PIN_INVALID, 0, 19,
    # 14-23 (A0-A9)
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, 8, 9, ADC_SC1A_PIN_INVALID,
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
    # 24,25 are digital only pins
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
    # 26-33 26=5a, 27=5b, 28=4b, 29=6b, 30=7b, ADC_SC1A_PIN_INVALID=4a, 32,33 are digital only
    5 + ADC_SC1A_PIN_MUX, 5, 4, 6, 7, 4 + ADC_SC1A_PIN_MUX,
    ADC_SC1A_PIN_INVALID, ADC_SC1A_PIN_INVALID,
    # 34-37 (A10-A13) A11 isn't connected.
    3 + ADC_SC1A_PIN_DIFF, ADC_SC1A_PIN_INVALID + ADC_SC1A_PIN_DIFF,
    0 + ADC_SC1A_PIN_DIFF, 19 + ADC_SC1A_PIN_DIFF,
    # 38-43: temp. sensor, VREF_OUT, A14 (not connected), bandgap, VREFH, VREFL.
    26, 18, ADC_SC1A_PIN_INVALID, 27, 29, 30
]

CHANNEL_TO_SC1A_DIFF_ADC1 = [
    # A10-A11 (DAD3), A12-A13 (DAD0, PGA1)
    3, 3, 0 + ADC_SC1A_PIN_PGA, 0 + ADC_SC1A_PIN_PGA
]
