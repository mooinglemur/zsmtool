import librosa
import numpy as np
import math
import sys
from scipy.signal import find_peaks

def process_amplitude(x):
    n = 28 * math.log(x) / math.log(6)
    if n > 63:
        return 63
    if n < 0:
        return 0
    return round(n)
    

# Load the audio file
audio_file = sys.argv[1]
y, sr = librosa.load(audio_file, sr=None)

# Parameters
frame_length = int(sr * 1/3)  # 1/60th second frame length (adjust as needed)
hop_length = int(frame_length / (60/3))

# Initialize lists to store frame frequencies and amplitudes
frame_frequencies = []
frame_amplitudes = []

# Iterate over frames
for i in range(0, len(y) - frame_length, hop_length):
    frame = y[i:i + frame_length]
    
    # Apply windowing function
    frame *= np.hamming(len(frame))
    
    # Compute STFT
    D = np.abs(librosa.stft(frame))
    
    # Find the dominant frequencies (adjust parameters as needed)
    freq_indices = np.where(D > 0.1 * np.max(D))  # Adjust the threshold as needed
    frequencies = librosa.fft_frequencies(sr=sr)[freq_indices[0]]
    amplitudes = D[freq_indices]

    # Filter out frequencies < 20 and > 20000
    valid_indices = np.where((frequencies >= 20) & (frequencies <= 20000))
    frequencies = frequencies[valid_indices]
    amplitudes = amplitudes[valid_indices]

    # Find peaks in the frequency spectrum
    peaks, _ = find_peaks(amplitudes)

    # Sort peaks by amplitude and take the top N peaks
    peak_indices = np.argsort(amplitudes[peaks])[::-1][:16]
    top_frequencies = frequencies[peaks[peak_indices]]
    top_amplitudes = amplitudes[peaks[peak_indices]]

    # frequency_amplitude_pairs = list(zip(frequencies, amplitudes))
    # frequency_amplitude_pairs.sort(key=lambda x: x[1], reverse=True)

    # top_frequencies = [pair[0] for pair in frequency_amplitude_pairs[:16]]
    # top_amplitudes = [pair[1] for pair in frequency_amplitude_pairs[:16]]

    # for j in range(0, len(top_frequencies)-1):
    #     for k in range(j+1, len(top_frequencies)):
    #         if top_frequencies[k]:
    #             ratio = top_frequencies[j] / top_frequencies[k]
    #             if ratio > 98/100 and ratio < 100/98:
    #                 top_amplitudes[j] /= 0.8
    #                 top_amplitudes[k] *= 0.8

    # frequency_amplitude_pairs = list(zip(top_frequencies, top_amplitudes))
    # frequency_amplitude_pairs.sort(key=lambda x: x[1], reverse=True)

    # top_frequencies = [pair[0] for pair in frequency_amplitude_pairs[:16]]
    # top_amplitudes = [pair[1] for pair in frequency_amplitude_pairs[:16]]

    frame_frequencies.append(top_frequencies)
    frame_amplitudes.append(top_amplitudes)

oldpsgh = np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
oldpsgl = np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
oldpsgv = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

preamble="""
zsm:
  version: 0x01  # Version 1 is the only valid value at this time
  fm_channel_mask: 0b_0000_0000  # FM channels that are touched by this ZSM need to have a 1 here. Channel number 0 is the rightmost bit.
  psg_channel_mask: 0b_1111_1111_1111_1111 # PSG channels that are touched by this ZSM need to have a 1 here. Channel number 0 is the rightmost bit.
  tick_rate: 60 # Number of ticks per second
  reserved_header: 0x0000 # For future use
  data:
  - psg_write: # Preamble
    - addr: 0x03
      data: 0x80
    - addr: 0x07
      data: 0x80
    - addr: 0x0b
      data: 0x80
    - addr: 0x0f
      data: 0x80
    - addr: 0x13
      data: 0x80
    - addr: 0x17
      data: 0x80
    - addr: 0x1b
      data: 0x80
    - addr: 0x1f
      data: 0x80
    - addr: 0x23
      data: 0x80
    - addr: 0x27
      data: 0x80
    - addr: 0x2b
      data: 0x80
    - addr: 0x2f
      data: 0x80
    - addr: 0x33
      data: 0x80
    - addr: 0x37
      data: 0x80
    - addr: 0x3b
      data: 0x80
    - addr: 0x3f
      data: 0x80"""

print(preamble)

delay = 0

# Print the frequencies and amplitudes for each frame
for i, (freqs, amps) in enumerate(zip(frame_frequencies, frame_amplitudes)):
    #print(f"Frame {i}:")
    delay += 1
    psgused = np.array([False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False])
    newpsgh = np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
    newpsgl = np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
    newpsgv = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

    groupstart = True

    for freq, amp in zip(freqs, amps):
        psgfreq = round(freq * ((2**17) / 48828.125))
        psglow = psgfreq & 0xff
        psghigh = (psgfreq >> 8) & 0xff
        psgvol = process_amplitude(amp * 6)

        freqmatchi = np.where((psgused == False) & (psglow == oldpsgl) & (psghigh == oldpsgh))
        freqhmatchi = np.where((psgused == False) & (psghigh == oldpsgh))
        volmatchi = np.where((psgused == False) & (psgvol == oldpsgv))
        unusedi = np.where(psgused == False)

        if freqmatchi[0].size:
            idx = freqmatchi[0][0]
        elif freqhmatchi[0].size:
            idx = freqhmatchi[0][0]
        elif volmatchi[0].size:
            idx = volmatchi[0][0]
        elif unusedi[0].size:
            idx = unusedi[0][0]

        psgused[idx] = True
        newpsgh[idx] = psghigh
        newpsgl[idx] = psglow
        #print ("Idx: {} vol: {} amp: {}".format(idx, psgvol, amp))
        newpsgv[idx] = psgvol
        
        #print(f"  Frequency: {freq} Hz, Amplitude: {amp}")

        if (newpsgl[idx] != oldpsgl[idx] and psgvol):
            if (groupstart):
                while delay > 63:
                    print("  - delay: 0x3f")
                    delay -= 63
                print("  - delay: 0x{:02x}".format(delay))
                delay = 0
                print("  - psg_write: # Frame {}".format(i))
                groupstart = False
            print("    - addr: 0x{:02x}".format(idx * 4))
            print("      data: 0x{:02x}".format(newpsgl[idx]))
            oldpsgl[idx] = newpsgl[idx]
        if (newpsgh[idx] != oldpsgh[idx] and psgvol):
            if (groupstart):
                while delay > 63:
                    print("  - delay: 0x3f")
                    delay -= 63
                print("  - delay: 0x{:02x}".format(delay))
                delay = 0
                print("  - psg_write: # Frame {}".format(i))
                groupstart = False
            print("    - addr: 0x{:02x}".format(idx * 4 + 1))
            print("      data: 0x{:02x}".format(newpsgh[idx]))
            oldpsgh[idx] = newpsgh[idx]
        if (newpsgv[idx] != oldpsgv[idx]):
            if (groupstart):
                while delay > 63:
                    print("  - delay: 0x3f")
                    delay -= 63
                print("  - delay: 0x{:02x}".format(delay))
                delay = 0
                print("  - psg_write: # Frame {}".format(i))
                groupstart = False
            print("    - addr: 0x{:02x}".format(idx * 4 + 2))
            print("      data: 0x{:02x}".format(newpsgv[idx] | 0xc0))
            oldpsgv[idx] = newpsgv[idx]


print("  - eod")
