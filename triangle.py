import math

def triangle_type(a, b, c): 
    a = float(a)
    b = float(b) 
    c = float(c) 

    cos1 = (a**2 + b**2 - c**2) / (2*a*b) 
    cos2 = (b**2 + c**2 - a**2) / (2*b*c) 
    cos3 = (a**2 + c**2 - b**2) / (2*a*c)

    print(cos1)
    print(cos2)
    print(cos3)

    radAngle1 = math.acos(cos1)
    radAngle2 = math.acos(cos2)
    radAngle3 = math.acos(cos3)

    degAngle1 = math.degrees(radAngle1)
    degAngle2 = math.degrees(radAngle2)
    degAngle3 = math.degrees(radAngle3)

    print (degAngle1)
    print (degAngle2)
    print (degAngle3)

    if (degAngle1 >= 180) or (degAngle2 >= 180) or (degAngle3 >= 180.0):
        return "Invalid Triangle"
    if (degAngle1 == 90.0) or (degAngle2 == 90.0) or (degAngle3 == 90.0):
        return "Right angle Triangle"
    if (degAngle1 > 90.0) or (degAngle2 > 90.0) or (degAngle3 > 90.0):
        return "Obtuse Triangle"
    if (degAngle1 < 90.0) and (degAngle2 <90.0) and (degAngle3 < 90.0):
        return "Acute Triangle"

print(triangle_type(55.1, 35.0, 58.84796))