# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 05:57:41 2021
Garmin Challenge 2021
@author: Shaun Struwig
"""

from scipy.io.wavfile import read
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, irfft
from scipy import signal
from scipy.signal import correlate

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

#Crude filtering method, makes values below a certain threshhold 0
def filter_data(threshHold,fftArray,filteredArray):
    for i in range(0,len(fftArray)):
        if np.abs(fftArray[i]) < threshHold:
            filteredArray.append(0)
        else:
            filteredArray.append(fftArray[i])

#Detects the max frequency
def simple_peak_detect(x,y):
    index = np.argmax(y,axis=0)
    return x[index]

#Calculates the speed using the doppler formula
def calc_speed(fSource,fTarget):
    c = 343 #343m/s
    delta_f = np.abs(fSource-fTarget)
    return (delta_f/fSource)*(c/2)

#Estimate the angle  
def estimate_angle(fSource,fTarget,vTarget):
    c = 343 #343m/s
    delta_f = np.abs(fSource-fTarget)
    theta = delta_f/(2*fSource*(vTarget/c))
    print(theta)
    

### Load in the data from .wav files ###
    
T = get_time_step('Transmit_1.wav')
timeTransmit, dataTransmit = import_audio(os.path.join(scriptDir,'Transmit_1.wav'))
N=len(dataTransmit)
timeJavelin, dataJavelin = import_audio(os.path.join(scriptDir,'Javelin_receive_1.wav'))
timeShotput, dataShotput = import_audio(os.path.join(scriptDir,'Shotput_receive_1.wav'))

### Obtain FFTs of all three signals ###

yf = rfft(dataTransmit)
xf = rfftfreq(N, T)

yf2 = rfft(dataJavelin)
xf2 = rfftfreq(N, T)

yf3 = rfft(dataShotput)
xf3 = rfftfreq(N, T)

### Plot the FFT of all trhee signals (no filtering) ### 

plt.figure()
plt.plot(xf[4000:6000], np.abs(yf)[4000:6000],label='Transmitted Signal')
plt.plot(xf2[4000:6000], np.abs(yf2)[4000:6000],label='Received (Javelin)')
plt.plot(xf2[4000:6000], np.abs(yf2)[4000:6000],label='Received (Shotput)')
plt.title('Power vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.legend()

### FFT plot of return signals ###

#Defines
yf2clean = []
yf3clean = []

### Filter the two received signals ###

xf2 = rfftfreq(N, T)
yf2 = rfft(dataJavelin)
filter_data(3.5*10**7,np.abs(yf2),yf2clean)
dataJavelinClean = irfft(yf2clean) #back to time domain


xf3 = rfftfreq(N, T)
yf3 = rfft(dataShotput)
filter_data(2.0*10**7,np.abs(yf3),yf3clean)
dataShotputClean = irfft(yf3clean) #back to time domain

### Plot the two received signals after filtering ###

plt.figure()
plt.title('Power vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.plot(xf2, np.abs(yf2clean),label='Received (Javelin)')
plt.plot(xf3[100:], np.abs(yf3clean)[100:],label='Received (Shotput)') #From 100 onwards to get rid of the DC component value
plt.legend()
plt.xlim(8000,9500)


### Obtain the frequencies of the signals ###

fTransmit = simple_peak_detect(xf,yf)
fJavelin = simple_peak_detect(xf2,yf2clean)
fShotput = simple_peak_detect(xf3[100:],yf3clean[100:])

print('Frequency of Transmited Signal: {}KHz '.format(fTransmit/1000))
print('Frequency of Received Signal (Javelin): {}KHz '.format(fJavelin/1000))
print('Frequency of Received Signal (Shotput): {}KHz '.format(fShotput/1000))

### Calculate The speeds ###

vJavelin = calc_speed(fTransmit,fJavelin)
vShotput = calc_speed(fTransmit,fShotput)
print('Speed for Javelin: {}m/s '.format(vJavelin))
print('Speed for Shotput: {}m/s '.format(vShotput))

### BONUS ###

correlation = correlate(dataTransmit,dataJavelinClean)
maxValue = np.argmax(correlation,axis=0)
print('Phase shift estimate between Transmitted and Javelin Received: {}s'.format(maxValue*T))

correlation2 = correlate(dataTransmit,dataShotputClean)
maxValue2 = np.argmax(correlation2,axis=0)
print('Phase shift estimate between Transmitted and Shotput: {}s'.format(maxValue2*T))







