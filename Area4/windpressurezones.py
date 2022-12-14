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


def length_between2_points(x1,y1,z1,x2,y2,z2):
      
    lenght = math.sqrt(pow((x1-x2),2)+pow((y1-y2),2)+pow((z1-z2),2))
    return lenght
  

def new_coordinates_in_line(line,a,length):
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


    return x[0],y[0],z[0],x[1],y[1],z[1]

    
def n_rake_eave_ridge(i):
    
    n = 0
    
    for j in range(1,line_count+1):   
  
        if str("\'" +"l"+str(j)+"\'") in str(data[i]).lower():
            
            if data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "EAVE" or data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RAKE" or data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RIDGE":
                n = n + 1
    
    return n

"""nuo x2 iki x1"""
def get_the_vector(x1,y1,z1,x2,y2,z2):

    vectorx = x1 - x2
    vectory = y1 - y2
    vectorz = z1 - z2

    return vectorx,vectory,vectorz

def add_the_vectors(vx1,vy1,vz1,vx2,vy2,vz2):

    vectorx = vx1 + vx2
    vectory = vy1 + vy2
    vectorz = vz1 + vz2
    
    
    return vectorx,vectory,vectorz







"""problem"""
n2 = n_rake_eave_ridge(0) *2

cx = [[0]*polygon_count]*n2
cy = [[0]*polygon_count]*n2
cz = [[0]*polygon_count]*n2
    


i=0


    
p = 0

for j in range(1,line_count+1):
    
    

    if str("\'" +"l"+str(j)+"\'") in str(data[i]).lower():
        

        if data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "EAVE" or data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RAKE" or data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RIDGE":
            
                line = data[i]["POLYGON"]["@path"]["L"+str(j)]
                
                cx[i][p], cy[i][p], cz[i][p], cx[i][p+1], cy[i][p+1], cz[i][p+1] = new_coordinates_in_line(line,a,length(line))
                
                p = p + 2
n3 = n_rake_eave_ridge(0)

cx1 = [[0]*polygon_count]*n3
cy1 = [[0]*polygon_count]*n3
cz1 = [[0]*polygon_count]*n3
co = 0
                 

"""find 2 closest points"""

i = 0
    
p = 0

for j in range(1,line_count+1):
    
    

    if str("\'" +"l"+str(j)+"\'") in str(data[i]).lower():
        

        if data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "EAVE" or data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RAKE" or data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RIDGE":
            
            line = data[i]["POLYGON"]["@path"]["L"+str(j)]

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
                    
            for k in range(0,2):
                
                sx1 = cx[i][0]
                sy1 = cy[i][0]
                sz1 = cz[i][0]

                sx2 = cx[i][0]
                sy2 = cy[i][0]
                sz2 = cz[i][0]
                for b in range(0,9):
                    sb1=length_between2_points(sx1,sy1,sz1,x[k],y[k],z[k])

                    sb2=length_between2_points(sx2,sy2,sz2,x[k],y[k],z[k])

                    sk=length_between2_points(cx[i][b],cy[i][b],cz[i][b],x[k],y[k],z[k])

                    if sb1 > sk:
                        sx1=cx[i][b]
                        sy1=cy[i][b]
                        sz1=cz[i][b]

                    elif sb1 > sk:
                        sx2=cx[i][b]
                        sy2=cy[i][b]
                        sz2=cz[i][b]

                vx1,vy1,vz1 = get_the_vector(sx1,sy1,sz1,x[k],y[k],z[k])
                vx2,vy2,vz2 = get_the_vector(sx2,sy2,sz2,x[k],y[k],z[k])
                avx,avy,avz = add_the_vectors(vx1,vy1,vz1,vx2,vy2,vz2)
                """l = math.sqrt(pow(sb1,2)+pow(sb2),2)  (l / length)"""

                
                if(co % 2) == 0:
                    cx1[i][co] = x[k] + avx
                    cy1[i][co] = y[k] + avy
                    cz1[i][co] = z[k] + avz

                else:
                    cx1[i][co] = x[k] - avx
                    cy1[i][co] = y[k] - avy
                    cz1[i][co] = z[k] - avz

                co = co + 1
                    

"""
for i in range(0,n2+1):
    print("("+str(cx[0][i])+","+str(cy[0][i])+","+str(cz[0][i])+")")


for i in range(0,n3+1):
    print("("+str(cx1[0][i])+","+str(cy1[0][i])+","+str(cz1[0][i])+")")
"""


"""

for i in range(0,polygon_count):
    
    for j in range(1,line_count+1):   
    
        if str("\'" +"l"+str(j)+"\'") in str(data[i]).lower():
            
    
            if data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "EAVE" or data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RAKE" or data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] == "RIDGE":
                
                   line = data[i]["POLYGON"]["@path"]["L"+str(j)]
                   print("xyz wind zone coordinates for F" + str(i) + " Type " +  str(data[i]["POLYGON"]["@path"]["L"+str(j)]["Type"] ))
                   print(new_coordinates_in_line(line,a,length(line)))
                   
                   
                   

"""


