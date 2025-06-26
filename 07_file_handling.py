#redaing a file

# with open("genome.gff3",'r')as g:
#     for i in g:
#         col=i.strip()
#         col=col.split('\t')

#         id=col[0]
#         type=col[2]
#         start_cord=col[3]
#         end_coord=col[4]
#         score=col[5]

#         print("the id is this:",id)
#         print("the type is this:",type)
#         print("the start cord is this:",start_cord)
#         print("the end cord is this:",end_coord)
#         print("the score is this:",score)


#writing a file
import csv
with open('new_genome.gff3', 'w', newline="") as file:
    writer=csv.writer(file)  
    writer.writerow(["ID","Type","Start_coord","End_coord","Score"]) 


 