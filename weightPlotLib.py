import os
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt
from datetime import date, timedelta

def to_24hour(hour, ampm):
    """Convert a 12-hour time and "am" or "pm" to a 24-hour value."""
    hour = int(hour)
    if ampm == 'AM':
        return 0 if hour == 12 else hour
    else:
        return 12 if hour == 12 else hour + 12

def to_24hour_6pm(hour, ampm):
    """Convert a 12-hour time and "am" or "pm" to a 24-hour value zeroed at 6PM."""
    hour = int(hour)
    if ampm == 'PM':
        if hour != 12:
            hour += 12
    if ampm == 'AM':
        if hour == 12:
            hour = 0
    #now reset 0 to 6PM
    if hour >= 18:
        hour -= 18
    else:
        hour += 6

    return hour

def weightAnalysis(filename):

    #import the csv files for body weight
    #need to parse the date columns specifically as dates
    weights = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')

    #initialize empty DataFrames to be used for only nonzero values
    nonzeroWeights = pd.DataFrame(columns=['Date','Value','Units','Notes'])

    #let's only keep the nonzero values
    nonzeroWeights = weights[((weights.Value != 0))]
    #let's only keep weight values with notes attached
    nonzeroWeights = nonzeroWeights[((weights.Notes != 'No comments.'))]

    #reset the indices to go from 0 and count up by 1
    nonzeroWeights = nonzeroWeights.reset_index()

    #let's split the notes section into time and notes
    nonzeroWeightsHour = pd.DataFrame(nonzeroWeights.Notes.str.split(':',1).tolist(),
                                   columns = ['Hour','Notes'])
    nonzeroWeightsMinute = pd.DataFrame(nonzeroWeightsHour.Notes.str.split(' ',1).tolist(),
                                   columns = ['Minute','Notes'])
    nonzeroWeightsAMPM = pd.DataFrame(nonzeroWeightsMinute.Notes.str.split(' ',1).tolist(),
                                   columns = ['AMPM','Notes'])

    #delete old notes column
    del nonzeroWeights['Notes']

    #add back in the time, AMPM values, and Notes
    nonzeroWeights['Hour'] = nonzeroWeightsHour['Hour']
    nonzeroWeights['Minute'] = nonzeroWeightsMinute['Minute']
    nonzeroWeights['AMPM'] = nonzeroWeightsAMPM['AMPM']
    nonzeroWeights['Notes'] = nonzeroWeightsAMPM['Notes']

    #initialize 24 hour column with something that we can replace later
    nonzeroWeights['24 Hour Time'] = nonzeroWeightsHour['Hour']

    #re-index by date
    nonzeroWeights = nonzeroWeights.set_index('Date')

    #convert to 24 hour time
    for date in nonzeroWeights.index:
        nonzeroWeights.loc[date,'24 Hour Time'] = to_24hour_6pm(nonzeroWeights.loc[date,'Hour'], nonzeroWeights.loc[date,'AMPM']) + float(nonzeroWeights.loc[date,'Minute'])/60.0

    nonzeroWeights.reindex(['Date'])
    return nonzeroWeights


def weightDifference(data1, data2):
    difference = pd.DataFrame(columns=['Weight Difference','Time Difference'])
    difference['Weight Difference'] = data2['Value']
    for date in data2.index:
        if date in data1.index and data1.loc[date,'AMPM'] == 'AM':
            difference.loc[date,'Weight Difference'] = data2.loc[date,'Value'] - data1.loc[date,'Value']
        elif (date-timedelta(days=1)) in data1.index:
            difference.loc[date,'Weight Difference'] = data2.loc[date,'Value'] - data1.loc[date-timedelta(days=1),'Value']

        if date in data1.index and data1.loc[date,'AMPM'] == 'AM':
            difference.loc[date,'Time Difference'] = data2.loc[date,'24 Hour Time'] - data1.loc[date,'24 Hour Time']
        elif (date-timedelta(days=1)) in data1.index:
            difference.loc[date,'Time Difference'] = data2.loc[date,'24 Hour Time'] - data1.loc[date-timedelta(days=1),'24 Hour Time']
        
    return difference 

