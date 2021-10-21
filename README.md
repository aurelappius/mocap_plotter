# Mocap Plotter

Simple Python Script to plot the Motion Capture Data from the Vicon System using Matplotlib.

The following command will run the script:

<code>python3 mocap_plotter.py your_data.csv</code>.

Data has to have the following collums: 
"Frame", "Framerate", "Latency", "x", "y", "z", "roll", "pitch", "yaw","err"

the "err" column will be removed soon.

The data can be collected using the mocap_data_logger (hyperlink tbd)
