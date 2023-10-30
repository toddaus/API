from typing import Any

import streamlit as st
from pathlib import Path
import time
import numpy as np
import pandas as pd
from unittest import case
import datetime

from pandas import Series

from API import FWCAPI

s = pd.read_csv( 'https://raw.githubusercontent.com/toddaus/API/master/classifications.csv' )
t = pd.read_csv( 'https://raw.githubusercontent.com/toddaus/API/master/payrates.csv' )
q = pd.read_csv( 'https://raw.githubusercontent.com/toddaus/API/master/penalties.csv' )
r = pd.read_csv( 'https://raw.githubusercontent.com/toddaus/API/master/wage-allowances.csv' )
u = pd.read_csv( "https://raw.githubusercontent.com/toddaus/API/master/award_structure2.csv" )


st.write( "## Hospitality Wage Checker" )

age = st.selectbox(
    'Are you employed as Adult or as a Junior?',
    ('Adult', 'Junior') )

with st.expander( "See explanation" ):
    if age == 'Adult':
        st.write( "Adult employee means an employee who is 21 years of age or over" )
    elif age == 'Junior':
        st.write(
            "An employee who is less than 21 years of age and who is not undertaking a nationally recognised traineeship or apprenticeship" )
    else:
        st.write( "" )

option = st.selectbox(
    'What is your working arrangement?',
    ('Full Time', 'Part Time', 'Casual') )

with st.expander( "See explanation" ):
    if option == 'Part Time':
        st.write(
            "A part-time employee is an employee who is engaged to work at least 8 and fewer than 38 ordinary hours per week (or, if the employer operates a roster, an average of at least 8 and fewer than 38 hours per week over the roster cycle); and reasonably predictable hours of work." )
    elif option == 'Casual':
        st.write(
            "A person is a casual employee if there is no firm advance commitment to ongoing work with an agreed pattern of work" )
    elif option == 'Full Time':
        st.write(
            "An employee who is engaged to work an average of 38 ordinary hours per week is a full-time employee" )
    else:
        st.write( "" )

if option == 'Part Time':
    pt_hrs = st.number_input( "What hours are you employed for?", min_value=8.0, max_value=38.0, value=8.0,step = 0.5)


if age != 'Junior':
    job_filter = st.selectbox( "What is your role?", pd.unique( u['Profession'] ) )
    u2 = u[u['Profession'] == job_filter]
    job_filter2 = st.selectbox( "What is your grade?", pd.unique( u2['Grade'] ) )

    if job_filter == 'Introductory level':
        f = True
    else:
        f = False
    print( f )
    if job_filter2 != 'Null':
        u3 = u2[u2['Grade'] == job_filter2]
        indexx = u3.index[0]  # obtain the line number of the result
        u4 = u3.at[indexx, 'Level']
        u5 = u3.at[indexx, 'Level_no']
        u6 = u3.at[indexx, 'clause_description_id2']
    elif f is True:
        u4 = 'Introductory level'
        u5 = 1.0
        u6 = 'Hospitality Employees'
    else:
        u4 = 'Level 5'
        u5 = 6.0
        u6 = 'Hospitality Employees'

    profess = job_filter
    grade = job_filter2
    classification = u4
    classification_level_no = u5
    classification_id = profess + ' ' + grade

    if option == 'Full Time' and age == 'Adult' and u6 == 'Hospitality Employees':
        clause_description_id = 'Adult full-time and part-time employees'
        clause_description_id2 = 'Hospitality Employees'
    elif option == 'Part Time' and age == 'Adult' and u6 == 'Hospitality Employees':
        clause_description_id = 'Adult full-time and part-time employees'
        clause_description_id2 = 'Hospitality Employees'
    elif option == 'Casual' and age == 'Adult' and u6 == 'Hospitality Employees':
        clause_description_id = 'Adult casual employees'
        clause_description_id2 = 'Hospitality Employees'
    elif option == 'Full Time' and age == 'Adult' and u6 == 'Casino Gaming Employees':
        clause_description_id = 'Adult full-time and part-time casino gaming employees'
        clause_description_id2 = 'Casino Gaming Employees'
    elif option == 'Part Time' and age == 'Adult' and u6 == 'Casino Gaming Employees':
        clause_description_id = 'Adult full-time and part-time casino gaming employees'
        clause_description_id2 = 'Casino Gaming Employees'
    elif option == 'Casual' and age == 'Adult' and u6 == 'Casino Gaming Employees':
        clause_description_id = 'Adult casual casino gaming employees'
        clause_description_id2 = 'Casino Gaming Employees'
    else:
        clause_description_id = ''

    if job_filter2 != 'Null':
        output = u3['Award_Desc'].iloc[0]
    else:
        output = u2['Award_Desc'].iloc[0]
    with st.expander( "See explanation" ):
        st.write(output)

elif age == "Junior":

    clause_description_id = 'Junior employees (other than office juniors)'
    clause_description_id2 = 'Junior employees (other than office juniors)'

    #filter to remove the non Hospital employees who are not entitled to Junior awards
    k = u[u['clause_description_id2'] == 'Hospitality Employees']

    job_filter = st.selectbox( "What is your role?", pd.unique( k['Profession'] ) )
    u2 = k[k['Profession'] == job_filter]

    job_filter2 = st.selectbox( "What is your grade?", pd.unique( u2['Grade'] ) )

    if job_filter == 'Introductory level':
        f = True
    else:
        f = False
    if job_filter2 != 'Null':
        u3 = u2[u2['Grade'] == job_filter2]
        indexx = u3.index[0]  # obtain the line number of the result
        u4 = u3.at[indexx, 'Level']
        u5 = u3.at[indexx, 'Level_no']
    elif f is True:
        u4 = 'Introductory Level'
        u5 = 1.0
    else:
        u4 = 'Level 5'
        u5 = 6.0

    classification = st.selectbox(
        'What is your current age?',
        ('16 years of age and under', '17 years of age', '18 years of age', '19 years of age',
         '20 years of age') )

def data(clause_description=None):
    # this section is the default code"""
    id_or_code = 'MA000009'
    # filtering utilising the latest published year
    s2 = s[s['published_year'] == int( max( s['published_year'] ) )]
    # further filtering by the clause_description utilising the string containing the clause_description_id2
    s3 = s2[s2['clause_description'] == clause_description_id2]
    # further filtering by the parent_classification_name utilising the string containing the parent_classification_name_id
    if age == 'Junior':  # only need to filter at this level for juniors
        s4 = s3[s3['parent_classification_name'].str.contains( u4, na=False )]
    else:
        s4 = s3
    # further filtering by the classification utilising the string containing the classification
    s5 = s4[s4['classification'].str.contains( classification )]
    # obtain the result and save it against class_fixed_id"""
    class_fixed_id = (s5['classification_fixed_id'].iloc[0])


    # filtering utilising the latest published year
    t2 = t[t['published_year'] == int( max( t['published_year'] ) )]
    # further filtering by the classification_fixed_id utilising the string containing the class_fixed_id
    t3 = t2[t2['classification_fixed_id'] == class_fixed_id]
    # obtain the result and save it against base_pay_rate_id_a
    base_pay_rate_id_a = t3['base_pay_rate_id'].iloc[0]
    # filtering utilising the latest published year"""
    q2 = q[q['published_year'] == int( max( q['published_year'] ) )]
    q3 = q2[q2['base_pay_rate_id'] == base_pay_rate_id_a]
    # storing in dictionary results clause, penalty and value"""
    class_dict2 = dict(
        zip( (q3['clause_description']) + (q3['penalty_description']).str.lower(), q3['penalty_calculated_value'] ) )

    #  check for full time/part time or casual for weekend/rostered day or weekend clause specific clause
    if 'Adult full-time and part-time employees' in clause_description_id and option != 'Casual':
        dictionary( class_dict2, "Adult full-time and part-time employees", 'full' )

    elif 'Adult casual employees' in clause_description_id and option == 'Casual':
        dictionary( class_dict2, "Adult casual employees", "casual" )

    elif 'Adult full-time and part-time casino gaming employees' in clause_description_id and option != 'Casual':
        dictionary( class_dict2, "Adult full-time and part-time casino gaming employees", "full" )

    elif 'Adult casual casino gaming employees' in clause_description_id and option == 'Casual':
        dictionary( class_dict2, "Adult casual casino gaming employees", "Casual" )

    elif 'Junior employees (other than office juniors)' in clause_description_id and option != 'Casual':
        dictionary( class_dict2, "Junior full-time and part-time employees (other than junior office employees)", 'full' )

    elif 'Junior employees (other than office juniors)' in clause_description_id and option == 'Casual':
        dictionary( class_dict2, "Junior casual employees (other than junior office employees)", 'casual' )
    

def dictionary(arg1, arg2, arg3):
    try:
        hr_Ord = arg1[arg2 + "—ordinary and penalty ratesordinary hours"]
    except:
        hr_Ord = 0

    try:
        hr_OT3 = arg1[arg2 + "—overtime ratesmonday to friday - after 2 hours"]
    except:
        hr_OT3 = 0

    try:
        hr_OT02 = arg1[arg2 + "—overtime ratesmonday to friday - first 2 hours"]
    except:
        hr_OT02 = 0

    try:
        hr_Sat = arg1[arg2 + "—ordinary and penalty ratessaturday"]
    except:
        hr_Sat = 0

    try:
        hr_Sun = arg1[arg2 + "—ordinary and penalty ratessunday"]
    except:
        hr_Sun = 0

    try:
        hr_PH = arg1[arg2 + "—ordinary and penalty ratespublic holiday"]
    except:
        hr_PH = 0

    if arg3 != 'casual':
        try:
            hr_WR = arg1[arg2 + "—overtime ratesweekends and rostered days off"]
        except:
            hr_WR = 0

        try:
            hr_OTPH = arg1[arg2 + "—overtime ratespublic holiday"]
        except:
            hr_OTPH = 0

    if arg3 == 'casual':
        try:
            hr_WC = arg1[arg2 + "—overtime ratesweekends"]
        except:
            hr_WC = 0
    
    r2 = r[r['published_year'] == int( max( q['published_year'] ) )]
    wage_dict = dict( zip( r2['allowance'].str.strip(), r2['allowance_amount'] ) )
    hr_even = round( wage_dict['Penalty—Monday to Friday—7.00 pm to midnight'] + hr_Ord, 2 )
    hr_night = round( wage_dict['Penalty—Monday to Friday—midnight to 7.00 am'] + hr_Ord, 2 )
    All_Split2 = round( wage_dict['Split shift allowance—2 hours and up to 3 hours'], 2 )
    All_Split3 = round( wage_dict['Split shift allowance—More than 3 hours'], 2 )

    global saved_hr_Ord, saved_hr_even, saved_hr_night, saved_hr_Sat, saved_hr_Sun, saved_hr_PH, saved_hr_OT02, saved_hrOT3, saved_hr_OTPH
    saved_hr_Ord = hr_Ord
    saved_hr_even = hr_even
    saved_hr_night = hr_night
    saved_hr_Sat = hr_Sat
    saved_hr_Sun = hr_Sun
    saved_hr_PH = hr_PH
    saved_hr_OT02 = hr_OT02
    saved_hrOT3 = hr_OT3
    saved_hr_OTPH = hr_OTPH

if __name__ == "__main__":
    data()
    print( "----- Finished! -----" )


#Function that creates timesheet entry calculator
def timesheet():
    st.write( "## Timesheet Entry" )
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)

    if 'start_date' and 'end_date' and 'delta' and 'time_period' not in st.session_state:
        st.session_state['start_date'] = None
        st.session_state['end_date'] = None
        st.session_state['delta'] = None
        st.session_state['time_period'] = None

    try:
        st.session_state['start_date'], st.session_state['end_date'] =st.date_input('Select the time period you have worked (Start date - End date):', value = (datetime.datetime.today(), datetime.datetime.today()))
    except ValueError:
        st.error("Please select both a start date and end date.")
        return
    else:
        error_check = True

    if error_check == True:
        delta = st.session_state['end_date'] - st.session_state['start_date']
        if delta.days > 7:
            st.error('The maximum time period you may select is 7 days')    
        else:
            st.write("Select the times you have worked for each shift")
            st.session_state['time_period'] = [st.session_state['start_date']+datetime.timedelta(days=x) for x in range(((st.session_state['end_date'] + datetime.timedelta(days = 1))-st.session_state['start_date']).days)]

            #Change format of list to D-M-Y
            st.session_state['time_period'] = [datetime.datetime.strftime(date, "%d/%m/%Y") for date in st.session_state['time_period']]
            date_value_dict ={}
            end_date_dict = {}

            #Create time selector
            total_for_date = 0
            overall_total = 0
            ordinary_hours = datetime.timedelta(hours=0, minutes=0)
            for date in st.session_state['time_period']:
                date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
                st.subheader(f"{date} ({date_obj.strftime('%A')})")
                col1, col2, col3, col4= st.columns(4)
                with col1:
                    st.markdown('<div style="height: 28px;"></div>', unsafe_allow_html=True)
                    st.markdown("<span style='font-size: 20px;'>Start of shift time:</span>", unsafe_allow_html=True)
                with col2:
                    start_hours = st.selectbox(label='Hour', options=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23), key=f"{date}_start_hours")
                with col3:
                    start_mins = st.selectbox("Minute", options=(range(60)), key=f"{date}_start_minutes")
                start_time = datetime.time(start_hours, start_mins)
                with col1:
                    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
                    st.markdown("<span style='font-size: 20px;'>End of shift time:</span>", unsafe_allow_html=True)
                with col2:
                    end_hours = st.selectbox('Hour', options=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23), key=f"{date}_end_hours")
                with col3:
                    end_mins = st.selectbox("Minute", options=(range(60)), key=f"{date}_end_minutes")
                end_time = datetime.time(end_hours,end_mins)
                date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
                start_datetime = datetime.datetime.combine(date_obj, start_time)
                end_datetime = datetime.datetime.combine(date_obj, end_time)
                day_after = date_obj + datetime.timedelta(days=1)
                day_before = date_obj - datetime.timedelta(days=1)
                formatted_day_after = day_after.strftime("%d-%m-%Y")
                next_day_public_holiday = False
                #Check if they worked on this day  
                shift_check = st.checkbox('I did not work on this day.', key = f"{date}_shift_check]") 
                if shift_check == False:
                    end_date_check = st.checkbox(f'My shift finished the day after ({formatted_day_after})', key = f"{date}_end_date_check")
                    if (end_time < start_time) and end_date_check == False:
                        st.error(f'Please tick the box above if your shift ended on {formatted_day_after}. ')
                    if end_date_check == True:
                        next_day_public_holiday = st.checkbox(f'Was {formatted_day_after} a public holiday?', key = f"{date}_next_day_public_holiday_check",value = False)
                    public_holiday = st.checkbox('This day was a public holiday.', key = f"{date}_publicholiday_check")
                    end_date_dict[date] = end_date_check
                    day_before = datetime.datetime.strftime(day_before, "%d/%m/%Y")
                    if day_before in end_date_dict:
                        if end_date_dict[day_before] == True:
                            st.error(f'You indicated that your previous shift on {day_before} ended on this day ({date}). Please ensure you enter your shift details correctly.')
                        else:
                            pass                             
                # Change end time format if they finished shift day after
                    if end_date_check == True:
                        end_datetime = datetime.datetime.combine(day_after,end_time)
                end_date = end_datetime.date()

                #Calculate total hours worked 
                #Initialise variables
                time_dict = {}
                overtime_dict = {}
                ordinary_counter = 0
                night_counter = 0
                evening_counter = 0
                sunday_counter = 0
                saturday_counter = 0
                overtime_ordinary = 0
                overtime_evening = 0
                overtime_night = 0
                overtime_saturday = 0
                overtime_sunday = 0
                public_holiday_counter = 0
                overtime_night_sun_to_mon = 0
                time_interval = datetime.timedelta(minutes=1)
                time_to_midnight = datetime.timedelta(minutes=0)
                after2h_difference = datetime.timedelta(minutes=0)
                start = start_datetime
                end = end_datetime
                overtime_first_two_hr = 0
                overtime_after_two_hr = 0
                public_overtime = 0
                end_datetime = end_datetime - datetime.timedelta(minutes=30)
                public_holiday_hours = 0
                start_datetime_perm = start_datetime
                start_datetime_counter = start_datetime
                end_datetime_perm = end_datetime
                midnight_end_date = datetime.datetime.combine(end_date,datetime.time(0,0))
                start_datetime2 = start_datetime
                ot_ph_dict = {}
                shift_length = (end_datetime - start_datetime).total_seconds()/60
                if shift_check == False:
                    if end_datetime < start_datetime:
                        break
                    else:
                        #Determine whether length of shift is > 12hrs and determine when OT starts. Various cases are tested.
                        if overall_total/60 < 38 and shift_length > 720 and public_holiday == False and next_day_public_holiday == False and end_date_check == False:
                            overtime_date = start_datetime_perm + datetime.timedelta(minutes=720)
                            overtime_mins_int = (end_datetime - overtime_date).total_seconds()/60
                            if overtime_mins_int <= 120:
                                overtime_first_two_hr = overtime_mins_int
                            elif overtime_mins_int > 120:
                                overtime_first_two_hr = 120
                                first_two_hr_end = overtime_date + datetime.timedelta(minutes=120)
                                overtime_after_two_hr =  (end_datetime - first_two_hr_end).total_seconds()/60
                            end_datetime = overtime_date
                            overtime_date2 = overtime_date
                        
                        elif overall_total/60 < 38 and shift_length > 720 and public_holiday == False and next_day_public_holiday == False and end_date_check == True:
                            overtime_date = start_datetime_perm + datetime.timedelta(minutes=720)
                            overtime_mins_int = (end_datetime - overtime_date).total_seconds()/60
                            overtime_date2 = overtime_date
                            if (end_date.strftime("%A") == 'Monday' or end_date.strftime("%A") == 'Tuesday' or end_date.strftime("%A") == 'Wednesday' or end_date.strftime  ("%A") == 'Thursday' or end_date.strftime("%A") == 'Friday') and (date_obj.strftime("%A") == 'Monday' or date_obj.strftime("%A") == 'Tuesday' or date_obj.strftime("%A") == 'Wednesday' or date_obj.strftime  ("%A") == 'Thursday' or date_obj.strftime("%A") == 'Friday'):
                                if overtime_mins_int <= 120:
                                    overtime_first_two_hr = overtime_mins_int
                                elif overtime_mins_int > 120:
                                    first_two_hr_end = (overtime_date + datetime.timedelta(minutes=120))
                                    overtime_first_two_hr = 120
                                    overtime_after_two_hr = (end_datetime - first_two_hr_end).total_seconds()/60

                        elif overall_total/60 < 38 and shift_length > 720 and public_holiday == True and next_day_public_holiday == False and end_date_check == False:
                            overtime_date = start_datetime_perm + datetime.timedelta(minutes=720)
                            overtime_mins_int = (end_datetime - overtime_date).total_seconds()/60
                            end_datetime = overtime_date
                            public_overtime = overtime_mins_int
                            overtime_date2 = overtime_date
                        
                        elif overall_total/60 < 38 and shift_length > 720 and public_holiday == True and next_day_public_holiday == True and end_date_check == True:
                            overtime_date = start_datetime_perm + datetime.timedelta(minutes=720)
                            overtime_mins_int = (end_datetime - overtime_date).total_seconds()/60
                            end_datetime = overtime_date
                            public_overtime = overtime_mins_int
                            overtime_date2 = overtime_date

                        elif overall_total/60 < 38 and shift_length > 720 and public_holiday == True and next_day_public_holiday == False and end_date_check == True:
                            overtime_date = start_datetime_perm + datetime.timedelta(minutes=720)
                            overtime_mins_int = (end_datetime - overtime_date).total_seconds()/60
                            overtime_date2 = overtime_date
                            if overtime_date <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                public_overtime = (end_datetime - overtime_date).total_seconds()/60
                                if (end_date.strftime("%A") == 'Monday' or end_date.strftime("%A") == 'Tuesday' or end_date.strftime("%A") == 'Wednesday' or end_date.strftime  ("%A") == 'Thursday' or end_date.strftime("%A") == 'Friday'):
                                    if public_overtime <= 120:
                                        first_two_hour_end = overtime_date + datetime.timedelta(minutes = 120)
                                        overtime_first_two_hr = (end_datetime - datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60
                                        if first_two_hour_end <= end_datetime:
                                            overtime_after_two_hr = (end_datetime - first_two_hour_end).total_seconds()/60
                                        elif first_two_hour_end > end_datetime:
                                            overtime_after_two_hr = 0
                                    elif public_overtime > 120:
                                        overtime_after_two_hr = (end_datetime - datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60
                                elif (end_date.strftime("%A") == 'Saturday'):
                                    overtime_saturday = (end_datetime - datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60
                                elif (end_date.strftime("%A") == 'Sunday'):
                                    overtime_saturday = (end_datetime - datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60

                            elif overtime_date > datetime.datetime.combine(end_date, end_datetime(0,0)):
                                if (end_date.strftime("%A") == 'Monday' or end_date.strftime("%A") == 'Tuesday' or end_date.strftime("%A") == 'Wednesday' or end_date.strftime  ("%A") == 'Thursday' or end_date.strftime("%A") == 'Friday'):
                                    if overtime_mins_int <= 120:
                                        overtime_first_two_hr = (end_datetime - overtime_date).total_seconds()/60
                                    elif overtime_mins_int > 120:
                                        overtime_first_two_hr = 120
                                        overtime_after_two_hr = (end_datetime - overtime_date).total_seconds()/60
                                elif (end_date.strftime("%A") == 'Saturday'):
                                    overtime_saturday = (end_datetime - overtime_date).total_seconds()/60
                                elif (end_date.strftime("%A") == 'Sunday'):
                                    overtime_sunday = (end_datetime - overtime_date).total_seconds()/60

                        elif overall_total/60 < 38 and shift_length > 720 and public_holiday == False and next_day_public_holiday == True and end_date_check == True:
                            overtime_date = start_datetime_perm + datetime.timedelta(minutes=720)
                            overtime_mins_int = (end_datetime - overtime_date).total_seconds()/60
                            overtime_date2 = overtime_date
                            if overtime_date <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                public_overtime = (end_datetime - datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60
                                if (start_datetime_perm.strftime("%A") == 'Monday' or start_datetime_perm.strftime("%A") == 'Tuesday' or start_datetime_perm.strftime("%A") == 'Wednesday' or start_datetime_perm.strftime  ("%A") == 'Thursday' or start_datetime_perm.strftime("%A") == 'Friday'):
                                    if (datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date).total_seconds()/60 <= 120:
                                        overtime_first_two_hr = (datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date).total_seconds()/60
                                    elif (datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date).total_seconds()/60 > 120:
                                        overtime_first_two_hr = 120
                                        first_two_hr_end = overtime_date + datetime.timedelta(minutes = 120)
                                        overtime_after_two_hr = (datetime.datetime.combine(end_date, datetime.time(0,0)) - first_two_hr_end).total_seconds()/60
                                elif (start_datetime_perm.strftime("%A") == 'Saturday'):
                                    overtime_saturday = (datetime.datetime.combine(end_date, datetime.time(0,0))- overtime_date).total_seconds()/60
                                elif (start_datetime_perm.strftime("%A") == 'Sunday'):
                                    overtime_saturday = (datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date).total_seconds()/60

                            elif overtime_date > datetime.datetime.combine(end_date, datetime.time(0,0)):
                                public_overtime = (end_datetime - overtime_date).total_seconds()/60                                
                       
                        #Calculate ordinary, evening and night hours            
                        if overall_total/60 < 38:
                            if public_holiday == False and next_day_public_holiday == False:
                                #Check for Monday to Friday start time and end time
                                if (date_obj.strftime("%A") == 'Monday' or date_obj.strftime("%A") == 'Tuesday' or date_obj.strftime("%A") == 'Wednesday' or date_obj.strftime  ("%A") == 'Thursday' or date_obj.strftime("%A") == 'Friday') and (end_date.strftime("%A") == 'Monday' or end_date.strftime("%A") == 'Tuesday' or end_date.strftime("%A") == 'Wednesday' or end_date.strftime  ("%A") == 'Thursday' or end_date.strftime("%A") == 'Friday'):
                                    #Create dictionary containing all minutes between start and end of shift 
                                    while start_datetime_counter <= end_datetime:
                                        time_dict[start_datetime_counter] = None
                                        start_datetime_counter += time_interval
                                    #Count number of minutes between 7am - 7pm (Ordinary hours)
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine(date_obj, datetime.time(7,0)) and key <= datetime.datetime.combine(date_obj,datetime.time(19,0))) or (key >= datetime.datetime.combine(end_date, datetime.time(7,0)) and key <= datetime.datetime.combine(end_date,datetime.time(19,0))):
                                            ordinary_counter += 1
                                    if end_date_check == True and (start <= datetime.datetime.combine(date_obj, datetime.time(19,0))) and (end > datetime.datetime.combine(day_after, datetime.time(7,0))):
                                        ordinary_counter = ordinary_counter - 2
                                    elif ordinary_counter != 0:
                                        ordinary_counter = ordinary_counter - 1

                                    #Count number of minutes between 7pm - 12am
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine(date_obj, datetime.time(19,0)) and key <= datetime.datetime.combine(day_after, datetime.time(0,0))) or (key >= datetime.datetime.combine(day_after, datetime.time(19,0)) and key <= datetime.datetime.combine(day_after, datetime.time(23,59))):
                                            evening_counter += 1
                                    if end_date_check == True and end > datetime.datetime.combine(end_datetime, datetime.time(19,0)):
                                        evening_counter = evening_counter - 2
                                    elif evening_counter != 0:
                                        evening_counter = evening_counter - 1

                                    #Count number of minutes between 12-7am
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(date_obj, datetime.time(7,0))) or (key >= datetime.datetime.combine(day_after, datetime.time(0,0)) and key <= datetime.datetime.combine(day_after, datetime.time(7,0))):
                                            night_counter += 1
                                    if end_date_check == True and (start > datetime.datetime.combine(date_obj, datetime.time(0,0)) and start < datetime.datetime.combine(date_obj, datetime.time(7,0))) and (end > datetime.datetime.combine(day_after, datetime.time(0,0))):
                                        night_counter = night_counter - 2
                                    elif night_counter != 0:
                                         night_counter = night_counter - 1

                                #Calculate Weekend hours
                                elif (date_obj.strftime("%A") == 'Sunday' and end_date.strftime("%A") == 'Monday'):
                                    while start_datetime_counter <= end_datetime:
                                        time_dict[start_datetime_counter] = None
                                        start_datetime_counter += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(day_after, datetime.time(0,0)):
                                            sunday_counter += 1
                                    sunday_counter = sunday_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(end_date, datetime.time(0,0)) and key <= datetime.datetime.combine(end_date,datetime.time(7,0)):
                                            night_counter += 1
                                    if night_counter != 0:
                                        night_counter = night_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(end_date, datetime.time(7,0)) and key <= datetime.datetime.combine(end_date,datetime.time(19,0)):
                                            ordinary_counter += 1
                                    if ordinary_counter != 0:
                                        ordinary_counter = ordinary_counter - 1
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine(end_date, datetime.time(19,0)) and key <= datetime.datetime.combine(end_date, datetime.time(0,0))) or (key >= datetime.datetime.combine(end_date, datetime.time(19,0)) and key <= datetime.datetime.combine(end_date, datetime.time(23,59))):
                                            evening_counter += 1
                                    if evening_counter != 0:
                                        evening_counter = evening_counter - 1

                                elif (date_obj.strftime("%A") == 'Friday' and end_date.strftime("%A") == 'Saturday'):
                                    while start_datetime_counter <= end_datetime:
                                        time_dict[start_datetime_counter] = None
                                        start_datetime_counter += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(date_obj, datetime.time(7,0)) and key <= datetime.datetime.combine(date_obj,datetime.time(19,0)):
                                            ordinary_counter += 1
                                    if ordinary_counter != 0:
                                        ordinary_counter = ordinary_counter - 1
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine(date_obj, datetime.time(19,0)) and key <= datetime.datetime.combine(end_date, datetime.time(0,0))):
                                            evening_counter += 1
                                    if evening_counter != 0:
                                        evening_counter = evening_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(date_obj,datetime.time(7,0)):
                                            night_counter += 1
                                    if night_counter != 0:
                                        night_counter = night_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(end_date, datetime.time(0,0)) and key <= datetime.datetime.combine(end_date, datetime.time (23,50)):
                                            saturday_counter += 1
                                    saturday_counter = saturday_counter - 1

                                elif (date_obj.strftime("%A") == 'Saturday' and end_date.strftime("%A") == 'Sunday'):
                                    while start_datetime_counter <= end_datetime:
                                        time_dict[start_datetime_counter] = None
                                        start_datetime_counter += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(end_date,datetime.time(0,0)):
                                            saturday_counter += 1
                                    saturday_counter = saturday_counter - 1 
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(end_date, datetime.time(0,0)) and key <= datetime.datetime.combine(end_date,datetime.time(23,59)):  
                                            sunday_counter += 1
                                    sunday_counter = sunday_counter - 1

                                elif date_obj.strftime("%A") == 'Saturday':
                                    while start_datetime_counter <= end_datetime:
                                        time_dict[start_datetime_counter] = None
                                        start_datetime_counter += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(day_after,datetime.time(0,0)): 
                                            saturday_counter += 1
                                    saturday_counter = saturday_counter - 1

                                elif date_obj.strftime("%A") == 'Sunday':
                                    while start_datetime_counter <= end_datetime: 
                                        time_dict[start_datetime_counter] = None
                                        start_datetime_counter += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(day_after,datetime.time(0,0)): 
                                            sunday_counter += 1
                                    sunday_counter = sunday_counter - 1

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total
                           

                            #Calculate public holiday cases
                            elif (public_holiday == True and next_day_public_holiday == True and end_date_check == True):
                                while start_datetime_counter <= end_datetime:
                                    time_dict[start_datetime_counter] = None
                                    start_datetime_counter += time_interval
                                for key in time_dict:
                                    public_holiday_counter += 1
                                public_holiday_counter = public_holiday_counter - 1

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            
                            elif public_holiday == True and end_date_check == True and next_day_public_holiday == False and (end_date.strftime("%A") == 'Monday' or end_date.strftime("%A") == 'Tuesday' or end_date.strftime("%A") == 'Wednesday' or end_date.strftime("%A") == 'Thursday' or end_date.strftime("%A") == 'Friday'):
                                while start_datetime_counter <= end_datetime:
                                    time_dict[start_datetime_counter] = None
                                    start_datetime_counter += time_interval
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(day_after, datetime.time(0,0)):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(end_date, datetime.time(0,0)) and key <= datetime.datetime.combine(end_date, datetime.time(7,0)):
                                        night_counter +=1 
                                if night_counter != 0:
                                    night_counter = night_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(end_date, datetime.time(19,0)) and key >= datetime.datetime.combine(end_date, datetime.time(7,0)):
                                        ordinary_counter += 1
                                if ordinary_counter != 0:
                                    ordinary_counter = ordinary_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(end_date, datetime.time(23,59)) and key >= datetime.datetime.combine(end_date, datetime.time(19,0)):
                                        evening_counter += 1
                                if evening_counter != 0:
                                    evening_counter = evening_counter - 1

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif public_holiday == True and next_day_public_holiday == False and end_date_check == True and (end_date.strftime("%A") == 'Sunday'):
                                while start_datetime_counter <= end_datetime:
                                    time_dict[start_datetime_counter] = None
                                    start_datetime_counter += time_interval
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(day_after, datetime.time(0,0)):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        sunday_counter += 1
                                if sunday_counter != 0:
                                    sunday_counter = sunday_counter - 1

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif (public_holiday == True and next_day_public_holiday == False and end_date_check == True) and (end_date.strftime("%A") == 'Saturday'):
                                while start_datetime_counter <= end_datetime:
                                    time_dict[start_datetime_counter] = None
                                    start_datetime_counter += time_interval
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        saturday_counter += 1
                                if saturday_counter != 0:
                                    saturday_counter = saturday_counter - 1

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif public_holiday == False and next_day_public_holiday == True and end_date_check == True and (date_obj.strftime("%A") == 'Monday' or date_obj.strftime("%A") == 'Tuesday' or date_obj.strftime("%A") == 'Wednesday' or date_obj.strftime("%A") == 'Thursday' or date_obj.strftime("%A") == 'Friday'):
                                while start_datetime_counter <= end_datetime:
                                    time_dict[start_datetime_counter] = None
                                    start_datetime_counter += time_interval
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(date_obj, datetime.time(7,0)):
                                        night_counter +=1 
                                if night_counter != 0:
                                    night_counter = night_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(date_obj, datetime.time(19,0)) and key >= datetime.datetime.combine(date_obj, datetime.time(7,0)):
                                        ordinary_counter += 1
                                if ordinary_counter != 0:
                                    ordinary_counter = ordinary_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(date_obj, datetime.time(23,59)) and key >= datetime.datetime.combine(date_obj, datetime.time(19,0)):
                                        evening_counter += 1

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif public_holiday == False and next_day_public_holiday == True and end_date_check == True and (end_date.strftime("%A") == 'Saturday'):
                                while start_datetime_counter <= end_datetime:
                                    time_dict[start_datetime_counter] = None
                                    start_datetime_counter += time_interval
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(date_obj, datetime.time(7,0)):
                                        night_counter +=1 
                                if night_counter != 0:
                                    night_counter = night_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(date_obj, datetime.time(19,0)) and key >= datetime.datetime.combine(date_obj, datetime.time(7,0)):
                                        ordinary_counter += 1
                                if ordinary_counter != 0:
                                    ordinary_counter = ordinary_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(date_obj, datetime.time(23,59)) and key >= datetime.datetime.combine(date_obj, datetime.time(19,0)):
                                        evening_counter = evening_counter + 1

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif public_holiday == False and next_day_public_holiday == True and end_date_check == True and (end_date.strftime("%A") == 'Sunday'):
                                while start_datetime_counter <= end_datetime:
                                    time_dict[start_datetime_counter] = None
                                    start_datetime_counter += time_interval
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)) and key <= datetime.datetime.combine(date_obj, datetime.time(7,0)):
                                        night_counter +=1 
                                if night_counter != 0:
                                    night_counter = night_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(date_obj, datetime.time(19,0)) and key >= datetime.datetime.combine(date_obj, datetime.time(7,0)):
                                        ordinary_counter += 1
                                if ordinary_counter != 0:
                                    ordinary_counter = ordinary_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine(date_obj, datetime.time(23,59)) and key >= datetime.datetime.combine(date_obj, datetime.time(19,0)):
                                        evening_counter = evening_counter + 1

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            #Cases when shift is only on one day
                            elif public_holiday == True and end_date_check == False and next_day_public_holiday == False:
                                while start_datetime_counter <= end_datetime:
                                    time_dict[start_datetime_counter] = None
                                    start_datetime_counter += time_interval
                                for key in time_dict:
                                    if key >= datetime.datetime.combine(date_obj, datetime.time(0,0)):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                            
                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            #Calculate overtime when it goes over 38 hours during the shift.
                            if overall_total/60 >= 38 and public_holiday == False and next_day_public_holiday == False:
                                dates = list(date_value_dict.keys())
                                dates_index = dates.index(date)
                                previous_date = dates[dates_index - 1]
                                previous_total_value = date_value_dict[previous_date]['overall']
                                difference_mins = 2280 - previous_total_value
                                overtime_date = (start_datetime_perm + datetime.timedelta(minutes=difference_mins))

                                if shift_length > 720:
                                    if overtime_date >= overtime_date2:
                                        overtime_date = overtime_date2                                   
                                    elif overtime_date < overtime_date2:
                                        overtime_date = overtime_date

                                overtime_mins_int = (end_datetime_perm - overtime_date).total_seconds()/60
                                overtime_start_counter = overtime_date

                                #Calculate case for Friday into Saturday shift
                                if overtime_start_counter.strftime("%A") == 'Friday' and end_datetime.strftime("%A") == 'Saturday':
                                    #Case for when overtime starts and ends before or on midnight saturday                      
                                    if (overtime_start_counter + overtime_mins_timedelta) <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        if overtime_mins_int <= 120:
                                            overtime_first_two_hr = overtime_mins_int
                                        elif overtime_mins_int > 120:
                                            overtime_first_two_hr = 120
                                            overtime_after_two_hr = overtime_mins_int - 120

                                        #Store overtime section of shift in mins in a dict
                                        while overtime_start_counter <= end_datetime:
                                            overtime_dict[overtime_start_counter] = None
                                            overtime_start_counter += time_interval
                                        
                                        #Find ordinary hours during Friday that were considered overtime
                                        for key in overtime_dict:
                                            if ordinary_counter != 0:
                                                if key <= datetime.datetime.combine(overtime_date.date(), datetime.time(19,0)) and key >= datetime.datetime.combine(overtime_date.date(), datetime.time(7,0)):
                                                    overtime_ordinary += 1 
                                        if overtime_ordinary != 0:
                                            overtime_ordinary = overtime_ordinary - 1
                                            ordinary_counter = ordinary_counter - overtime_ordinary

                                        #Find evening hours during Friday that were considered overtime
                                        for key in overtime_dict:
                                            if evening_counter != 0:
                                                if key >= datetime.datetime.combine(overtime_date.date(), datetime.time(19,0)) and key <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                    overtime_evening += 1
                                        if overtime_evening != 0:
                                            overtime_evening = overtime_evening - 1
                                            evening_counter = evening_counter - overtime_evening

                                        #Find night hours during Friday that were considered overtime
                                        for key in overtime_dict:
                                            if night_counter != 0:
                                                if key >= datetime.datetime.combine(overtime_date.date(), datetime.time(0,0)) and key <= datetime.datetime.combine(overtime_date.date, datetime.time(7,0)):
                                                    overtime_night += 1
                                        if overtime_night != 0:
                                            overtime_night = overtime_night - 1
                                            night_counter = night_counter - overtime_night

                                    #Case for when overtime ends after midnight saturday
                                    elif (overtime_start_counter + overtime_mins_timedelta) > datetime.datetime.combine(end_date, datetime.time(0,0)):

                                        #Case for when there is less than 120 minutes of overtime before Sat midnight
                                        if (datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_start_counter).total_seconds()/60 < 120:
                                            overtime_first_two_hr = (datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_start_counter).total_seconds()/60
                                            overtime_after_two_hr = (end_datetime -  datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60

                                        #Case for when there are over or equal to 120 minutes of overtime before sat midnight
                                        else:
                                            overtime_first_two_hr = 120
                                            overtime_after_two_hr = (datetime.datetime.combine(end_date, datetime.time(0,0)) - (overtime_start_counter + datetime.timedelta(minutes=120))).total_seconds()/60
                                            overtime_after_two_hr = overtime_after_two_hr + (end_datetime -  datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60

                                        #Store overtime section of shift in mins in a dict
                                        while overtime_start_counter <= end_datetime:
                                            overtime_dict[overtime_start_counter] = None
                                            overtime_start_counter += time_interval

                                        #Find ordinary hours during Friday that were considered overtime
                                        for key in overtime_dict:
                                            if ordinary_counter != 0:
                                                if (key <= datetime.datetime.combine(overtime_date.date(), datetime.time(19,0)) and key >= datetime.datetime.combine(overtime_date.date(), datetime.time(7,0))):
                                                    overtime_ordinary += 1 
                                        if overtime_ordinary != 0:
                                            overtime_ordinary = overtime_ordinary - 1
                                            ordinary_counter = ordinary_counter - overtime_ordinary

                                        #Find evening hours during Friday that were considered overtime
                                        for key in overtime_dict:
                                            if evening_counter != 0:
                                                if (key >= datetime.datetime.combine(overtime_date.date(), datetime.time(19,0)) and key <= datetime.datetime.combine(end_date, datetime.time(0,0))):
                                                    overtime_evening += 1 
                                        if overtime_evening != 0:
                                            overtime_evening = overtime_evening - 1
                                            evening_counter = evening_counter - overtime_evening

                                        #Find night hours during Friday that were considered overtime
                                        for key in overtime_dict:
                                            if night_counter != 0:
                                                if key >= datetime.datetime.combine(overtime_date.date(), datetime.time(0,0)) and key <= datetime.datetime.combine(overtime_date.date(), datetime.time(7,0)):
                                                    overtime_night += 1
                                        if overtime_night != 0:
                                            overtime_night = overtime_night - 1
                                            night_counter = night_counter - overtime_night

                                        #Find saturday hours during saturday that were considered overtime
                                        for key in overtime_dict:
                                            if saturday_counter != 0:
                                                if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                    overtime_saturday += 1
                                        if overtime_saturday != 0:
                                            overtime_saturday = overtime_saturday - 1
                                            saturday_counter = saturday_counter  - overtime_saturday

                                #Calculate Sunday to Monday
                                elif overtime_start_counter.strftime("%A") == 'Sunday' and end_datetime.strftime("%A") == 'Monday':
                                    while overtime_start_counter <= end_datetime:
                                        overtime_dict[overtime_start_counter] = None
                                        overtime_start_counter += time_interval
                                    if end_datetime <= datetime.datetime.combine(end_date, datetime.time(0,0)):                                       
                                        #Case for when overtime ends before or on midnight Monday
                                        #Find number of minutes of overtime on sunday
                                        for key in overtime_dict:
                                            if sunday_counter != 0:
                                                    overtime_sunday += 1
                                        if overtime_sunday != 0:
                                            overtime_sunday = overtime_sunday - 1
                                            overtime_after_two_hr = overtime_sunday
                                            sunday_counter = sunday_counter - overtime_after_two_hr 
                                    
                                    elif end_datetime > datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        if datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date >= datetime.timedelta(minutes=120):
                                            for key in overtime_dict:
                                                if sunday_counter !=0:
                                                    if key <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                        overtime_sunday += 1
                                            if overtime_sunday != 0:
                                                overtime_sunday = overtime_sunday - 1
                                                overtime_after_two_hr = overtime_sunday
                                                sunday_counter = sunday_counter - overtime_sunday
                                            for key in overtime_dict:
                                                if ordinary_counter != 0: 
                                                    if key >= datetime.datetime.combine(end_date, datetime.time(7,0)) and key <= datetime.datetime.combine(end_date, datetime.time(19,0)):
                                                        overtime_ordinary += 1
                                            if overtime_ordinary != 0:
                                                overtime_ordinary = overtime_ordinary - 1
                                                overtime_after_two_hr = overtime_ordinary
                                                ordinary_counter = ordinary_counter - overtime_after_two_hr
                                            for key in overtime_dict:
                                                if night_counter != 0:
                                                    if key >= datetime.datetime.combine(end_date, datetime.time(0,0)) and key <= datetime.datetime.combine(end_date, datetime.time(7,0)):
                                                        overtime_night += 1
                                            if overtime_night != 0:
                                                overtime_night = overtime_night - 1
                                                overtime_after_two_hr = overtime_night
                                                night_counter = night_counter - overtime_after_two_hr
                                            for key in overtime_dict:
                                                if evening_counter != 0:
                                                    if key <= datetime.datetime.combine(end_date, datetime.time(23,59)) and key >= datetime.datetime.combine(end_date, datetime.time(19,0)):
                                                        evening_counter += 1
                                            if overtime_evening != 0:
                                                overtime_evening = overtime_evening - 1
                                                overtime_after_two_hr = overtime_evening
                                                evening_counter = evening_counter - overtime_after_two_hr
                                            overtime_after_two_hr = overtime_evening + overtime_ordinary + overtime_night + overtime_sunday          

                                        elif datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date < datetime.timedelta(minutes=120):
                                            time_to_midnight =  datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date
                                            after2h_difference = datetime.timedelta(minutes=120) - time_to_midnight
                                            after2h_time_start = datetime.datetime.combine(end_date, datetime.time(0,0)) + after2h_difference
                                            for key in overtime_dict:
                                                if sunday_counter != 0:
                                                    if key <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                        overtime_sunday += 1
                                            if overtime_sunday != 0:
                                                overtime_sunday = overtime_sunday - 1
                                                after2h_difference = overtime_sunday
                                                sunday_counter = sunday_counter - after2h_difference

                                            for key in overtime_dict:
                                                if night_counter != 0:
                                                    if key <= after2h_time_start and key <= datetime.datetime.combine(end_date, datetime.time(7,0)) and key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                        overtime_night += 1
                                            if overtime_night != 0:
                                                    overtime_night = overtime_night - 1
                                                    overtime_first_two_hr = overtime_night 
                                                    night_counter = night_counter - overtime_first_two_hr

                                            for key in overtime_dict:
                                                    if night_counter != 0:
                                                        if key >= after2h_time_start and key <= datetime.datetime.combine(end_date, datetime.time(7,0)):
                                                            overtime_night_sun_to_mon += 1
                                            if overtime_night_sun_to_mon != 0:
                                                    overtime_night_sun_to_mon = overtime_night_sun_to_mon - 1
                                                    overtime_after_two_hr = overtime_night_sun_to_mon
                                                    night_counter = night_counter - overtime_after_two_hr

                                            for key in overtime_dict:
                                                if ordinary_counter != 0:
                                                    if key >= datetime.datetime.combine(end_date, datetime.time(7,0)) and key <= datetime.datetime.combine(end_date, datetime.time(19,0)):
                                                        overtime_ordinary += 1
                                            if overtime_ordinary != 0:
                                                overtime_ordinary = overtime_ordinary - 1
                                                overtime_after_two_hr = overtime_ordinary
                                                ordinary_counter = ordinary_counter - overtime_after_two_hr
                                            for key in overtime_dict:
                                                if evening_counter != 0:
                                                    if key >= datetime.datetime.combine(end_date, datetime.time(19,0)) and key <= datetime.datetime.combine(end_date,datetime.time(23,59)):
                                                        overtime_evening += 1
                                            if overtime_evening != 0:
                                                overtime_evening = overtime_evening - 1
                                                overtime_after_two_hr = overtime_evening
                                                evening_counter = evening_counter - overtime_after_two_hr
                                            overtime_after_two_hr = overtime_night_sun_to_mon + overtime_sunday + overtime_ordinary + overtime_evening 
                          
                                #Calculate for Mon - Fri start and end
                                elif (overtime_date.strftime("%A") == 'Monday' or overtime_date.strftime("%A") == 'Tuesday' or overtime_date.strftime("%A") == 'Wednesday' or overtime_date.strftime("%A") == 'Thursday' or overtime_date.strftime("%A") == 'Friday') and (end_datetime.strftime("%A") == 'Monday' or end_datetime.strftime("%A") == 'Tuesday' or end_datetime.strftime("%A") == 'Tuesday' or end_datetime.strftime("%A") == 'Wednesday' or end_datetime.strftime("%A") == 'Thursday' or end_datetime.strftime("%A") == 'Friday'):

                                    if overtime_mins_int <= 120:
                                        overtime_first_two_hr = overtime_mins_int
                                    elif overtime_mins_int > 120:
                                        overtime_first_two_hr = 120
                                        overtime_after_two_hr = overtime_mins_int - 120

                                    #Store overtime section of shift in mins in a dict
                                    while overtime_start_counter <= end_datetime:
                                        overtime_dict[overtime_start_counter] = None
                                        overtime_start_counter += time_interval
                                    for key in overtime_dict:
                                        if ordinary_counter != 0:
                                            #Find ordinary hours during weekdays that were considered overtime
                                            if key <= datetime.datetime.combine(overtime_date.date(), datetime.time(19,0)) and key >= datetime.datetime.combine(overtime_date.date(), datetime.time(7,0)) or key <= datetime.datetime.combine(end_date, datetime.time(19,0)) and key >= datetime.datetime.combine(end_date, datetime.time(7,0)):
                                                overtime_ordinary += 1

                                    if overtime_ordinary != 0:
                                        overtime_ordinary = overtime_ordinary - 1
                                        ordinary_counter = ordinary_counter - overtime_ordinary

                                    for key in overtime_dict:
                                        if evening_counter != 0:
                                            #Find evening hours during weekdays that were considered overtime
                                            if key >= datetime.datetime.combine(overtime_date.date(), datetime.time(19,0)) and key <= datetime.datetime.combine(end_date, datetime.time(0,0)) or key >= datetime.datetime.combine(end_date, datetime.time(19,0)) and key <= datetime.datetime.combine(end_date, datetime.time(23,59)):
                                                overtime_evening += 1

                                    if overtime_evening != 0:
                                        overtime_evening = overtime_evening - 1
                                        evening_counter = evening_counter - overtime_evening

                                    for key in overtime_dict:
                                        if night_counter != 0:
                                            #Find night hours during Friday that were considered overtime
                                            if key >= datetime.datetime.combine(overtime_date.date(), datetime.time(0,0)) and key <= datetime.datetime.combine(overtime_date.date(), datetime.time(7,0)) or key >= datetime.datetime.combine(end_date, datetime.time(0,0)) and key <= datetime.datetime.combine(end_date, datetime.time(7,0)):
                                                overtime_night += 1

                                    if overtime_night != 0:
                                        overtime_night = overtime_night - 1
                                        night_counter = night_counter - overtime_night

                                #Calculate saturday and sunday
                                elif overtime_start_counter.strftime("%A") == 'Saturday' and end_datetime.strftime("%A") == 'Sunday':
                                    while overtime_start_counter <= end_datetime:
                                        overtime_dict[overtime_start_counter] = None
                                        overtime_start_counter += time_interval
                                    for key in overtime_dict:
                                        if saturday_counter != 0:
                                            if key <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                overtime_saturday += 1 
                                            elif key >= datetime.datetime.combine (end_date, datetime.time(0,0)):
                                                overtime_sunday += 1
                                    if overtime_saturday != 0:
                                        overtime_saturday = overtime_saturday - 1
                                        overtime_after_two_hr = overtime_saturday
                                        saturday_counter = saturday_counter - overtime_after_two_hr
                                    if overtime_sunday != 0:
                                        overtime_after_two_hr = overtime_sunday
                                        sunday_counter = sunday_counter - overtime_after_two_hr
                                    overtime_after_two_hr = overtime_saturday + overtime_sunday
                                    
                                #calculate only sunday or only saturday
                                elif overtime_start_counter.strftime("%A") == 'Saturday' or overtime_start_counter.strftime("%A") == 'Sunday':
                                    while overtime_start_counter <= end_datetime:
                                        overtime_dict[overtime_start_counter] = None
                                        overtime_start_counter += time_interval
                                    if overtime_start_counter.strftime("%A") == 'Saturday':
                                        for key in overtime_dict:
                                            if saturday_counter != 0:
                                                if key <= datetime.datetime.combine(day_after, datetime.time(0,0)):
                                                    overtime_saturday += 1
                                        if overtime_saturday != 0:
                                            overtime_saturday = overtime_saturday - 1
                                            overtime_after_two_hr = overtime_saturday
                                            saturday_counter = saturday_counter - overtime_after_two_hr
                                    elif overtime_start_counter.strftime("%A") == 'Sunday':
                                        for key in overtime_dict:
                                            if saturday_counter != 0:
                                                if key <= datetime.datetime.combine(day_after, datetime.time(0,0)):
                                                    overtime_sunday += 1
                                        if overtime_sunday != 0:
                                            overtime_sunday = overtime_sunday - 1
                                            overtime_after_two_hr = overtime_sunday
                                            sunday_counter = sunday_counter - overtime_after_two_hr

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                    #Public holiday during shift overtime
                        elif overall_total/60 >= 38 and (public_holiday == True or next_day_public_holiday == True):
                            ordinary_counter = 0
                            night_counter = 0 
                            evening_counter = 0
                            saturday_counter = 0
                            saturday_counter = 0
                            overtime_mins_int = overall_total - 2280
                            overtime_mins_timedelta = datetime.timedelta(minutes=overtime_mins_int)
                            overtime_start_counter = end_datetime - overtime_mins_timedelta
                            overtime_date = overtime_start_counter
                            first_two_hour_end = overtime_date + datetime.timedelta(minutes=120)
                            #Check if shift length > 12hrs
                            if shift_length > 720:
                                if overtime_date >= overtime_date2:
                                    overtime_date = overtime_date2                                    
                                elif overtime_date < overtime_date2:
                                    overtime_date = overtime_date

                            #Check cases for combination of possible shifts with public holidays
                            if public_holiday == True and end_date_check == False and next_day_public_holiday == False:
                                public_holiday_counter = (overtime_date - start_datetime_perm).total_seconds()/60
                                public_overtime = (end_datetime - overtime_date).total_seconds()/60

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif public_holiday == True and end_date_check == True and next_day_public_holiday == False:
                                while midnight_end_date <= overtime_date:
                                    ot_ph_dict[midnight_end_date] = None
                                    midnight_end_date += time_interval

                                if end_date.strftime("%A") == 'Monday' or end_date.strftime("%A") == 'Tuesday' or end_date.strftime("%A") == 'Wednesday' or end_date.strftime("%A") == 'Thursday' or end_date.strftime("%A") == 'Friday':
                                    if overtime_date > datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        for key in ot_ph_dict:
                                            if key <= datetime.datetime.combine(end_date,datetime.time(7,0)):
                                                night_counter = night_counter + 1
                                        for key in ot_ph_dict:
                                            if key >= datetime.datetime.combine(end_date, datetime.time(7,0)) and key <= datetime.datetime.combine(end_date, datetime.time(19,0)):
                                                ordinary_counter = ordinary_counter + 1
                                        for key in ot_ph_dict:
                                            if key >= datetime.datetime.combine(end_date, datetime.time(19,0)) and key <= datetime.datetime.combine(end_date, datetime.time(23,59)):
                                                evening_counter = evening_counter + 1
                                        if night_counter != 0:
                                            night_counter = night_counter -1
                                        if ordinary_counter != 0:
                                            ordinary_counter = ordinary_counter - 1
                                        if evening_counter != 0:
                                            evening_counter = evening_counter - 1
                                        if overtime_mins_int <= 120:
                                            overtime_first_two_hr = overtime_mins_int
                                        elif overtime_mins_int > 120:
                                            overtime_first_two_hr = 120
                                            overtime_after_two_hr = (end_datetime - overtime_date).total_seconds()/60

                                    elif overtime_date <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        if first_two_hour_end > datetime.datetime.combine(end_date,datetime.time(0,0)):                                          
                                            overtime_first_two_hr = (first_two_hour_end - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                                            public_overtime = (datetime.datetime.combine(end_date,datetime.time(0,0)) - overtime_date).total_seconds()/60
                                            if first_two_hour_end <= end_datetime:
                                                overtime_after_two_hr = (end_datetime - first_two_hour_end).total_seconds()/60
                                            elif first_two_hour_end > end_datetime:
                                                overtime_after_two_hr = 0 
                                        elif first_two_hour_end <= datetime.datetime.combine(end_date,datetime.time(0,0)):
                                            overtime_first_two_hr = 0
                                            overtime_after_two_hr = (end_datetime - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                                            public_overtime = (datetime.datetime.combine(end_date,datetime.time(0,0)) - overtime_date).total_seconds()/60
                                    
                                elif end_date.strftime("%A") == 'Saturday':
                                    if overtime_date > datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        overtime_saturday = (end_datetime - overtime_date).total_seconds()/60
                                        saturday_counter = (overtime_date - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                                    elif overtime_date <= datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        public_overtime = (datetime.datetime.combine(end_date,datetime.time(0,0)) - overtime_date).total_seconds()/60
                                        overtime_saturday = (end_datetime - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                                elif end_date.strftime("%A") == 'Sunday':
                                    if overtime_date > datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        overtime_saturday = (end_datetime - overtime_date).total_seconds()/60
                                        sunday_counter = (overtime_date - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                                    elif overtime_date <= datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        public_overtime = (datetime.datetime.combine(end_date,datetime.time(0,0)) - overtime_date).total_seconds()/60
                                        overtime_sunday = (end_datetime - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif public_holiday == False and end_date_check == True and next_day_public_holiday == True:
                                while start_datetime2 <= overtime_date:
                                    ot_ph_dict[start_datetime2] = None
                                    start_datetime2 += time_interval

                                if start_datetime_perm.strftime("%A") == 'Monday' or start_datetime_perm.strftime("%A") == 'Tuesday' or start_datetime_perm.strftime("%A") == 'Wednesday' or start_datetime_perm.strftime("%A") == 'Thursday' or start_datetime_perm.strftime("%A") == 'Friday':
                                    if overtime_date > datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        public_overtime =(end_datetime - overtime_date).total_seconds()/60
                                        public_holiday_counter = (overtime_date - midnight_end_date).total_seconds()/60
                                        for key in ot_ph_dict:
                                            if key >= datetime.datetime.combine(date_obj,datetime.time(0,0)) and key <= datetime.datetime.combine(date_obj,datetime.time(7,0)):
                                                night_counter = night_counter + 1
                                        for key in ot_ph_dict:
                                            if key >= datetime.datetime.combine(date_obj,datetime.time(7,0)) and key <= datetime.datetime.combine(date_obj,datetime.time(19,0)):
                                                ordinary_counter = ordinary_counter + 1
                                        for key in ot_ph_dict:
                                            if key >= datetime.datetime.combine(date_obj,datetime.time(7,0)) and key <= datetime.datetime.combine(end_date,datetime.time(0,0)):
                                                evening_counter = evening_counter + 1
                                        if night_counter != 0:
                                            night_counter = night_counter -1
                                        if ordinary_counter != 0:
                                            ordinary_counter = ordinary_counter - 1
                                        if evening_counter != 0:
                                            evening_counter = evening_counter - 1

                                    elif overtime_date <= datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        public_overtime = (end_datetime - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                                        if overtime_mins_int <= 120:
                                            overtime_first_two_hr = overtime_mins_int
                                        elif overtime_mins_int > 120:
                                            overtime_first_two_hr = 120
                                            overtime_after_two_hr = (datetime.datetime.combine(end_date,datetime.time(0,0)) - first_two_hour_end).total_seconds()/60
                                        for key in ot_ph_dict:
                                            if key >= datetime.datetime.combine(date_obj,datetime.time(0,0)) and key <= datetime.datetime.combine(date_obj,datetime.time(7,0)):
                                                night_counter = night_counter + 1
                                        for key in ot_ph_dict:
                                            if key >= datetime.datetime.combine(date_obj,datetime.time(7,0)) and key <= datetime.datetime.combine(date_obj,datetime.time(19,0)):
                                                ordinary_counter = ordinary_counter + 1
                                        for key in ot_ph_dict:
                                            if key >= datetime.datetime.combine(date_obj,datetime.time(7,0)) and key <= datetime.datetime.combine(end_date,datetime.time(0,0)):
                                                evening_counter = evening_counter + 1
                                        if night_counter != 0:
                                            night_counter = night_counter -1
                                        if ordinary_counter != 0:
                                            ordinary_counter = ordinary_counter - 1
                                        if evening_counter != 0:
                                            evening_counter = evening_counter - 1

                                elif start_datetime_perm.strftime("%A") == 'Saturday':
                                    if overtime_date > datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        public_overtime =(end_datetime - overtime_date).total_seconds()/60
                                        public_holiday_counter = (overtime_date - midnight_end_date).total_seconds()/60
                                        saturday_counter = (datetime.datetime.combine(end_date,datetime.time(0,0)) - start_datetime_perm).total_seconds()/60
                                    elif overtime_date <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        saturday_counter = (overtime_date - start_datetime_perm).total_seconds()/60
                                        public_overtime = (end_datetime - datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60
                                        overtime_saturday = (datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date).total_seconds()/60

                                elif start_datetime_perm.strftime("%A") == 'Sunday':
                                    if overtime_date > datetime.datetime.combine(end_date,datetime.time(0,0)):
                                        public_overtime =(end_datetime - overtime_date).total_seconds()/60
                                        public_holiday_counter = (overtime_date - midnight_end_date).total_seconds()/60
                                        sunday_counter = (datetime.datetime.combine(end_date,datetime.time(0,0)) - start_datetime_perm).total_seconds()/60
                                    elif overtime_date <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                        sunday_counter = (overtime_date - start_datetime_perm).total_seconds()/60
                                        public_overtime = (end_datetime - datetime.datetime.combine(end_date, datetime.time(0,0))).total_seconds()/60
                                        overtime_sunday = (datetime.datetime.combine(end_date, datetime.time(0,0)) - overtime_date).total_seconds()/60

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total


                            elif public_holiday == True and end_date_check == True and next_day_public_holiday == True:
                                public_overtime = (end_datetime - overtime_date).total_seconds()/60
                                public_holiday_counter = (overtime_date - start_datetime_perm).total_seconds()/60

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                        #Calculate hours when overtime threshold has already been reached                  
                        elif overall_total/60 >= 38:
                            overtime_mins_int = (end_datetime - start_datetime).total_seconds()/60
                            overtime_mins_timedelta = datetime.timedelta(minutes=overtime_mins_int)
                            overtime_start_counter = end_datetime - overtime_mins_timedelta
                            overtime_date = start_datetime
                            
                            if public_holiday == False and next_day_public_holiday == True and end_date_check == True:
                                public_overtime = (end_datetime - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                                if (start_datetime.strftime("%A") == 'Monday' or start_datetime.strftime("%A") == 'Tuesday' or start_datetime.strftime("%A") == 'Wednesday' or start_datetime.strftime("%A") == 'Thursday' or start_datetime.strftime("%A") == 'Friday'):
                                    if (datetime.datetime.combine(end_date, datetime.time(0,0)) - start_datetime).total_seconds()/60 <= 120:
                                        overtime_first_two_hr = (datetime.datetime.combine(end_date, datetime.time(0,0)) - start_datetime).total_seconds()/60
                                    elif (datetime.datetime.combine(end_date, datetime.time(0,0)) - start_datetime).total_seconds()/60 > 120:
                                        overtime_first_two_hr = 120
                                        overtime_after_two_hr = (datetime.datetime.combine(end_date, datetime.time(0,0)) - (start_datetime + datetime.timedelta(minutes=120))).total_seconds()/60
                                elif start_datetime.strftime("%A") == 'Saturday':
                                    overtime_saturday = (datetime.datetime.combine(end_date, datetime.time(0,0)) - start_datetime).total_seconds()/60
                                elif start_datetime.strftime("%A") == 'Sunday':
                                    overtime_sunday = (datetime.datetime.combine(end_date, datetime.time(0,0)) - start_datetime).total_seconds()/60
                                
                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif public_holiday == False and next_day_public_holiday == False:
                                if overtime_start_counter.strftime("%A") == 'Friday' and end_datetime.strftime("%A") == 'Saturday':
                                    if overtime_mins_int <= 120:
                                        first_two_hour_end = start_datetime + overtime_mins_timedelta

                                        while start_datetime <= end_datetime:
                                            overtime_dict[start_datetime] = None
                                            start_datetime += time_interval
                                        if first_two_hour_end <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                            overtime_first_two_hr = overtime_mins_int
                                        else:
                                            for key in overtime_dict:
                                                if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                    overtime_after_two_hr += 1
                                            overtime_after_two_hr = overtime_after_two_hr - 1
                                            overtime_first_two_hr = overtime_mins_int - overtime_after_two_hr

                                    elif overtime_mins_int > 120:
                                        after2h_time_start = start_datetime + datetime.timedelta(minutes =120)
                                        first_two_hour_end = after2h_time_start
                                        after2h_difference = end_datetime - after2h_time_start
                                        while start_datetime <= end_datetime:
                                            overtime_dict[start_datetime] = None
                                            start_datetime += time_interval
                                        for key in overtime_dict:
                                            if key >= after2h_time_start:
                                                overtime_after_two_hr += 1                                               
                                        overtime_first_two_hr = 120
                                        overtime_after_two_hr = overtime_after_two_hr - 1
                                
                                elif overtime_start_counter.strftime("%A") == 'Sunday' and end_datetime.strftime("%A") == 'Monday':
                                    if overtime_mins_int <= 120:
                                        first_two_hour_end = start_datetime + overtime_mins_timedelta
                                        while start_datetime <= end_datetime:
                                            overtime_dict[start_datetime] = None
                                            start_datetime += time_interval
                                        if first_two_hour_end <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                            overtime_after_two_hr = overtime_mins_int
                                        else:
                                            for key in overtime_dict:
                                                if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                    overtime_first_two_hr += 1
                                            overtime_first_two_hr = overtime_first_two_hr - 1
                                            overtime_after_two_hr = overtime_mins_int - overtime_first_two_hr

                                    elif overtime_mins_int > 120:
                                        after2h_time_start = start_datetime + datetime.timedelta(minutes =120)
                                        first_two_hour_end = after2h_time_start
                                        after2h_difference = end_datetime - after2h_time_start
                                        while start_datetime <= end_datetime:
                                            overtime_dict[start_datetime] = None
                                            start_datetime += time_interval
                                        for key in overtime_dict:
                                            if key <= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                overtime_after_two_hr += 1
                                        if overtime_after_two_hr != 0:
                                            overtime_after_two_hr = overtime_after_two_hr - 1
                                        if after2h_time_start == datetime.datetime.combine(end_date, datetime.time(0,0)):
                                            for key in overtime_dict:
                                                if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                    overtime_after_two_hr += 1
                                            overtime_after_two_hr = overtime_after_two_hr - 1
                                        elif after2h_time_start > datetime.datetime.combine(end_date, datetime.time(0,0)):
                                            after2h_after_midnight = first_two_hour_end -  datetime.datetime.combine(end_date, datetime.time(0,0))
                                            overtime_after_two_hr = overtime_after_two_hr + after2h_difference.total_seconds()/60
                                            overtime_first_two_hr = after2h_after_midnight.total_seconds()/60
                                        elif after2h_time_start < datetime.datetime.combine(end_date, datetime.time(0,0)):
                                            for key in overtime_dict:
                                                if key >= datetime.datetime.combine(end_date, datetime.time(0,0)):
                                                    overtime_after_two_hr += 1
                                            overtime_after_two_hr = overtime_after_two_hr - 1

                                elif overtime_start_counter.strftime("%A") == 'Saturday' and end_datetime.strftime("%A") == 'Sunday':
                                    overtime_after_two_hr = overtime_mins_int

                                elif (overtime_start_counter.strftime("%A") == 'Monday' or overtime_start_counter.strftime("%A") == 'Tuesday' or overtime_start_counter.strftime("%A") == 'Wednesday' or overtime_start_counter.strftime("%A") == 'Thursday' or overtime_start_counter.strftime("%A") == 'Friday') and (end_datetime.strftime("%A") == 'Monday' or end_datetime.strftime("%A") == 'Tuesday' or end_datetime.strftime("%A") == 'Wednesday' or end_datetime.strftime("%A") == 'Thursday' or end_datetime.strftime("%A") == 'Friday'):
                                    while start_datetime <= end_datetime:
                                        overtime_dict[start_datetime] = None
                                        start_datetime += time_interval
                                    if overtime_mins_int <= 120:
                                        overtime_first_two_hr = overtime_mins_int
                                    elif overtime_mins_int > 120:
                                        overtime_first_two_hr = 120
                                        overtime_after_two_hr = overtime_mins_int - 120
                                
                                elif overtime_start_counter.strftime("%A") == 'Saturday' or overtime_start_counter.strftime("%A") == 'Sunday':
                                    overtime_after_two_hr = overtime_mins_int

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total
                        
                            elif public_holiday == True and next_day_public_holiday == False and end_date_check == False:
                                public_overtime = overtime_mins_int

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total
                        
                            elif public_holiday == True and end_date_check == True and next_day_public_holiday == False:
                                public_holiday_hours = (datetime.datetime.combine(end_date, datetime.time(0,0)) - start_datetime).total_seconds()/60
                                if end_datetime.strftime("%A") == 'Monday' or end_datetime.strftime("%A") == 'Tuesday' or end_datetime.strftime("%A") == 'Wednesday' or end_datetime.strftime("%A") == 'Thursday' or end_datetime.strftime("%A") == 'Friday':
                                    if public_holiday_hours <= 120:
                                        public_overtime = public_holiday_hours
                                        overtime_first_two_hr = (120 - public_overtime)
                                        first_two_hour_end = (datetime.datetime.combine(end_date, datetime.time(0,0)) + datetime.timedelta(minutes=overtime_first_two_hr))
                                        overtime_after_two_hr = (end_datetime - first_two_hour_end).total_seconds()/60
                                    elif public_holiday_hours > 120:
                                        public_overtime = public_holiday_hours
                                        overtime_after_two_hr = (end_datetime - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                            
                                elif end_datetime.strftime("%A") == 'Saturday':
                                        public_overtime = public_holiday_hours
                                        overtime_saturday = (end_datetime - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
                                elif end_datetime.strftime("%A") == 'Sunday':
                                        public_overtime = public_holiday_hours
                                        overtime_sunday = (end_datetime - datetime.datetime.combine(end_date,datetime.time(0,0))).total_seconds()/60
  
                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday

                                date_value_dict[date] = {
                                'ordinary':int(ordinary_counter),
                                'night':int(night_counter),
                                'evening':int(evening_counter),
                                'sunday':int(sunday_counter),
                                'saturday':int(saturday_counter),
                                'public_holiday':int(public_holiday_counter),
                                'overtime_first2':int(overtime_first_two_hr),
                                'overtime_after2':int(overtime_after_two_hr),
                                'public_hol_overtime':int(public_overtime),
                                'overtime_sunday':int(overtime_sunday),
                                'overtime_saturday':int(overtime_saturday),
                                'total': int(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

                            elif public_holiday == True and end_date_check == True and next_day_public_holiday == True:
                                public_overtime = (end_datetime - start_datetime).total_seconds()/60
                                
                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter +overtime_first_two_hr +overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                
                                date_value_dict[date] = {
                                'ordinary':float(ordinary_counter),
                                'night':float(night_counter),
                                'evening':float(evening_counter),
                                'sunday':float(sunday_counter),
                                'saturday':float(saturday_counter),
                                'public_holiday':float(public_holiday_counter),
                                'overtime_first2':float(overtime_first_two_hr),
                                'overtime_after2':float(overtime_after_two_hr),
                                'public_hol_overtime':float(public_overtime),
                                'overtime_sunday':float(overtime_sunday),
                                'overtime_saturday':float(overtime_saturday),
                                'total': float(total_for_date),
                                }
                                overall_total = sum(item['total'] for item in date_value_dict.values())
                                date_value_dict[date]['overall'] = overall_total

        for key in date_value_dict:
            date_value_dict[key]['overtime_after2'] += date_value_dict[key]['overtime_sunday'] + date_value_dict[key]['overtime_saturday']
        
        for key in date_value_dict:
            del date_value_dict[key]['overtime_sunday']
            del date_value_dict[key]['overtime_saturday']
            del date_value_dict[key]['total']
            del date_value_dict[key]['overall']
    
        for key in date_value_dict:
            date_value_dict[key]['Ordinary Hours (7am - 7pm)'] = date_value_dict[key].pop('ordinary')
            date_value_dict[key]['Evening Hours (7pm - 12am)'] = date_value_dict[key].pop('evening')
            date_value_dict[key]['Night Hours (12am - 7am)'] = date_value_dict[key].pop('night')
            date_value_dict[key]['Saturday Hours'] = date_value_dict[key].pop('saturday')
            date_value_dict[key]['Sunday Hours'] = date_value_dict[key].pop('sunday')
            date_value_dict[key]['Overtime (First 2 hours)'] = date_value_dict[key].pop('overtime_first2')
            date_value_dict[key]['Overtime (After 2 hours)'] = date_value_dict[key].pop('overtime_after2')
            date_value_dict[key]['Public Holiday Hours'] = date_value_dict[key].pop('public_holiday')
            date_value_dict[key]['Public Holiday Overtime'] = date_value_dict[key].pop('public_hol_overtime')
        
        for key in date_value_dict:
            date_value_dict[key]['Ordinary Hours (7am - 7pm)'] = date_value_dict[key]['Ordinary Hours (7am - 7pm)']/60
            date_value_dict[key]['Evening Hours (7pm - 12am)'] = date_value_dict[key]['Evening Hours (7pm - 12am)']/60
            date_value_dict[key]['Night Hours (12am - 7am)'] =  date_value_dict[key]['Night Hours (12am - 7am)']/60
            date_value_dict[key]['Saturday Hours'] = date_value_dict[key]['Saturday Hours']/60
            date_value_dict[key]['Sunday Hours'] = date_value_dict[key]['Sunday Hours']/60
            date_value_dict[key]['Overtime (First 2 hours)'] = date_value_dict[key]['Overtime (First 2 hours)']/60
            date_value_dict[key]['Overtime (After 2 hours)'] = date_value_dict[key]['Overtime (After 2 hours)']/60
            date_value_dict[key]['Public Holiday Hours'] = date_value_dict[key]['Public Holiday Hours']/60
            date_value_dict[key]['Public Holiday Overtime'] = date_value_dict[key]['Public Holiday Overtime']/60

        for key in date_value_dict:
            date_value_dict[key]['Total'] = ''
            date_value_dict[key]['Superannuation'] = ''
        return date_value_dict


timesheet = timesheet()         

rates_dict = {
    'Ordinary Hours (7am - 7pm)': saved_hr_Ord,
    'Evening Hours (7pm - 12am)': saved_hr_even,
    'Night Hours (12am - 7am)' : saved_hr_night,
    'Saturday Hours' : saved_hr_Sat,
    'Sunday Hours' : saved_hr_Sun,
    'Overtime (First 2 hours)' : saved_hr_OT02,
    'Overtime (After 2 hours)' : saved_hrOT3,
    'Public Holiday Hours' : saved_hr_PH,
    'Public Holiday Overtime': saved_hr_OTPH,
    'Total':'',
    'Superannuation':''                                
}

timesheet['Rates'] = rates_dict

ordinary_hours_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        ordinary_hours_sum += values.get("Ordinary Hours (7am - 7pm)", 0)

evening_hour_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        evening_hour_sum += values.get("Evening Hours (7pm - 12am)", 0)

night_hour_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        night_hour_sum += values.get("Night Hours (12am - 7am)", 0)

saturday_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        saturday_sum += values.get("Saturday Hours", 0)

sunday_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        sunday_sum += values.get("Sunday Hours", 0)

overtime_first2h_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        overtime_first2h_sum += values.get("Overtime (First 2 hours)", 0)

overtime_after2h_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        overtime_after2h_sum += values.get("Overtime (After 2 hours)", 0)

public_hol_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        public_hol_sum += values.get("Public Holiday Hours", 0)

public_hol_ot_sum = 0
for key, values in timesheet.items():
    if key != "Rates":
        public_hol_ot_sum += values.get("Public Holiday Overtime", 0)


pay_dict = {
    'Ordinary Hours (7am - 7pm)': round(float(ordinary_hours_sum * saved_hr_Ord),2),
    'Evening Hours (7pm - 12am)': round(float(evening_hour_sum * saved_hr_even),2),
    'Night Hours (12am - 7am)' : round(float(night_hour_sum * saved_hr_night),2),
    'Saturday Hours' : round(float(saturday_sum * saved_hr_Sat),2),
    'Sunday Hours' : round(float(sunday_sum * saved_hr_Sun),2),
    'Overtime (First 2 hours)' : round(float(overtime_first2h_sum * saved_hr_OT02),2),
    'Overtime (After 2 hours)' : round(float(overtime_after2h_sum * saved_hrOT3),2),
    'Public Holiday Hours' : round(float(public_hol_sum * saved_hr_PH),2),
    'Public Holiday Overtime': round(float(public_hol_ot_sum * saved_hr_OTPH),2),
    'Total': round((ordinary_hours_sum * saved_hr_Ord + evening_hour_sum * saved_hr_even + night_hour_sum * saved_hr_night + saturday_sum * saved_hr_Sat + sunday_sum * saved_hr_Sun + overtime_first2h_sum * saved_hr_OT02 + overtime_after2h_sum * saved_hrOT3 + public_hol_sum * saved_hr_PH + public_hol_ot_sum * saved_hr_OTPH),2),
    'Superannuation': round((ordinary_hours_sum * saved_hr_Ord + evening_hour_sum * saved_hr_even + night_hour_sum * saved_hr_night + saturday_sum * saved_hr_Sat + sunday_sum * saved_hr_Sun + overtime_first2h_sum * saved_hr_OT02 + overtime_after2h_sum * saved_hrOT3 + public_hol_sum * saved_hr_PH + public_hol_ot_sum * saved_hr_OTPH)*0.11,2)                     

}

timesheet['Pay'] = pay_dict

check = 0
for key in timesheet.items():
    check += 1

if check > 2:
    st.subheader("Pay table")
    df = pd.DataFrame(timesheet)
    st.dataframe(df, width = 1200, height = 422)

    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    csv = convert_df(df)
    st.download_button(
    "Press to Download Table",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
    )

    with st.expander( "Issues or Concerns with your pay" ):
        st.write ('Any concern with your pay please')
        st.write ('1. Contact your employer to discuss your problem')
        st.write ('2. Contact Fair Work Ombudsman for more support through https://www.fairwork.gov.au/about-us/contact-us')    

