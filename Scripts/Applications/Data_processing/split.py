import csv
import sys

channelA = sys.argv[1]
channelB = sys.argv[2]
out = sys.argv[3] # output directory name

test_file = open(channelA,"rb")
#data = test_file.readline()

counter = 1

pulse_counter = 0
signal_counter = 0
file_open = 0
signal_detected = 0
timestamps = []
end_timestamps = []
start_writing = 0
up=0

# goes through file, detects starting positions
# detect start and end instead for channel A
print("Detecting signals starting points...")
for line in test_file:
      time =  float(line[0:12])
      signal = float(line[13:26])

      if signal > 200:
            up = 1

      if signal < 200 and up and signal_detected == 0:
            up=0
            pulse_counter += 1
            if pulse_counter == 1:
                  signal_detected = 1
                  timestamps.append(time)
            if pulse_counter == 3:
                  pulse_counter = 0

      if up and signal_detected == 1:
            signal_detected = 0
            signal_counter += 1
            end_timestamps.append(time)

      if signal_counter >= 1000:
            break

test_file.seek(0,0)
signal_counter = 0
internal_counter = 0
num_signals = len(timestamps)
print("No. of signals:", num_signals)

test_file.close()

test_file = open(channelB,"rb")

i=0
# cut channel B
print("Splitting signals...")
for line in test_file:
      #fetch time and signal from current line
      time = float(line[:12])
      signal = float(line[13:26])

      if time < timestamps[i]:
            continue

      if file_open == 0:
            file_name = out+ "/data" + str(timestamps[i]) + ".csv"
            current_csv = open(file_name, "w")
            file_open = 1

      current_csv.write("%.13f \n" % (signal))

      if time >= end_timestamps[i]:
            internal_counter = 0
            current_csv.close()
            file_open = 0
            signal_counter += 1
            i+=1

      if signal_counter >= num_signals:
            break

test_file.close()

