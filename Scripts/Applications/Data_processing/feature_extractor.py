import statistics, csv

test_file = open("signal_1.csv","w")

data_list = []

for iterator in range(0,100):

   data = open("data" + str(iterator) + ".csv", "r")

   for line in data:
      data_list.append(float(line))

   test_file.write("%.13f %.13f %.13f \n" % (statistics.mean(data_list), min(data_list), max(data_list)))

   del data_list[:]



