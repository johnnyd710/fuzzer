import random, csv, sys

test_file = open(sys.argv[1],"w")

data_list = []

for iterator in range(0,100):

   test_file.write("%.13f,%.13f,%.13f \n" % (float(random.uniform(1.5,1.9)), float(random.uniform(10,10.2)), float(random.uniform(5,5.1))))



