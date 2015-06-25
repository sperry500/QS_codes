import pandas as pd
from matplotlib import pyplot as plt

#import the csv files for body weight for morning and evening
#need to parse the date columns specifically as dates
morning = pd.read_csv('BodyWeightMorning.csv', parse_dates=['Date'])
night = pd.read_csv('BodyWeightNight.csv', parse_dates=['Date'])

#initialize empty DataFrames to be used for only nonzero values
nonzeroMorning = pd.DataFrame(columns=['Date','Value','Units','Notes'])
nonzeroNight = pd.DataFrame(columns=['Date','Value','Units','Notes'])

#let's only keep the nonzero values
nonzeroMorning = morning[((morning.Value != 0))]
nonzeroNight = night[((night.Value != 0))]

#reset the indices to go from 0 and count up by 1
nonzeroMorning = nonzeroMorning.reset_index()

#let's split the notes section into time and notes
nonzeroMorningHour = pd.DataFrame(nonzeroMorning.Notes.str.split(':',1).tolist(),
                                   columns = ['Hour','Notes'])
nonzeroMorningMinute = pd.DataFrame(nonzeroMorningHour.Notes.str.split(' ',1).tolist(),
                                   columns = ['Minute','Notes'])
nonzeroMorningAMPM = pd.DataFrame(nonzeroMorningMinute.Notes.str.split(' ',1).tolist(),
                                   columns = ['AMPM','Notes'])

#delete old notes column
del nonzeroMorning['Notes']

#add back in the time, AMPM values, and Notes
nonzeroMorning['Hour'] = nonzeroMorningHour['Hour']
nonzeroMorning['Minute'] = nonzeroMorningMinute['Minute']
nonzeroMorning['AMPM'] = nonzeroMorningAMPM['AMPM']
nonzeroMorning['Notes'] = nonzeroMorningAMPM['Notes']

print(nonzeroMorning)

def to_24hour(hour, ampm):
    """Convert a 12-hour time and "am" or "pm" to a 24-hour value."""
    hour = int(hour)
    if ampm == 'am':
        return 0 if hour == 12 else hour
    else:
        return 12 if hour == 12 else hour + 12

rows, cols = nonzeroMorning.shape

"""
THIS LOOP BELOW IS NOT PROPERLY EXECUTING...FIX NEXT TIME
"""

#convert to 24 hour time
for time in range(0,rows):
    nonzeroMorning['24 Hour Time'] = str(to_24hour(nonzeroMorning['Hour'][time], nonzeroMorning['AMPM'][time])) + ":" + nonzeroMorning['Minute'][time]

print(nonzeroMorning)

#plot weight vs. date
plt.figure()
plt.plot(nonzeroMorning['Date'],nonzeroMorning['Value'],'r-', label='Morning')
plt.plot(nonzeroNight['Date'],nonzeroNight['Value'],'b-', label='Night')
plt.xlabel('Date')
plt.ylabel('Weight (lbs)')
plt.legend(loc='best')
plt.show()



"""
#plot time vs. date
plt.figure()
plt.plot(nonzeroMorning['Date'],nonzeroMorning2['Time'],'r-', label='Morning')
#plt.plot(nonzeroNight['Date'],nonzeroNight['Value'],'b-', label='Night')
plt.xlabel('Date')
plt.ylabel('Time')
plt.legend(loc='best')
plt.show()
"""
