import numpy as np
import pandas as pd


PDB_SC_CONT = 0x00000002  # Continuous Mode Enable
PDB_SC_DMAEN = 0x00008000  # DMA Enable
PDB_SC_LDOK = 0x00000001  # Load OK
PDB_SC_PDBEIE = 0x00020000  # Sequence Error Interrupt Enable
PDB_SC_PDBEN = 0x00000080  # PDB Enable
PDB_SC_PDBIE = 0x00000020  # PDB Interrupt Enable.
PDB_SC_PDBIF = 0x00000040  # PDB Interrupt Flag
PDB_SC_SWTRIG = 0x00010000  # Software Trigger
PDB0_IDLY = 0x4003600C  # Interrupt Delay Register
PDB0_MOD = 0x40036004  # Modulus Register
PDB0_SC = 0x40036000  # Status and Control Register


def PDB_SC_TRGSEL(n): return (((n) & 15) << 8)  # Trigger Input Source Select
def PDB_SC_PRESCALER(n): return (((n) & 7) << 12)  # Prescaler Divider Select
def PDB_SC_MULT(n): return (((n) & 3) << 2)  # Multiplication Factor
def PDB_SC_LDMOD(n): return (((n) & 3) << 18)  # Load Mode Select


def get_pdb_divide_params(frequency, F_BUS=int(48e6)):
    mult_factor = np.array([1, 10, 20, 40])
    prescaler = np.arange(8)

    clock_divide = (pd.DataFrame([[i, m, p, m * (1 << p)]
                                  for i, m in enumerate(mult_factor)
                                  for p in prescaler],
                                 columns=['mult_', 'mult_factor',
                                          'prescaler', 'combined'])
                    .drop_duplicates(subset=['combined'])
                    .sort_values('combined', ascending=True))
    clock_divide['clock_mod'] = (F_BUS / frequency
                                 / clock_divide.combined).astype(int)
    return clock_divide.loc[clock_divide.clock_mod <= 0xffff]
