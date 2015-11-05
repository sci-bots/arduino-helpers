# -*- coding: utf-8 -*-
import io
import pandas as pd


# Description of System Integration Module:
#   System Clock Gating Control Register 6 (12.2.13/256)
SCGC6_DESCRIPTIONS_TSV = '''
full_name	short_description	description	page
RTC	RTC Access Control	This bit controls software access and interrupts to the RTC module. 0: Access and interrupts disabled, 1: Access and interrupts enabled	12.2.13/256
ADC0	ADC0 Clock Gate Control	This bit controls the clock gate to the ADC0 module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
FTM1	FTM1 Clock Gate Control	This bit controls the clock gate to the FTM1 module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
FTM0	FTM0 Clock Gate Control	This bit controls the clock gate to the FTM0 module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
PIT	PIT Clock Gate Control	This bit controls the clock gate to the PIT module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
PDB	PDB Clock Gate Control	This bit controls the clock gate to the PDB module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
USBDCD	USB DCD Clock Gate Control	This bit controls the clock gate to the USB DCD module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
CRC	CRC Clock Gate Control	This bit controls the clock gate to the CRC module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
I2S	I2S Clock Gate Control	This bit controls the clock gate to the I 2 S module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
SPI1	SPI1 Clock Gate Control	This bit controls the clock gate to the SPI1 module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
SPI0	SPI0 Clock Gate Control	This bit controls the clock gate to the SPI0 module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
FLEXCAN0	FlexCAN0 Clock Gate Control	This bit controls the clock gate to the FlexCAN0 module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
DMAMUX	DMA Mux Clock Gate Control	This bit controls the clock gate to the DMA Mux module. 0: Clock disabled, 1: Clock enabled	12.2.13/256
FTFL	Flash Memory Clock Gate Control	This bit controls the clock gate to the flash memory. Flash reads are still supported while the flash memory is clock gated, but entry into low power modes is blocked. 0: Clock disabled, 1: Clock enabled	12.2.13/256
'''.strip()

SCGC6_DESCRIPTIONS = pd.read_csv(io.BytesIO(SCGC6_DESCRIPTIONS_TSV),
                                 sep='\t').set_index('full_name')
SCGC6_DESCRIPTIONS.loc[SCGC6_DESCRIPTIONS.description.isnull(),
                       'description'] = ''


# Description of System Integration Module:
#   System Clock Gating Control Register 7 (12.2.14/259)
SCGC7_DESCRIPTIONS_TSV = '''
full_name	short_description	description	page
DMA	DMA Clock Gate Control	This bit controls the clock gate to the DMA module. 0: Clock disabled, 1: Clock enabled	12.2.14/259
'''.strip()

SCGC7_DESCRIPTIONS = pd.read_csv(io.BytesIO(SCGC7_DESCRIPTIONS_TSV),
                                 sep='\t').set_index('full_name')
SCGC7_DESCRIPTIONS.loc[SCGC7_DESCRIPTIONS.description.isnull(),
                       'description'] = ''
