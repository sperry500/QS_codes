import sys
import pandas as pd
from matplotlib import pyplot as plt
from weightPlotLib import weightAnalysis, weightDifference

morning=weightAnalysis('BodyWeightMorning.csv')
night=weightAnalysis('BodyWeightNight.csv')

#plot weight vs. date
plt.figure()
plt.plot(morning.index,morning['Value'],'r-', label='Morning')
plt.plot(night.index,night['Value'],'b-', label='Night')
plt.xlabel('Date')
plt.ylabel('Weight (lbs)')
plt.legend(loc='best')
plt.show()

#plot time of day vs. date
plt.figure()
plt.plot(morning.index,morning['24 Hour Time'],'ro', label='Morning')
plt.plot(night.index,night['24 Hour Time'],'bo', label='Night')
plt.xlabel('Date')
plt.ylabel('Hours since 6 PM')
plt.legend(loc='best')
plt.show()

difference=weightDifference(night, morning)

    
