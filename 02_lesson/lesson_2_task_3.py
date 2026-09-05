def square(side):
    area = side * side
    if not isinstance(side, int):
        area = -(-int(area) // 1)  
        
    return area


print(square(5))     
print(square(2.5))