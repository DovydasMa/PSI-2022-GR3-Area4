import json
import re

file = open("data.json")
data = file.read()
file.close()

parsedJson = json.loads(data)
data = parsedJson["FACE"]



polygon_count = 0
old = 0

point_count = 0
for word in re.sub('[^a-zA-Z]', " ",str(data)).lower().replace("'", ' ').split():
    
    if "c" == word:
        point_count = point_count + 1

line_count = 0
for word in re.sub('[^a-zA-Z]', " ",str(data)).lower().replace("'", ' ').split():
    
    if "l" == word:
        line_count = line_count + 1

for word in re.sub('[^a-zA-Z]', " ",str(data)).lower().replace("'", ' ').split():
    
    if "polygon" == word:
        polygon_count = polygon_count + 1
        
        
        
count = 0
low_points_sum = 0

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


if average_hight < 3:
    a = 0.4 * 3
else:
    a = 0.4 * average_hight               
                        
print("a is: " + str(a))