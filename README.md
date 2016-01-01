# open-rc-buggy-simulator

![Simulated Buggy Jumps](https://github.com/juherask/open-rc-buggy-simulator/raw/master/images/jump.gif)

A work-in-progress open source simulator for radio-controlled off-road buggies. It is built on a entirely open source stack:

* Linux
* Blender3D / Blender game engine / Bullet physics
* uinput
* Arduino IDE

However, pull requests to make it work on Windows are welcome. What would be required is to hack a Arduino joystick driver to work with the soon-to-be included Arduino RX-PC bridge.

The Blender3d has a built-in game engine BGE, which in turn uses the Bullet physics engine. The RC buggy in this simulator is built using 6-degrees-of-freedom (6dof) rigid body joints and gravity, friction, collisions etc. are provided by the Bullet physics engine.

![The structure of the car model under the hood](https://raw.githubusercontent.com/juherask/open-rc-buggy-simulator/master/images/model.png)


# Feature highlights
* A Bullet physics powered 3D RC buggy model
 * Friction for each wheel to all different directions x,y,z (via Anisotropic Friction)
 * Suspension with springs and shocks using rigid body 6dof joints with all but z-axis fixed. The min/max limits for z-axis can be used to adjust the down/uptravel of the shock.
 * Front and back ends are connected by 6rigid body joint

# Implementation notes

The buggy model is built as follows:
* (F)ront and (B)ack end of the buggy are cube objects that are connected using a rigid body 6dof joint constraint with all axis and rotations fixed. In the future this allows some leeway in case chassis flex is modeled (allowing adjusting the flex in horizontal and vertical direction using Servo Actuators or python script applying torques and forces.
