Sergei 2 CNC machine parts list
===============================

Machine body
------------

* 20x40 mm steel tubing
* 50x50 mm steel tubing
* M6 cap head screws
* [Epoxy paint](https://www.biltema.fi/veneily/veneen-huoltotuotteet/epoksitaytteet/epoksipohjamaali-2000023393)

Bridge / X-axis
---------------

* Premade [1000 mm ballscrew linear assembly](mechanical/plans_solvespace/linear_assembly_1000mm.txt)
* Utopi DC [motor](notes/Motor_UGRMEM-04MMA31.txt) and [encoder](notes/Encoder_UTOPI_O25SD.txt)
* [DIY 48VDC motor driver](electronics/motor_driver/)
* Cable chain
* Mounted with M8 cap head screws
* Canvas dust shield, DIY

Table / Y-axis
--------------

* Premade [760 mm ballscrew linear assembly](mechanical/plans_solvespace/linear_assembly_700mm.txt) for movement
* Utopi DC [motor](notes/Motor_UGRMEM-04MMA31.txt) and [encoder](notes/Encoder_UTOPI_O25SD.txt)
* [DIY 48VDC motor driver](electronics/motor_driver/)
* Dual linear rails for table support
* Aluminum extrusion for T-slot table

Columns / Z-axis
----------------

* Two premade [1100 mm linear assemblies](mechanical/plans_solvespace/linear_assembly_1100mm.txt)
* Trapezoidal screws TR12x3 installed inside each column
* Cable chain inside columns
* Belt drive from a central motor:
  * 2x GT2 belt, 6 mm wide, 1140 mm loop
  * 2x 100 tooth pulleys, 12 mm bore
  * 1x dual 20T pulley, 8 mm bore
  * 2x 16 mm wide smooth bearing belt tensioners
* [Motor MY1016](notes/Motor_MY1016.txt)
* [Encoder AS5134](electronics/motor_encoder)

Spindle
-------

* [Makita RT0700C](https://www.makita.fi/product/rt0700cx2j.html) with 65 mm wide mounting
* Possible update to brushless water cooled spindle later

Cabinet
-------

* 48x48 mm vertical wood beams
* 48x98 mm horizontal wood beams
* Plywood base for the machine

Control PC
----------

* Fujitsu desktop PC with Core i3 and 8 GB RAM.
* [Mesa 6i25 FPGA card](http://store.mesanet.com/index.php?route=product/product&product_id=58)
* Novation Nocturn USB pad for manual control

Control electronics
-------------------
* 48 VDC 2 kW power supply for axis motors
* Operating mode selection switch: [GX1653U](https://www.tme.eu/en/details/gx1653u/cam-switches/lovato-electric/) or similar
* Relay for spindle start / stop
* Emergency stop switch