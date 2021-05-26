import csv
import random
from collections import deque
import math
import time
import os
Null=None


class Node:
    def __init__(self,link_or_val=Null):
        self.link_or_val=link_or_val
        self.next=Null

class main_list_Node:
    def __init__(self,value):
        self.value=value
        self.side_link=Null
        self.next=Null

class Scale:
    def __init__(self):        
        self.x_scale=Null
        self.y_scale=Null


scale=Scale()
x_scale1=Node(0)
x_scale1.next=Node(400)
scale.x_scale=x_scale1

y_scale1=Node(0)
y_scale1.next=Node(400)
scale.y_scale=y_scale1

main_list=main_list_Node(400)
main_list.side_link=Node()
Grid=main_list
points_in_grid=0
print("Enter bucket capacity")
bkt_capacity=int(input())
bkt_count=0

def createRandomSortedList(num, start = 1, end = 100): 
    arr = [] 
    tmp = random.randint(start, end) 
    for x in range(num): 
        while tmp in arr: 
            tmp = random.randint(start, end) 
        arr.append(tmp) 
    arr.sort() 
    return arr 


def generate_data():
    print("Enter number of records you want to generate ")
    n=int(input())
    print("Enter name for output file (without extension)")
    name=input()
    writer = csv.writer(open(name+'.csv', 'w'))
    x=["id","x-coordinate","y-coordinate"]
    writer.writerow(x)
    lsa=createRandomSortedList(n,1,n)
    for a in lsa:
        x=random.randint(0,400)
        y=random.randint(0,400)
        sd=[a,x,y]
        writer.writerow(sd)
    print("File "+name+".csv created successfully !!")




def read_data():
    print("Enter name of csv file with extension:")
    name=input()
    try:
        reader = csv.reader(open(name, 'r'))
    except:
        print("Ooops No such file Exist !!!")
        print('\n')
        add_records_csv()
    i=0
    rec=[]
    for row in reader:
        if i>0:
            xc=(int(row[0]),int(row[1]),int(row[2]))
            rec.append(xc)
        else:
            i=i+1
    return rec





def find_widest_spread_axis(arr):
    x_arr=[]
    y_arr=[]
    for i in arr:
        x_arr.append(int(i[0]))
        y_arr.append(int(i[1]))
    x_arr.sort()
    y_arr.sort()
    x_dif=x_arr[-1]-x_arr[0]
    y_dif=y_arr[-1]-y_arr[0]
    if x_dif>=y_dif:
        return 0
    return 1


def select_median(arr_temp,n):
    if n==1:
        return arr_temp[0]
    temp=[]
    for x in arr_temp:
        temp.append(int(x))
    temp.sort()
    #print(n,"L")
    
    if n % 2==1:
        return temp[int(n//2)+1]
    else:
        #print(n)
        return temp[int(n/2)]



def inspesct_bucket(file_name):
    f=open(file_name,"r")
    content=f.readlines()
    arr=[]
    cnt=0
    for line in content:
        vals=line.split()
        arr.append((vals[1],vals[2]))
        cnt+=1
    axis=find_widest_spread_axis(arr)
    arr2=[]
    for line in content:
        vals=line.split(" ")
        arr2.append(vals[axis+1])
    return select_median(arr2,cnt),axis
    
def find_grid_cell_num(entry_main):
    global scale
    x_val=entry_main[1]
    y_val=entry_main[2]
    current1=scale.x_scale
    x_cnt=0
    y_cnt=0
    while current1.next.link_or_val<x_val:
        current1=current1.next
        x_cnt+=1
    current2=scale.y_scale
    while current2.next.link_or_val<y_val:
        current2=current2.next
        y_cnt+=1
    return x_cnt,y_cnt


#axis==0 means cut will be perpendicular to x-axis
def divide_grid_cell(file_name1,file_name2,dividing_term,axis,entry_main):
    global Grid,scale
    x_cnt,y_cnt=find_grid_cell_num(entry_main)
    #print(file_name2,"GUG")
    if axis==1:
        cnt=1
        current=Grid
        while y_cnt>cnt:
            current=current.next
            cnt+=1
        nd=main_list_Node(dividing_term)
        nd.next=current.next
        nd.side_link=Node()
        lower=current.side_link
        current.next=nd
        current=nd.side_link
        if x_cnt==1:
            #print("YES@@")
            current.link_or_val=file_name2
            #lower.link_or_val=file_name1
            current.next=Node()
            current=current.next
            lower=lower.next
        else:
            current.link_or_val=lower.link_or_val
            current.next=Node()
            current=current.next
            lower=lower.next
        cnt_x=2
        while lower!=Null:
            if x_cnt==cnt_x:
                #print("YESS##")
                current.link_or_val=file_name2
                #lower.link_or_val=file_name1
                cnt_x+=1
                current.next=Node()
                current=current.next
                lower=lower.next
            current.link_or_val=lower.link_or_val
            lower=lower.next
            current.next=Node()
            current=current.next
            cnt_x+=1



    else:   #verticle line cut
        main_current=Grid
        cnt_main=1
        while main_current!=Null:
            cnt_x=1
            current=main_current.side_link

            if cnt_main==y_cnt:
                while x_cnt>cnt_x:
                    current=current.next
                    cnt_x+=1
                nxt=current.next
                #print("YESS!!")
                nd=Node(file_name2)
                nd.next=nxt
                current.next=nd
                #current.link_or_val=file_name1
                
                main_current=main_current.next
                cnt_main+=1 

            else:
                while x_cnt>cnt_x:
                    current=current.next
                    cnt_x+=1
                nxt=current.next
                nd=Node(current.link_or_val)
                nd.next=nxt
                current.next=nd                
                main_current=main_current.next
                cnt_main+=1



def update_scale(axis,dividing_term):
    global scale
    if axis==0:
        done=False
        current=scale.x_scale
        while done==False:
            if current.link_or_val<dividing_term and  current.next.link_or_val>dividing_term:
                done = True
                node=Node(dividing_term)
                node.next=current.next
                current.next=node
            else:
                current=current.next
    else:
        done=False
        current=scale.y_scale
        while done==False and current!=Null:
            if current.link_or_val<dividing_term and  current.next.link_or_val>dividing_term:
                done = True
                node=Node(dividing_term)
                node.next=current.next
                current.next=node
            else:
                current=current.next
        




def divide_data(file_name,dividing_term,axis,entry_main):
    global bkt_count
    f=open(file_name,"r")
    #print(file_name,"popq")
    content=f.readlines()
    #print(content,"IOI")
    arr1=[]
    arr2=[]
    cnt=0
    for line in content:
        vals=line.split(" ")
        if int(vals[axis+1])>=dividing_term:
            arr2.append((vals[0],vals[1],vals[2]))
        else:
            arr1.append((vals[0],vals[1],vals[2]))
        cnt+=1
    f.close()
    #print(arr1,"mmm")
    #print(arr2,"bb")
    if len(arr2)==0:
        return False
    if os.path.exists(file_name):
        os.remove(file_name)
    
    f1=open(file_name,"a+")
    file_name2="bucket_"+str(bkt_count)+".txt"
    #print("RERE")
    f2=open(file_name2,"a+")
    bkt_count+=1
    for entry in arr1:
        #print(entry,"fef")
        f1.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2]))
        #f1.write("\n")
    for entry in arr2:
        f2.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2]))
        #f2.write("\n")
    f1.close()
    f2.close()
    update_scale(axis,dividing_term)
    divide_grid_cell(file_name,file_name2,dividing_term,axis,entry_main)
    return True
    


def insert(entry):

    global points_in_grid, bkt_capacity,bkt_count,Grid,scale
    
    x_val=entry[1]
    y_val=entry[2]
    if points_in_grid < bkt_capacity:
        #print("Yes1")
        if points_in_grid==0:
            #print("yes2")
            f= open("bucket_"+str(bkt_count)+".txt","a+")
            f.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2]))  
            f.write("\n")          
            Grid.side_link.link_or_val="bucket_"+str(bkt_count)+".txt"
            f.close()
            bkt_count+=1
            points_in_grid+=1
        else:
            file_name=Grid.side_link.link_or_val
            f=open(file_name,"a+")
            f.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2]))
            f.write("\n")
            f.close()
            points_in_grid+=1
    elif points_in_grid==bkt_capacity: #and bkt_count==1:
        file_name=Grid.side_link.link_or_val
        f=open(file_name,"a+")
        f.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2]))
        f.write("\n")
        f.close()
        points_in_grid+=1
        dividing_term,axis=inspesct_bucket(file_name)
        res=divide_data(file_name,dividing_term,axis,entry)

        if res==False:  #Incase overflow happens
            f1=open("ovf_"+file_name,"a+")
            f=open(file_name,"r")
            content=f.readlines()
            #print(file_name,"GT")
            #print(content)
            f.close()
            if os.path.exists(file_name):
                os.remove(file_name)
            arr1=[]
            for line in content:
                vals=line.split(" ")
                arr1.append((vals[0],vals[1],vals[2]))
            cnt=0
            f2=open(file_name,"a+")
            
            for element in arr1:
                if cnt>=bkt_capacity:
                    #print(element,"KIK")
                    f1.write(str(element[0])+" "+str(element[1])+" "+str(element[2]))
                    #f1.write("\n")
                    cnt+=1
                else:
                    #print(element,"FRH")
                    f2.write(str(element[0])+" "+str(element[1])+" "+str(element[2]))
                    #f2.write("\n")
                    cnt+=1
            f1.close()
            f2.close()

        if res==True:   # if the only cell in grid is divided we need to update scales then
            #print("Greatttt")
            f=open(file_name,"r")
            #print(f.readlines(),"UUU")

    else:   #Generic case of insertion
        x_cnt,y_cnt=find_grid_cell_num(entry)
        main_current=Grid
        for i in range(y_cnt-1):
            main_current=main_current.next
        current=main_current.side_link
        for i in range(x_cnt-1):
            current=current.next
        file_name=current.link_or_val
        #print(file_name,"joj")
        f=open(file_name,"r")
        content=f.readlines()
        #print(content,"sas")
        f.close()
        count=0
        for x in content:
            count+=1
        if count<bkt_capacity:
            
            #print("ZOZOOZ",count)
            f=open(file_name,"a+")
            f.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2]))
            f.write("\n")
            f.close()
            points_in_grid+=1
        elif os.path.isfile("ovf_"+file_name):
            #print("XOXOXO")
            f=open("ovf_"+file_name,"a+")
            f.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2]))
            f.write("\n")
            f.close()
            points_in_grid+=1
        else:
            f=open(file_name,"a+")
            f.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2]))
            f.write("\n")
            f.close()
            points_in_grid+=1
            dividing_term,axis=inspesct_bucket(file_name)
            res=divide_data(file_name,dividing_term,axis,entry)
            #print("WOWOWO")
            if res==False:
                #print("KOKOKO")
                f1=open("ovf_"+file_name,"a+")
                f=open(file_name,"r")
                content=f.readlines()
                f.close()
                if os.path.exists(file_name):
                    os.remove(file_name)
                arr1=[]
                for line in content:
                    vals=line.split(" ")
                    arr1.append((vals[0],vals[1],vals[2]))
                cnt=0
                f2=open(file_name,"a+")
                for element in content:
                    if cnt>bkt_capacity:
                        f1.write(str(element[0])+" "+str(element[1])+" "+str(element[2]))
                        f1.write("\n")
                        cnt+=1
                    else:
                        f2.write(str(element[0])+" "+str(element[1])+" "+str(element[2]))
                        f2.write("\n")
                        cnt+=1
                f1.close()
                f2.close()

            
                 


def print_grid():
    global Grid,scale
    
    main_current=Grid
    while main_current:
    
        current=main_current.side_link
        while current!=Null:
            if current.link_or_val!=None:
                print("\n")             
                print(" -- ",current.link_or_val," -- ",)
                print("\n")
            current=current.next
    
        main_current=main_current.next
    

def print_scale():
    global scale
    y_current=scale.y_scale
    x_current=scale.x_scale
    print("\n")
    print("y-axis scale:")
    while y_current:
        print(y_current.link_or_val)
        y_current=y_current.next

    print("\n")
    print("x-axis scale:")
    while x_current:
        print(x_current.link_or_val)
        x_current=x_current.next
    print("\n")


    
from re import search

def print_buckets():
    arr = os.listdir()
    strtxt = ".txt"
    for txtfile in arr:
        if txtfile.__contains__(strtxt):
            print(txtfile)
            #fileObject = open(txtfile, "r")
            #data = fileObject.read()
            #print(data)
            
def print_bucket_data():
    print("Please enter bucket name to print its data with .txt")
    nm=input()
    fileObject = open(nm, "r")
    lines = fileObject.readlines()
    for line in lines:
        print(line)

        
arr5 = os.listdir()
strtxt5 = ".txt"
for txtfile5 in arr5:
    if txtfile5.__contains__(strtxt5):
        os.remove(txtfile5)
        #fileObject = open(txtfile, "r")


print("Do you want to generate dataset ? if yes enter 1 else 0")
a12=input()
if a12=="1":
    generate_data()
print("\n")
data=read_data()
for x in data:
    #print("W")
    insert(x)
print("/n")
while True:
    #print("To print Grid enter 2")
    print("To print Scales enter 3")
    print("To print buckets enter 4")
    print("To print data in a bucket enter 5")
    print("To exit enter 6")
    a23=input()
    #if a23=="2":
        #print_grid()
    if a23=="3":
        print_scale()
    if a23=="4":
        print_buckets()
    if a23=="5":
        print_bucket_data()
    if a23=="6":
        exit()





