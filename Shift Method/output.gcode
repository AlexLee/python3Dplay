;start.gcode
G21
G90
G28 X0 Y0
G28 Z0
G92 E0
G1 X0.08 Y0.0 Z0.481753674102 E0
G1 X0.08 Y0.5 Z0.481753674102 E0.5
G1 X0.08 Y1.0 Z0.481753674102 E1.0
G1 X0.08 Y1.5 Z0.481753674102 E1.5
G1 X0.08 Y2.0 Z0.481753674102 E2.0
M104 S0
M140 S0
G91
G1 E-1 F300
G1 Z+20 E-5
M84
G90