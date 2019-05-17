# Hypersurfaces Software Development by Javi Fernandez
Repository to work on the Software Development project assigned by Hypersurfaces.

## How to run

1. Modify file permissions with chmod: add the following in *./Dockerfile*.
```
RUN chmod 644 app.py
```
2. Specify shebang line in the first line of executable *./app.py* to locate the right interpreter.
```
#! /usr/local/bin/python3
```
3. Build up the Docker services. 
>> Execute on terminal the next command (after cd to working directory)
```
docker-compose build
```
4. Build up the docker containers in the local directory. 
>> Execute on terminal the next command (after cd to working directory)
```
docker-compose -f docker-compose.yml up 
```
# Output
The output will be directed on your browser at: 
http://0.0.0.0:5090/

A drop down menu allows the user to select one of the three .wav audio signals that are available.

>> Channel_1 :: ch-1l.wav
>> Channel_2 :: ch-2l.wav
>> Channel_3 :: ch-3l.wav
By default Channel_1 is displayed. 

By simply selecting and submitting any other Channl the figures will be generated and displayed for the desired audio signal.

Each figure displays the audio signal (dark golden yellow), lines on top of the audio signal (dark grey), and peaks' positions as vertical lines (sky blue).

On the right pannel different options are available thanks to the Bokeh config. such as zoom in/out, scrolling, saving the figure as a .png file. 
