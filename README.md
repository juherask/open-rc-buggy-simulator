# open-rc-buggy-simulator

![Simulated Buggy Jumps](https://github.com/juherask/open-rc-buggy-simulator/raw/master/images/jump.gif)

** NOTE: Developed on Blender 2.71. Use that specific version when developing this game. **
A work-in-progress open source simulator for radio-controlled off-road buggies. It is built on a entirely open source stack:

* Linux
* Blender3D / Blender game engine / Bullet physics
* uinput
* Arduino IDE

However, the game is entirely playable on Windows / OSX if Blender 2.71 is installed. Pull requests to make RC TX/RX to work on Windows are welcome. What would be required is to hack a Arduino joystick driver to work with the soon-to-be included Arduino RX-PC bridge.

The Blender3d has a built-in game engine BGE, which in turn uses the Bullet physics engine. The RC buggy in this simulator is built using 6-degrees-of-freedom (6dof) rigid body joints and gravity, friction, collisions etc. are provided by the Bullet physics engine. It should be just a matter of setting the parameters of the chassis for other car types as soon as the car physics model is made parametric.

![The structure of the car model under the hood](https://raw.githubusercontent.com/juherask/open-rc-buggy-simulator/master/images/model.png)


# Feature highlights
* A Bullet physics powered 3D RC buggy model
 * Friction for each wheel to all different directions x,y,z (via Anisotropic Friction)
 * Independent suspension with springs and shocks using rigid body 6dof joints with all but z-axis fixed. The min/max limits for z-axis can be used to adjust the down/uptravel of the shock (the python script for shock absorbers is working in another prototype and will be imported quite soon). It is possible to implement the effect of different shock positions to the progressivity of the suspension via this script. 
 * The suspension allows tuning the geometry: caster, camber, toe and kickoff. The effect on the car can be simulated if the Physics engine does not support it directly.
 * Front and back ends of the chassis are connected by 6rigid body joint. This allows simulation of chassis flex (not yet implemented).
 * Center-of-gravity is modeled and can be tuned. 
* Use your own RC transmitter as the game controller. The required adapter only costs an [euro and some cents](http://www.ebay.com/itm/USB-Nano-V3-0-ATmega328-16M-5V-Micro-controller-CH340G-board-For-Arduino-1PC-/381506734078), some wires and time to put it together.

# Implementation notes

The buggy model is built as follows:
* (F)ront and (B)ack end of the buggy are cube objects that are connected using a rigid body 6dof joint constraint with all axis and rotations fixed. In the future this allows some leeway in case chassis flex is modeled (allowing adjusting the flex in horizontal and vertical direction using Servo Actuators or python script applying torques and forces.
* TBD...
