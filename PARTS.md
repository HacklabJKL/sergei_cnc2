Sergei 2 CNC machine parts list
===============================

Machine body
------------

* 20x40 mm steel tubing
* 50x50 mm steel tubing
* M6 cap head screws
* Spray painted black

Bridge / X-axis
---------------

* Premade [1000 mm ballscrew linear assembly](mechanical/plans_solvespace/linear_assembly_1000mm.txt)
* Utopi DC [motor](notes/Motor_UGRMEM-04MMA31.txt) and [encoder](notes/Encoder_UTOPI_O25SD.txt)
* [DIY 48VDC motor driver](electronics/motor_driver/)
* Cable chain
* Mounted with M8 cap head screws
* Canvas dust shield, [DIY](http://essentialscrap.com/cnc2/dust_shields/)

Table / Y-axis
--------------

* Premade [760 mm ballscrew linear assembly](mechanical/plans_solvespace/linear_assembly_700mm.txt) for movement
* Utopi DC [motor](notes/Motor_UGRMEM-04MMA31.txt) and [encoder](notes/Encoder_UTOPI_O25SD.txt)
* [DIY 48VDC motor driver](electronics/motor_driver/)
* Dual linear rails for table support
* [Aluminum extrusion 30x120 I-type](https://www.dold-mechatronik.de/Aluminum-profile-30x120L-I-type-groove-6) for T-slot table

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

* [Vevor 0.8kW Air-cooled ER11 spindle](https://eur.vevor.com/spindle-motor-c_10130/vevor-0-8kw-er11-air-cooled-spindle-motor-24000rpm-for-milling-engraving-machine-p_010636027589?utm_source=email_sys&utm_medium=mail&utm_campaign={en}_{EU}_{orderDelivery}_{2022-04-25%2017:21:27})
* [Vevor 1.5kW VFD](https://eur.vevor.com/variable-frequency-drives-c_10745/vevor-2hp-1-5kw-vfd-variable-frequency-drive-220v-inverter-soundl-solutions-p_010276894883?utm_source=email_sys&utm_medium=mail&utm_campaign={en}_{EU}_{orderDelivery}_{2022-04-24%2019:21:47}) [manual](datasheets/Vevor_A2_8015_VFD_Manual_v1.8.pdf)
* [65 mm spindle motor clamp](https://www.ebay.com/itm/293600909919)
* 50°C overtemperature switch
* [NICEYRIG rail](https://www.ebay.com/itm/293185219621) for mounting dust collection & other extra tools

Coolant supply
--------------

* 2x 4 mm hose routed through cable chains in right side Z column and X axis to the spindle mount.
* [24V peristaltic pump](https://www.ebay.com/itm/274481580980)

Cabinet
-------

* 48x48 mm vertical wood beams
* 48x98 mm horizontal wood beams
* Plywood base for the machine
* Originally designed for robot hand project, original plans: [1](notes/cabinet1.jpg) [2](notes/cabinet2.jpg)

Control PC
----------

* Dell OptiPlex 990/0D6H9T, 8 GB RAM, 120 GB SSD
* [Mesa 6i25 FPGA card](http://store.mesanet.com/index.php?route=product/product&product_id=58)
* Novation Nocturn USB pad for manual control

Control electronics
-------------------
* 48 VDC 2 kW power supply for axis motors
* Operating mode selection switch: [GX1653U](https://www.tme.eu/en/details/gx1653u/cam-switches/lovato-electric/) or similar
* Emergency stop switch
* [Power control board](electronics/power_control_pcb/images/power_control_pcb.pdf)
* [Wiring diagram](electronics/wiring/images/sergei2-wiring.pdf)

