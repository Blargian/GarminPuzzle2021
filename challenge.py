# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 05:57:41 2021
Garmin Challenge 2021
@author: shaun
"""

from scipy.io.wavfile import read
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy import signal

#Constants

scriptDir = os.path.join(os.path.dirname(__file__),'sound-files')
#Takes the audio file and returns the time series data
def import_audio(fileName):

    sampleRate, data = read(fileName)
    duration=len(data)/sampleRate
    time = np.arange(0,duration,1/sampleRate)
    
    return time, data

#Used to get the timeStep between samples
def get_time_step(fileName):
    sampleRate, data = read(os.path.join(scriptDir,fileName))
    return 1/sampleRate

def simple_peak_detect(x,y):
    index = np.argmax(y,axis=0)
    return x[index]

def calc_speed(fSource,fTarget):
    c = 343 #343m/s
    delta_f = np.abs(fSource-fTarget)
    return (delta_f/fSource)*(343/2)
    


T = get_time_step('Transmit_1.wav')
timeTransmit, dataTransmit = import_audio(os.path.join(scriptDir,'Transmit_1.wav'))
N=len(dataTransmit)
timeJavelin, dataJavelin = import_audio(os.path.join(scriptDir,'Javelin_receive_1.wav'))
timeShotput, dataShotput = import_audio(os.path.join(scriptDir,'Shotput_receive_1.wav'))

#Taking the FFT of the time series data

### FFT plot of all three ###
yf = rfft(dataTransmit)
xf = rfftfreq(N, T)

plt.figure()

plt.plot(xf[4000:6000], np.abs(yf)[4000:6000],label='Transmitted Signal')

plt.title('Power vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')

yf2 = rfft(dataJavelin)
xf2 = rfftfreq(N, T)
plt.plot(xf2[4000:6000], np.abs(yf2)[4000:6000],label='Received (Javelin)')

yf3 = rfft(dataShotput)
xf3 = rfftfreq(N, T)
plt.plot(xf2[4000:6000], np.abs(yf2)[4000:6000],label='Received (Shotput)')

plt.legend()

### FFT plot of return signals###

b, a = signal.butter(2, 0.3)

plt.figure()

plt.title('Power vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')

yf2 = rfft(dataJavelin)
yf2clean = signal.filtfilt(b, a, yf2, padlen=150)
xf2 = rfftfreq(N, T)
plt.plot(xf2[4000:5000], np.abs(yf2clean)[4000:5000],label='Received (Javelin)')

yf3 = rfft(dataShotput)
yf3clean = signal.filtfilt(b, a, yf3, padlen=150)
xf3 = rfftfreq(N, T)
plt.plot(xf3[4000:5000], np.abs(yf3clean)[4000:5000],label='Received (Shotput)')
plt.legend()

fTransmit = simple_peak_detect(xf[4000:],yf[4000:])
fJavelin = simple_peak_detect(xf2[4000:5000],yf2clean[4000:5000])
fShotput = simple_peak_detect(xf3[4000:5000],yf3clean[4000:5000])

print(calc_speed(fTransmit,fJavelin))
print(calc_speed(fTransmit,fShotput))





