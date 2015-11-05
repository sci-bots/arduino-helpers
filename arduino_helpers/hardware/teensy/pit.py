# -*- coding: utf-8 -*-
import io
import pandas as pd


# Description of Periodic Interrupt Timer (PIT) (37/901)
REGISTERS_DESCRIPTIONS_TSV = '''
full_name	short_description	description	page
MCR.MDIS	Module Disable	Disables the module clock. This field must be enabled before any other setup is done. 0: Clock for PIT timers is enabled. 1: Clock for PIT timers is disabled.	37.3.1/903
MCR.FRZ	Freeze	Allows the timers to be stopped when the device enters the Debug mode. 0: Timers continue to run in Debug mode. 1: Timers are stopped in Debug mode.	37.3.1/903
'''.strip()

REGISTERS_DESCRIPTIONS = pd.read_csv(io.BytesIO(REGISTERS_DESCRIPTIONS_TSV),
                                     sep='\t').set_index('full_name')
REGISTERS_DESCRIPTIONS.loc[REGISTERS_DESCRIPTIONS.description.isnull(),
                           'description'] = ''


# Description of Periodic Interrupt Timer Config registers (37.3.2/904 - 37.3.5/906)
TIMER_CONFIG_DESCRIPTIONS_TSV = '''
full_name	short_description	description	page
LDVAL	Timer Start Value	Sets the timer start value. The timer will count down until it reaches 0, then it will generate an interrupt and load this register value again. Writing a new value to this register will not restart the timer; instead the value will be loaded after the timer expires. To abort the current cycle and start a timer period with the new value, the timer must be disabled and enabled again.	37.3.2/904
CVAL	Current Timer Value	Represents the current timer value, if the timer is enabled. NOTE: 1) If the timer is disabled, do not use this field as its value is unreliable. 2) The timer uses a downcounter. The timer values are frozen in Debug mode if MCR[FRZ] is set.	37.3.3/905
TCTRL.CHN	Chain Mode	When activated, Timer n-1 needs to expire before timer n can decrement by 1. Timer 0 can not be chained. 0: Timer is not chained. 1: Timer is chained to previous timer. For example, for Channel 2, if this field is set, Timer 2 is chained to Timer 1.	37.3.4/905
TCTRL.TIE	Timer Interrupt Enable	When an interrupt is pending, or, TFLGn[TIF] is set, enabling the interrupt will immediately cause an interrupt event. To avoid this, the associated TFLGn[TIF] must be cleared first. 0: Interrupt requests from Timer n are disabled. 1: Interrupt will be requested whenever TIF is set.	37.3.4/905
TCTRL.TEN	Timer Enable	Enables or disables the timer. 0: Timer n is disabled. 1: Timer n is enabled.	37.3.4/905
TFLG.TIF	Timer Interrupt Flag	Sets to 1 at the end of the timer period. Writing 1 to this flag clears it. Writing 0 has no effect. If enabled, or when TCTRLn[TIE] = 1, TIF causes an interrupt request. 0: Timeout has not yet occurred. 1: Timeout has occurred.	37.3.5/906
'''.strip()

TIMER_CONFIG_DESCRIPTIONS = \
    pd.read_csv(io.BytesIO(TIMER_CONFIG_DESCRIPTIONS_TSV),
                sep='\t').set_index('full_name')
TIMER_CONFIG_DESCRIPTIONS.loc[TIMER_CONFIG_DESCRIPTIONS.description.isnull(),
                              'description'] = ''
