import math

# Objective: find all factors that give the area:

area = 2930
area_range = [area]
for i in range(0,10):
    area +=1
    area_range.append(area)
factor_list = []
for height in range(6, area+1):
    for width in range(6, area+1):
        if (height*width in area_range) and (height <= width):
            factor_list.append((width, height))

print(factor_list)

# Bind and generate spinbox values for rectangular ductwork based on for loop

# see if a second bind can be made for the entry fields