"""
Calculate HRV (heart rate variability) from ECG signal data.

Uses biosppy to get the indices of the R peaks in the ECG signal.
https://biosppy.readthedocs.io/en/stable/

HRV is calculated using the Root Mean Square of Successive Differences (RMSSD)
https://www.ahajournals.org/doi/full/10.1161/01.cir.93.5.1043
"""

import sys
import math
import argparse
import pandas as pd
from biosppy.signals import ecg

def calculate_HRV(input_ecg_file, sample_rate):

    """ Function to calculate heart rate variability.
        Inputs: - name of file containing ECG signal data in csv format
                - sample rate in Hz
        Output: HRV in milliseconds
    """

    # Read the appropriate column from the ECG signal data file. 
    # Sometimes, they have 3 columns for the 3 leads. Adjust as needed.
    df = pd.read_csv(input_ecg_file,header=None)
    ecg1 = df[0]

    # set show=True to see the graphs
    out = ecg.ecg(signal=ecg1, sampling_rate=sample_rate,show=False) 

    # Extract the indices of the R peaks
    rpeak_indices = out['rpeaks']
    num_peaks = len(rpeak_indices)

    # Calculate HRV (in ms) using RMSSD
    values = [math.pow((ecg1[rpeak_indices[i+1]] - ecg1[rpeak_indices[i]]),2) for i in range(num_peaks - 1)]
    hrv = math.sqrt(sum(values)/(num_peaks-1))

    return hrv

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", default='ECG.csv', help="name of input csv file containing ECG data")
    parser.add_argument("-s", default=300, help="sample rate (Hz)")
    args = parser.parse_args()

    infile = args.i
    samplerate = args.s

    hrv = calculate_HRV(infile,samplerate)
    print('hrv = ',hrv)

