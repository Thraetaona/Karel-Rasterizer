<div align="center">

  <h1><code>Karel Rasterizer</code></h1>

  <p>
    <strong>An image rasterizer written in Python using CodeHS' Karel API</strong>
  </p>
  
  <h3>
    <a href="https://codehs.com/sandbox/thraetaona/karel-rasterizer">Demo (With source)</a>
    <span> | </span>
    <a href="https://codehs.com/sandbox/thraetaona/karel-rasterizer/run">Demo (App)</a>
  </h3>

</div>

***

# Background

This (very, very overkill) project was done for a basic assignment in the [AP Computer Science Principles](https://en.wikipedia.org/wiki/AP_Computer_Science_Principles) ("AP CSP") class where [Karel the robot dog](https://en.wikipedia.org/wiki/Karel_(programming_language)) was supposed to paint just a few blocks by a series of hard-coded steps.

It was designed to use [CodeHS](https://en.wikipedia.org/wiki/CodeHS)' Karel Python API.

### Demos:
(Note: Make sure to set the speed to maximum when running the below demos.)

[Online interactive demo (Edit-able source code)](https://codehs.com/sandbox/thraetaona/karel-rasterizer) \
[Online demo (No source code)](https://codehs.com/sandbox/thraetaona/karel-rasterizer/run)

In order to draw a different scene, simply replace the array on lines number 127-148 (All of which start with 't.extend'.) with one of the samples provided in the 'scenes.txt' file in the './examples' folder.

---

What made my program interesting was the way it drew these images, it first constructed a 20x20 array (Framebuffer) with a one-to-one representation of the world's grids and then painted the world according to the array onto the world; it could even "upscale" the image array for larger worlds (Such as 40x40), this works just as a monitor in real life does. (Albeit slower, which is fair considering that it is running on an already-slow interpreted programming language like Python, implemented in a poorly-optimized JavaScript emulator, inside of a browser on top of the hardware.)

Although initially it is faster to hard-code the steps for drawing an image rather than writing a rasterizer to draw it for you, the latter would allow new images to be drawn in a matter of minutes as opposed to hours of hard-coding it again in the former, because you would just be modifying an array that looks similar to the world that it's going to get painted on.

For the rest of the technical details, refer to the comments inside of the source code.

---

You could also copy-paste the contents of the 'main.py' file in the './src' folder into CodeHS' editor in assignment number 2.1.10 ("Create your UltraKarel Image!") and see the rasterizer in action.


The source code is idomatic Python with some minor syntactic modifications to work-around CodeHS' Python interpreter bugs & limitations.

---

Video demonstration of a night scene image being drawn onto the world:

<p align="center" text-align="center"> <br />
  <img width="400" height="400"
    src="./docs/demo.gif?raw=true" 
    alt="Demo GIF's placeholder, If the .GIF file does not load properly then you could try manually opening the 'demo.gif' file in the 'docs' folder."
    title="A video demonstrating an image of a night scene being drawn."
  />
  <br />
  <sub>
    It takes exactly 20 seconds to fully render a 20x20 (400 pixels) world.  So, a row containg 20 pixels will be drawn every second.
  </sub>
<br /> </p>


Some other scenes: <br />
(Also found inside of the './docs' folder.)

<p align="center" text-align="center"> <br />
  <img width="400" height="400" src="./docs/derafsh-e kaviani.png?raw=true" />
  <img width="400" height="400" src="./docs/derafsh-e kaviani_4x.png?raw=true" />
  <br />
  <sub>
    The 20x20 alongside 40x40 renderings of Iran's Neo-Persian royal standard. (https://en.wikipedia.org/wiki/Derafsh_Kaviani)
  </sub>
<br /> </p>

<p align="center" text-align="center"> <br />
  <img width="400" height="400" src="./docs/night scene_4x.png?raw=true" />
  <br />
  <sub>
    The 40x40 variant of the night scene drawn earlier.
  </sub>
<br /> </p>

