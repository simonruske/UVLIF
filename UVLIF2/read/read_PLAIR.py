import os
import zipfile


def read_PLAIR(cfg, info, g, l):

  if info[1] == '-1':
    return

  # unzip the file
  zip_ref = zipfile.ZipFile(info[0], 'r')
  zip_ref.extractall(os.path.join(cfg['main_directory'], "temp"))

  # read in the file
  filename = os.listdir(os.path.join(cfg['main_directory'], "temp"))[0]
  full_filename = os.path.join(cfg['main_directory'], "temp", filename)
  f = open(full_filename)

  # get the header
  for line in f:
    if line.startswith("#global"):
      break

  header = line.strip('\n').split(',')

  for line in f:
    output_list = line.strip('\n').split(',')[:432-48] + line.strip('\n').split(',')[432:432+256]
    output_str = ','.join(output_list) + '\n'
    g.write(output_str)
    l.write(info[1] + "\n")
 




'''
from collections import Counter
import numpy as np
from matplotlib.pyplot import plot, show
from datetime import datetime, timedelta

FL_total = []

def read_file(FL_total, filename):
 
  minute_FL_total = []

  # get the header


  header = line.strip('\n').split(',')

  # 946 columns 432 - 687 are FL so read in the rest and total
  for line in f:

    #
    aggregate_FL = sum(np.array(line.strip('\n').split(',')[464:496], 'float'))
    aggregate_FL -= sum(np.array(line.strip('\n').split(',')[688-32:688], 'float'))
    minute_FL_total.append(aggregate_FL)
  FL_total.append(np.mean(minute_FL_total))
  
  
  


  # remove the file when finished
  os.remove(os.path.join(os.curdir, "PLAIR_temp", os.listdir(os.path.join(os.curdir, "PLAIR_temp"))[0]))



  



    
  

dt = []
for filename in np.sort(os.listdir(directory)):
  if analysis_date in filename:
    
    try:
      read_file(FL_total, os.path.join(directory, filename))
    except Exception:
      continue
    dt.append(datetime.strptime(filename[12:-4], "%Y%m%d%H%M"))
  

# put nans in where there are gaps
full_dt = []
full_FL_total = []
for item in np.arange(min(dt), max(dt), timedelta(minutes = 1)):
  cur_date = datetime.strptime(str(item)[:16], "%Y-%m-%dT%H:%M")
  full_dt.append(cur_date)
  if cur_date in dt:
    for i, date in enumerate(dt):
      if cur_date - date  < timedelta(minutes = 0.99):
        break
    print(i)
    full_FL_total.append(FL_total[i])
  else:
    full_FL_total.append(np.NaN)



# plot the totals
plot(dt, FL_total)
#plot(full_dt, full_FL_total)
show()


'''
