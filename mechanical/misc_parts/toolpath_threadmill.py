import math

minor = 1.4
major = 2.4
shaftlen = 5
safedist = 5
tool_width = 0.7
stock_diameter = 3
initial_offset = 0.3 # stock_diameter / 2.0
advance = 0.05

def generate(offset):
    # Go to near center bottom of rod
    print("G0 X%0.3f" % safedist)
    print("G0 Z0 Y0")
    print("G1 X%0.3f F200" % offset)
    
    # Retract and go down in 60 deg angle
    tan60 = math.tan(math.radians(60))
    x = major / 2.0 + tool_width * tan60 / 2
    y = x / tan60
    print("G1 X%0.3f Z%0.3f" % (x + offset, -y))
    
    # Go to minor diameter in 60 deg angle
    dx2 = (major - minor) / 2.0
    y2 = y + tool_width + dx2 / tan60
    print("G1 X%0.3f Z%0.3f" % (minor / 2.0 + offset, -y2))
    
    # Go to shaft length
    print("G1 Z%0.3f" % (-shaftlen))
    
    # Go out in 45 deg angle
    stock_rad = stock_diameter / 2.0
    print("G1 X%0.3f Z%0.3f" % (stock_rad + offset, -shaftlen - stock_rad))
    
    # Go out to safe distance
    print("G0 X%0.3f" % safedist)


print("M3 S15000")
offset = initial_offset
while offset > 0:
    generate(offset)
    offset = max(0.0, offset - advance)

# A few spring passes
for i in range(3):
    generate(0.0)

print("M2")
