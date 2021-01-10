# GarminPuzzle2021 - Technical challenge for Garmin Junior Software Role

## Brief
I've been given three sound files. The first is a recording of a transmission signal from a (sonar?) tracking system and the second and third are the return signal from a javelin and from a shot-put. The task is to firstly try determine the speed of the object measured and then to determine how far off to the side of the object the tracker was.

## Assumptions

- Assume that the transmitter/receive system is stationary.
- Assume that the velocities of the objects involved in this problem are less than the speed of light i.e) they share a common frame of reference... sorry Einstein, next time! 

## Approach

The first thing that came to mind was a speed gun, a device which uses EM waves and the doppler effect to measure the velocity of the object. I have a gut feel that this problem involves the doppler effect and that it would involve extracting the frequency information of the signals as there isn't much else to go on. I thought of the radar equation but I'm not sure how that transfers to audio + i'd need things like radar cross section and gain etc.

I first wrote a simple python script (see challenge.py) to read the .wav data and to plot the FFT of the data to see the frequency information. 

The FFT of the transmit signal shows a clear spike in power at around 10kHz. The receiving signals are noisy - so I do some filtering on those just by applying a low pass filter. Plotting the cleaner data I can see clear spikes in power at a little more than 8kHz for the Javelin and a little more than 9kHz for the shotput. This makes sense to me as the drop in frequency (red-shift) would indicate that the target is moving **away** from the observer.

![All Signals](/images/All_unfiltered.png)

![Filtered Received Signals](/images/Received_filtered.png)

The frequencies of each signal can be obtained programatically. I selected a cut-off for the lowpass filter of around 30% of the max frequency (where 50% is the nyquist frequency) because if I went any lower the peak value for the shotput seemed off in comparison to the graph, then I use a numpy function to 'peak detect' and get back the frequency of the peaks. I get those as:

- Transmit: 9999.80Hz
- Receive Javelin: 8265.83Hz
- Receive Shotput: 9241.82Hz 

With this information I can use the doppler formula found here:

![\Large v = \frac{\Delta f}{f}\frac{c}{2}](https://latex.codecogs.com/svg.latex?v&space;=&space;\frac{\Delta&space;f}{f}\frac{c}{2}) 

## Results   

I calculate around 29.738m/s for the Javelin and 12.9m/s for the shotput. 

A quick google search for average [Javelin throwspeed!](https://theconversation.com/science-of-the-spear-biomechanics-of-a-javelin-throw-29782#:~:text=The%20average%20maximum%20run%20up,of%20the%20final%20two%20steps.)

>The average maximum run up speed of an elite thrower ranges from 5-6m/s (20km/h), but elite throwers release the javelin at 28-30m/s

[For shotput!](https://www.quinticsports.com/performance-analysis-shot-put/#:~:text=The%20average%20shot%20velocity%20at,ms%2D1%20for%20athlete%20B.)

>The average shot velocity at release was 10.24ms-1 for athlete A and 9.40ms-1 for athlete B.

So the numbers calculated at least seem plausible. 
