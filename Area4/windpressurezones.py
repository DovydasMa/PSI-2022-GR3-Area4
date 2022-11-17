import json
import re
import math

file = open("data.json")
data = file.read()
file.close()

parsedJson = json.loads(data)
data = parsedJson["FACE"]




"""getting necessary information to parse the json file """

point_count = 0
for word in re.sub('[^a-zA-Z]', " ",str(data)).lower().replace("'", ' ').split():
    
    if "c" == word:
        point_count = point_count + 1

line_count = 0
for word in re.sub('[^a-zA-Z]', " ",str(data)).lower().replace("'", ' ').split():
    
    if "l" == word:
        line_count = line_count + 1
        
polygon_count = 0
for word in re.sub('[^a-zA-Z]', " ",str(data)).lower().replace("'", ' ').split():
    
    if "polygon" == word:
        polygon_count = polygon_count + 1
        
        
        
count = 0
low_points_sum = 0

"""getting the sum of low points"""

for i in range(0,polygon_count):    
    
    for j in range(1,line_count+1):   
  
        if str("\'" +"l"+str(j)+"\'") in str(data[i]).lower():
            
            for k in range(1,point_count+1):
            
                if data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "EAVE":
                    
                    if str("\'" +"c"+str(k)+"\'") in str(data[i]["POLYGON"]["@path"]["L"+str(j)]).lower():
                        
                        low_points_sum = low_points_sum + data[i]["POLYGON"]["@path"]["L"+str(j)]["C"+str(k)]["Z"]
                        count = count + 1
                 
            
average_lowest_hight = low_points_sum / count


count = 0
high_points_sum = 0

"""getting the sum of high points"""

if "RIDGE" in str(data):
    for i in range(0,polygon_count):    
        
        for j in range(1,line_count+1):   
      
            if str("\'" +"l"+str(j)+"\'") in str(data[i]).lower():
                
                for k in range(1,point_count+1):
                
                    if data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RIDGE":
                        
                        if str("\'" +"c"+str(k)+"\'") in str(data[i]["POLYGON"]["@path"]["L"+str(j)]).lower():
                            
                            
                            high_points_sum =  high_points_sum + data[i]["POLYGON"]["@path"]["L"+str(j)]["C"+str(k)]["Z"]
                            count = count + 1
    
             
else:
    """if roof doesnt have any ridge"""
    
    
average_highest_hight = high_points_sum / count
count = 0
average_hight = average_highest_hight - average_lowest_hight   

"""calculating the a value"""

if average_hight < 3:
    a = 0.4 * 3
else:
    a = 0.4 * average_hight               
                        
print("a is: " + str(a))








"""finds the eave line of the polygon"""

def eave_line(i): 
    
    for j in range(1,line_count+1):   
  
        if str("\'" +"l"+str(j)+"\'") in str(data[i]).lower():
            
            if data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "EAVE":
                    
                   return data[i]["POLYGON"]["@path"]["L"+str(j)]
               
                
"""lenght of the given line"""               
                
def length(line):
    x = [0,0]
    y = [0,0]
    z = [0,0]
    count = 0
    for k in range(1,point_count+1):
        if str("\'" +"c"+str(k)+"\'") in str(line).lower():
            x[count] = line["C"+str(k)]["X"]
            y[count] = line["C"+str(k)]["Y"]
            z[count] = line["C"+str(k)]["Z"]
            count = count + 1
            
            
    lenght = math.sqrt(pow((x[1]-x[0]),2)+pow((y[1]-y[0]),2)+pow((z[1]-z[0]),2))
    return lenght
  

def wind_pressure_coordinates(line,a,length):
    """parses x and y from the given line"""
    cx = [0,0]
    cy = [0,0]
    cz = [0,0]
    count = 0
    for k in range(1,point_count+1):
        if str("\'" +"c"+str(k)+"\'") in str(line).lower():
            cx[count] = line["C"+str(k)]["X"]
            cy[count] = line["C"+str(k)]["Y"]
            cz[count] = line["C"+str(k)]["Z"]
            count = count + 1
    """calculates x and y equations, a is the width of the zone which 
    is then proportionally added to the given line coordubates which results us
    getting new coordinates"""            
    vectorx = cx[1] - cx[0]
    vectory = cy[1] - cy[0]
    vectorz = cz[1] - cz[0]
    x = [0,0]
    y = [0,0]
    z = [0,0]
    x[0] = cx[1] - (a / length) * vectorx
    x[1] = cx[0] + (a / length) * vectorx
    y[0] = cy[1] - (a / length) * vectory
    y[1] = cy[0] + (a / length) * vectory
    z[0] = cz[1] - (a / length) * vectorz
    z[1] = cz[0] + (a / length) * vectorz

    

    return x, y, z

    """
    print(c[0])
    print(c[0])
    print(c[1])
    print(length)"""
    


print("new coordinates of the given line: " + str(wind_pressure_coordinates(eave_line(1),a,length(eave_line(1)))))


