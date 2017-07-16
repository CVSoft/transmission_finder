Description of the 148.465 MHz Transmission Detection Software
Software written by Brandon Longo and released under AGPL v3, unless otherwise specified.
16 July 2017
==============================================================


Data Collection
===============
rtl_power collects spectrum data from a standard RTL-SDR. The setup used is configured for a 100 kHz bandwidth of 148.400 to 148.500 MHz, with a resolution better than 750 Hz (rtl_power selects 390.63 Hz). The scripts should be able to accept any spectrum setup, as long as it includes 148.465 MHz and the resolution is sufficient to allow a narrowband FM signal to be discriminated against background noise and interference. This outputs to a CSV file, which can be directly visualized using heatmap.py (see generate_heatmap.bat). 


heatmap.py
==========
heatmap.py is an externally provided standalone script, written by Kyle "Keenerd" Keen, that turns a CSV file from rtl_power into a .png image. It does little more than parsing the CSV format, extracting the power levels, and applying a color gradient to them. It requires Python 2.7 or newer, and the Pillow image processing library. As it discards timestamp info, it cannot be used alone to determine transmission times. However, since it maps raw data to a png, rows in the CSV file directly correspond to the PNG file's pixel rows. 


rtl_power_process.py
====================
rtl_power_process.py is a library that facilitates reading of the CSV output of rtl_power. It is general purpose, but used only by freebander_transmission_find.py for this purpose. It defines a Line object, which is a container for all of the data provided in one line of the CSV output. Additionally, it provides a simple noise floor calculation, which is the average of the bottom one-third of the spectrum power values. It also includes some debugging functions, such as a function that plots the cSV data on a text-based graph. 

Command-line syntax:
python rtl_power_process.py filename.csv
Displays a CSV file graphically, using the text-based graph debugging function. Press ENTER to go to the next line of the CSV, and Ctrl-C or end-of-file to exit. 


freebander_transmission_find.py
===============================
This script depends on rtl_power_process.py and contains the code specific to identifying the timing and duration of transmissions on 148.465 MHz. It accepts data collected from rtl_power generated within the contraints listed in the Data Collection section, and produces a text file summary of detected transmissions. A transmission is defined as an increase of peak signal strength within a region of spectrum about +/- 5 kHz of 148.465 MHz, exceeding the calculated noise floor of the entire CSV line by some margin (2 dB by default). The start time of a transmission is the timestamp of the first line in which it is first detected, and the end time is the timestamp of the first line in which a transmission is not found, provided no detections occur in the following minute. Thus, conversations in which both sides can be heard are classified as a single transmission; this keeps the output concise. 

Command-line syntax:
python freeband_transmission_find.py input-filename.csv output-filename.txt (float)dB-detection-margin
Parses a CSV input and produces a summary of transmissions in a text file. 


Execution Notes
===============
This software was written and tested on Python 2.7.13, with Pillow 4.2.1. While all of the Python scripts will work on Linux without modification, the software was only tested on Windows 7 x86, and expects Python to be added to PATH. heatmap.py is compatible with Python 3, but rtl_power_process.py and freebander_transmission_find.py are not. 