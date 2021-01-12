# GarminPuzzle2021 - Technical challenge for Garmin Junior Software Role

## Brief
I've been given three sound files. The first is a recording of a transmission signal from a (an acoustic radar?) tracking system and the second and third are the return signals from a thrown javelin and from a shot-put. The task is to firstly try determine the speed of the objects and then to determine how far off to the side of the object the tracker was.

## Assumptions

- Assume that the transmitter/receive system is stationary.
- Assume that the velocities of the objects involved in this problem are less than the speed of light i.e) they share a common frame of reference... sorry Albert, maybe next time! 
- For a start assume that the transmitter/receive system is parallel to the sportsman or at least very close. 

## Approach

The first thing that came to mind after reading the challenge was a speed gun, a device which uses EM waves and the doppler effect to measure the velocity of the object. I have a gut feel that this problem involves the doppler effect in some way and that it would involve extracting the frequency information of the signals as there isn't much else to go on. I initially thought of the radar equation but I'm not sure how that transfers to audio, plus i'd need things like radar cross section and gain etc.

I first wrote a simple python script (see challenge.py) to read the .wav data and to plot the FFT of the data to see the frequency information. 

The FFT of the transmit signal shows a clear spike in power at around 10kHz. The receiving signals are noisy, as is to be expected - so I do some crude filtering on those signals first, just by visually inspecting where the peaks are and then zeroing below a threshhold value. Plotting the cleaner data I can see clear spikes in power at a little more than 8kHz for the Javelin and a little more than 9kHz for the shotput. This makes sense to me as the drop in frequency (red-shift) would indicate that the target is moving **away** from the observer. Shown below in the first image is a plot of the frequency information for all three and then in image two, the filtered data for the received signals. 

![All Signals](/images/All_unfiltered.png)

![Filtered Received Signals](/images/Received_filtered.png)

The frequencies of each signal can be obtained programatically. I use a numpy function to peak detect and get back the frequency of the peaks. I get those as:

- Transmit: 9999.80Hz
- Receive Javelin: 8265.83Hz
- Receive Shotput: 9241.82Hz 

With this information I can use this doppler formula:

![\Large v = \frac{\Delta f}{f}\frac{c}{2}](https://latex.codecogs.com/svg.latex?v&space;=&space;\frac{\Delta&space;f}{f}\frac{c}{2}) 

## Results   

I calculate a release speed of around **32.04m/s** for the Javelin and **13.51m/s** for the shotput. 

A quick google search for average [Javelin throwspeed](https://theconversation.com/science-of-the-spear-biomechanics-of-a-javelin-throw-29782#:~:text=The%20average%20maximum%20run%20up,of%20the%20final%20two%20steps.)

>The average maximum run up speed of an elite thrower ranges from 5-6m/s (20km/h), but elite throwers release the javelin at 28-30m/s

[For shotput](https://www.quinticsports.com/performance-analysis-shot-put/#:~:text=The%20average%20shot%20velocity%20at,ms%2D1%20for%20athlete%20B.)

>The average shot velocity at release was 10.24ms-1 for athlete A and 9.40ms-1 for athlete B.

So the numbers calculated at least seem plausible, if not a little high. However this is to be expected because the assumption was made that the tracker was inline with the thrower, where in reality it will be off to the side, so the actual speed here will have an error associated with it. 

## BONUS (An attempt)

After a bit more googling I've come across something called "Doppler Angle", mostly in the context of ultrasound. The basic idea is that if you're measuring a flow of blood, you will be measuring at an angle which introduces error unless the beam is transmitted parallel to the flow of blood (not possible)I.e when measuring you want to be as close to an angle of 0 degrees to the motion of the tracked object as you can. Same thing applies here I think. This formula is given for the doppler angle:

![\Large \Delta f = 2f_t\frac{V}{c}\cos\Theta](https://latex.codecogs.com/svg.latex?\Delta&space;f&space;=&space;2f_t\frac{V}{c}\cos\Theta) 

Previously I made the assumption that the tracker was parallel to the thrower - in practise that is not correct which means that there is an error on the speeds above.

### Ideas

Have been thinking of a way that I could solve for the Cosine angle geometrically but I think it might be more complex than that. From the small amount of knowledge I have on radar and what I've read, normally you apply a matched filter to do range estimation. The phase information is very important for calculating how far the target is away. 

Found this website on [Radar](https://www.radartutorial.eu/11.coherent/co06.en.html) 

I'm a little rusty on my second year linear systems and signals knowledge but I do believe that I can obtain the phase difference between two signals by finding the maximum of the correlation between them (as seems to be confirmed [here](https://stackoverflow.com/questions/6157791/find-phase-difference-between-two-inharmonic-waves). 

So I use cross-correlation to get the lag (in samples) between the transmit and receive signals. I then multiply that by the sample interval in seconds and convert that into a radian value.  

- Phase shift estimate between Transmitted and Javelin Received: 0.27 radians
- Phase shift estimate between Transmitted and Shotput Received: 0.50 radians

I then calculated the distance r to the target using the above values and the formula below:

![\Large \phi = -\frac{2r \times 2\pi}{\lambda}](https://latex.codecogs.com/svg.latex?\phi&space;=&space;-\frac{2r&space;\times&space;2\pi}{\lambda}) 

From that you can work out how far to the side the sensor is for a given angle of inclination (I think you would choose this to be low to reduce the error) using simple trigonometry:

![Geometry](/images/sideDistance.jpg) 

For an angle of 20 degrees for instance the sensor would be 0.045m from the thrower and for the shotput 0.086m. 










	





 
 




