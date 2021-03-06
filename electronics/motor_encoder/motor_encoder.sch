EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "AS5134 Magnetic Encoder"
Date "2021-11-13"
Rev "1"
Comp "Hacklab Jyväskylä / jpa"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L motor_encoder:AS5134 U1
U 1 1 618E5BFB
P 6800 3150
F 0 "U1" H 6550 4050 50  0000 C CNN
F 1 "AS5134" H 6550 3950 50  0000 C CNN
F 2 "Package_SO:SSOP-20_5.3x7.2mm_P0.65mm" H 6800 3100 50  0001 C CNN
F 3 "" H 6800 3100 50  0001 C CNN
	1    6800 3150
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x06 J1
U 1 1 618E65D5
P 1450 2250
F 0 "J1" H 1368 2667 50  0000 C CNN
F 1 "Program" H 1368 2576 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 1450 2250 50  0001 C CNN
F 3 "~" H 1450 2250 50  0001 C CNN
	1    1450 2250
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1650 2350 1900 2350
Wire Wire Line
	1650 2450 2250 2450
Wire Wire Line
	1650 2550 2600 2550
Text Label 2700 2050 0    50   ~ 0
VPP
Wire Wire Line
	3050 1900 3050 2150
Wire Wire Line
	1650 2150 3050 2150
$Comp
L power:GND #PWR07
U 1 1 618E7610
P 3050 3300
F 0 "#PWR07" H 3050 3050 50  0001 C CNN
F 1 "GND" H 3055 3127 50  0000 C CNN
F 2 "" H 3050 3300 50  0001 C CNN
F 3 "" H 3050 3300 50  0001 C CNN
	1    3050 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 3300 3050 3200
Wire Wire Line
	1650 2250 3050 2250
Text Label 2700 2350 0    50   ~ 0
DIO
Text Label 2700 2450 0    50   ~ 0
CLK
Text Label 2700 2550 0    50   ~ 0
CS
Wire Wire Line
	6350 2550 5650 2550
Text Label 4950 2550 2    50   ~ 0
VPP
Wire Wire Line
	6350 3050 6250 3050
Text Label 6250 3050 2    50   ~ 0
CLK
Wire Wire Line
	6350 2950 6250 2950
Text Label 6250 2950 2    50   ~ 0
DIO
Wire Wire Line
	6350 2750 6250 2750
Text Label 6250 2750 2    50   ~ 0
CS
$Comp
L Device:R R4
U 1 1 618E9407
P 2600 2850
F 0 "R4" H 2670 2896 50  0000 L CNN
F 1 "100k" H 2670 2805 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2530 2850 50  0001 C CNN
F 3 "~" H 2600 2850 50  0001 C CNN
	1    2600 2850
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 618E973B
P 2250 2850
F 0 "R3" H 2320 2896 50  0000 L CNN
F 1 "100k" H 2320 2805 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2180 2850 50  0001 C CNN
F 3 "~" H 2250 2850 50  0001 C CNN
	1    2250 2850
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 618E9914
P 1900 2850
F 0 "R2" H 1970 2896 50  0000 L CNN
F 1 "100k" H 1970 2805 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1830 2850 50  0001 C CNN
F 3 "~" H 1900 2850 50  0001 C CNN
	1    1900 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	1900 2700 1900 2350
Connection ~ 1900 2350
Wire Wire Line
	1900 2350 2700 2350
Wire Wire Line
	2250 2700 2250 2450
Connection ~ 2250 2450
Wire Wire Line
	2250 2450 2700 2450
Wire Wire Line
	2600 2700 2600 2550
Connection ~ 2600 2550
Wire Wire Line
	2600 2550 2700 2550
Wire Wire Line
	3050 3200 2600 3200
Wire Wire Line
	1900 3200 1900 3000
Connection ~ 3050 3200
Wire Wire Line
	3050 3200 3050 2250
Wire Wire Line
	2250 3000 2250 3200
Connection ~ 2250 3200
Wire Wire Line
	2250 3200 1900 3200
Connection ~ 2600 3200
Wire Wire Line
	2600 3200 2250 3200
$Comp
L Device:C C2
U 1 1 618EBAB4
P 5650 2700
F 0 "C2" H 5765 2746 50  0000 L CNN
F 1 "100nF" H 5765 2655 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5688 2550 50  0001 C CNN
F 3 "~" H 5650 2700 50  0001 C CNN
	1    5650 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 3000 2600 3200
NoConn ~ 6350 2650
$Comp
L power:GND #PWR05
U 1 1 618ED1AF
P 6000 2900
F 0 "#PWR05" H 6000 2650 50  0001 C CNN
F 1 "GND" H 6005 2727 50  0000 C CNN
F 2 "" H 6000 2900 50  0001 C CNN
F 3 "" H 6000 2900 50  0001 C CNN
	1    6000 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 2850 6000 2850
Wire Wire Line
	6000 2850 6000 2900
NoConn ~ 6350 3250
NoConn ~ 6350 3350
NoConn ~ 6350 3450
NoConn ~ 6350 3550
NoConn ~ 6350 3650
NoConn ~ 7200 2750
NoConn ~ 7200 2850
NoConn ~ 7200 2950
NoConn ~ 7200 3450
$Comp
L power:GND #PWR08
U 1 1 618F0331
P 6800 3950
F 0 "#PWR08" H 6800 3700 50  0001 C CNN
F 1 "GND" H 6805 3777 50  0000 C CNN
F 2 "" H 6800 3950 50  0001 C CNN
F 3 "" H 6800 3950 50  0001 C CNN
	1    6800 3950
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x06 J2
U 1 1 618F103D
P 1400 5450
F 0 "J2" H 1318 5867 50  0000 C CNN
F 1 "Output" H 1318 5776 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Horizontal" H 1400 5450 50  0001 C CNN
F 3 "~" H 1400 5450 50  0001 C CNN
	1    1400 5450
	-1   0    0    -1  
$EndComp
$Comp
L power:+5V #PWR01
U 1 1 618F18B3
P 3050 1900
F 0 "#PWR01" H 3050 1750 50  0001 C CNN
F 1 "+5V" H 3065 2073 50  0000 C CNN
F 2 "" H 3050 1900 50  0001 C CNN
F 3 "" H 3050 1900 50  0001 C CNN
	1    3050 1900
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR03
U 1 1 618F1C0C
P 6800 2350
F 0 "#PWR03" H 6800 2200 50  0001 C CNN
F 1 "+5V" H 6815 2523 50  0000 C CNN
F 2 "" H 6800 2350 50  0001 C CNN
F 3 "" H 6800 2350 50  0001 C CNN
	1    6800 2350
	1    0    0    -1  
$EndComp
$Comp
L Device:L_Core_Ferrite L1
U 1 1 618F28B5
P 3000 5250
F 0 "L1" V 3225 5250 50  0000 C CNN
F 1 "Ferrite 1k" V 3134 5250 50  0000 C CNN
F 2 "Inductor_SMD:L_0603_1608Metric" H 3000 5250 50  0001 C CNN
F 3 "~" H 3000 5250 50  0001 C CNN
	1    3000 5250
	0    -1   -1   0   
$EndComp
$Comp
L Device:C C3
U 1 1 618F53ED
P 3400 5500
F 0 "C3" H 3515 5546 50  0000 L CNN
F 1 "10µF" H 3515 5455 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3438 5350 50  0001 C CNN
F 3 "~" H 3400 5500 50  0001 C CNN
	1    3400 5500
	1    0    0    -1  
$EndComp
$Comp
L Device:C C4
U 1 1 618F5961
P 3900 5500
F 0 "C4" H 4015 5546 50  0000 L CNN
F 1 "100nF" H 4015 5455 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3938 5350 50  0001 C CNN
F 3 "~" H 3900 5500 50  0001 C CNN
	1    3900 5500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 5250 3400 5250
Wire Wire Line
	3900 5250 3900 5350
Wire Wire Line
	3400 5350 3400 5250
Connection ~ 3400 5250
Wire Wire Line
	3400 5250 3900 5250
$Comp
L power:GND #PWR010
U 1 1 618F69C1
P 3900 5900
F 0 "#PWR010" H 3900 5650 50  0001 C CNN
F 1 "GND" H 3905 5727 50  0000 C CNN
F 2 "" H 3900 5900 50  0001 C CNN
F 3 "" H 3900 5900 50  0001 C CNN
	1    3900 5900
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR09
U 1 1 618F6F12
P 3900 5100
F 0 "#PWR09" H 3900 4950 50  0001 C CNN
F 1 "+5V" H 3915 5273 50  0000 C CNN
F 2 "" H 3900 5100 50  0001 C CNN
F 3 "" H 3900 5100 50  0001 C CNN
	1    3900 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 5100 3900 5250
Connection ~ 3900 5250
Wire Wire Line
	3900 5900 3900 5750
Wire Wire Line
	3900 5750 3400 5750
Wire Wire Line
	3400 5750 3400 5650
Connection ~ 3900 5750
Wire Wire Line
	3900 5750 3900 5650
Wire Wire Line
	1600 5350 3000 5350
Wire Wire Line
	3000 5350 3000 5750
Wire Wire Line
	3000 5750 3400 5750
Connection ~ 3400 5750
Wire Wire Line
	1600 5450 1700 5450
Wire Wire Line
	1600 5550 1700 5550
Wire Wire Line
	1600 5650 1700 5650
Text Label 1700 5450 0    50   ~ 0
B
Text Label 1700 5550 0    50   ~ 0
A
Text Label 1700 5650 0    50   ~ 0
Z
Wire Wire Line
	1600 5750 3000 5750
Connection ~ 3000 5750
Text Label 8250 3250 0    50   ~ 0
B
Text Label 8250 3150 0    50   ~ 0
A
Text Label 8250 3350 0    50   ~ 0
Z
$Comp
L Device:D_Schottky_ALT D1
U 1 1 618FEF8D
P 5200 2400
F 0 "D1" V 5246 2320 50  0000 R CNN
F 1 "BAT54W" V 5155 2320 50  0000 R CNN
F 2 "Diode_SMD:D_SOD-123" H 5200 2400 50  0001 C CNN
F 3 "~" H 5200 2400 50  0001 C CNN
	1    5200 2400
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1650 2050 2700 2050
Connection ~ 5650 2550
Wire Wire Line
	5650 2550 5200 2550
$Comp
L Device:C C1
U 1 1 61903876
P 5200 2700
F 0 "C1" H 5315 2746 50  0000 L CNN
F 1 "10µF" H 5315 2655 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5238 2550 50  0001 C CNN
F 3 "~" H 5200 2700 50  0001 C CNN
	1    5200 2700
	1    0    0    -1  
$EndComp
Connection ~ 5200 2550
Wire Wire Line
	5200 2550 4950 2550
$Comp
L power:+5V #PWR02
U 1 1 619059D3
P 5200 2250
F 0 "#PWR02" H 5200 2100 50  0001 C CNN
F 1 "+5V" H 5215 2423 50  0000 C CNN
F 2 "" H 5200 2250 50  0001 C CNN
F 3 "" H 5200 2250 50  0001 C CNN
	1    5200 2250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR06
U 1 1 61905BD7
P 5200 2950
F 0 "#PWR06" H 5200 2700 50  0001 C CNN
F 1 "GND" H 5205 2777 50  0000 C CNN
F 2 "" H 5200 2950 50  0001 C CNN
F 3 "" H 5200 2950 50  0001 C CNN
	1    5200 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	5200 2950 5200 2850
Wire Wire Line
	5200 2850 5650 2850
Connection ~ 5200 2850
Wire Wire Line
	7200 3150 7450 3150
Wire Wire Line
	7200 3250 7700 3250
Wire Wire Line
	7200 3350 7700 3350
$Comp
L Device:R R5
U 1 1 6190A871
P 7850 3150
F 0 "R5" V 7900 3000 50  0000 C CNN
F 1 "100" V 7850 3150 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7780 3150 50  0001 C CNN
F 3 "~" H 7850 3150 50  0001 C CNN
	1    7850 3150
	0    1    -1   0   
$EndComp
$Comp
L Device:R R6
U 1 1 6190AD4B
P 7850 3250
F 0 "R6" V 7900 3100 50  0000 C CNN
F 1 "100" V 7850 3250 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7780 3250 50  0001 C CNN
F 3 "~" H 7850 3250 50  0001 C CNN
	1    7850 3250
	0    1    -1   0   
$EndComp
$Comp
L Device:R R7
U 1 1 6190AF3D
P 7850 3350
F 0 "R7" V 7900 3200 50  0000 C CNN
F 1 "100" V 7850 3350 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7780 3350 50  0001 C CNN
F 3 "~" H 7850 3350 50  0001 C CNN
	1    7850 3350
	0    1    -1   0   
$EndComp
Wire Wire Line
	8000 3150 8250 3150
Wire Wire Line
	8000 3250 8250 3250
Wire Wire Line
	8000 3350 8250 3350
$Comp
L Device:R R1
U 1 1 6190F857
P 7850 2650
F 0 "R1" V 7643 2650 50  0000 C CNN
F 1 "4k7" V 7734 2650 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7780 2650 50  0001 C CNN
F 3 "~" H 7850 2650 50  0001 C CNN
	1    7850 2650
	0    1    1    0   
$EndComp
Wire Wire Line
	7450 3150 7450 2650
Wire Wire Line
	7450 2650 7700 2650
Connection ~ 7450 3150
Wire Wire Line
	7450 3150 7700 3150
$Comp
L Device:LED_ALT D2
U 1 1 61911074
P 8250 2650
F 0 "D2" H 8243 2395 50  0000 C CNN
F 1 "STATUS" H 8243 2486 50  0000 C CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 8250 2650 50  0001 C CNN
F 3 "~" H 8250 2650 50  0001 C CNN
	1    8250 2650
	-1   0    0    1   
$EndComp
Wire Wire Line
	8100 2650 8000 2650
Wire Wire Line
	8400 2650 8750 2650
Wire Wire Line
	8750 2650 8750 2850
$Comp
L power:GND #PWR04
U 1 1 61913527
P 8750 2850
F 0 "#PWR04" H 8750 2600 50  0001 C CNN
F 1 "GND" H 8755 2677 50  0000 C CNN
F 2 "" H 8750 2850 50  0001 C CNN
F 3 "" H 8750 2850 50  0001 C CNN
	1    8750 2850
	1    0    0    -1  
$EndComp
$Comp
L Device:D_Schottky_ALT D3
U 1 1 61917438
P 2450 5250
F 0 "D3" H 2450 5033 50  0000 C CNN
F 1 "BAT54W" H 2450 5124 50  0000 C CNN
F 2 "Diode_SMD:D_SOD-123" H 2450 5250 50  0001 C CNN
F 3 "~" H 2450 5250 50  0001 C CNN
	1    2450 5250
	-1   0    0    1   
$EndComp
Wire Wire Line
	2600 5250 2850 5250
Wire Wire Line
	2300 5250 1600 5250
$EndSCHEMATC
