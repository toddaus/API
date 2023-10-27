import streamlit as st
import pandas as pd
import datetime
from API import FWCAPI

st.title( 'Timesheet' )

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta( days=1 )

if 'start_date' and 'end_date' and 'delta' and 'time_period' not in st.session_state:
    st.session_state['start_date'] = None
    st.session_state['end_date'] = None
    st.session_state['delta'] = None
    st.session_state['time_period'] = None

def timesheet():
    try:
        st.session_state['start_date'], st.session_state['end_date'] = st.date_input(
            'Select the time period you have worked (Start date - End date):',
            value=(datetime.datetime.today(), datetime.datetime.today()) )
    except ValueError:
        st.error( "Please select both a start date and end date." )
        return
    else:
        error_check = True

    if error_check == True:
        delta = st.session_state['end_date'] - st.session_state['start_date']
        if delta.days > 7:
            st.error( 'The maximum time period you may select is 7 days' )
        else:
            st.write( "Select the times you have worked for each shift" )
            st.session_state['time_period'] = [st.session_state['start_date'] + datetime.timedelta( days=x ) for x in
                                               range( ((st.session_state['end_date'] + datetime.timedelta( days=1 )) -
                                                       st.session_state['start_date']).days )]

            # Change format of list to D-M-Y
            st.session_state['time_period'] = [datetime.datetime.strftime( date, "%d/%m/%Y" ) for date in
                                               st.session_state['time_period']]

            # total = datetime.timedelta(hours = end_datetime.hour - start_time.hour, minutes = end_datetime.minute)
            # total_time_worked += total

            date_value_dict = {}
            end_date_dict = {}
            # public_holiday_date_dict = {}
            # Create time selector
            total_for_date = 0
            overall_total = 0
            ordinary_hours = datetime.timedelta( hours=0, minutes=0 )
            for date in st.session_state['time_period']:
                date_obj = datetime.datetime.strptime( date, "%d/%m/%Y" )
                st.title( f"{date} ({date_obj.strftime( '%A' )})" )
                col1, col2, col3, col4 = st.columns( 4 )
                with col1:
                    st.markdown( '<div style="height: 28px;"></div>', unsafe_allow_html=True )
                    st.markdown( "<span style='font-size: 20px;'>Start of shift time:</span>", unsafe_allow_html=True )
                with col2:
                    # start_hours = st.selectbox(f"Start of shift time on {date} (Hour):", options=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23), key=f"{date}_start_hours", help="Time 1")
                    start_hours = st.selectbox( label='Hour', options=(
                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),
                                                key=f"{date}_start_hours" )
                with col3:
                    # start_mins = st.selectbox(f"Start of shift time on {date} (Minutes):", options=(range(60)), key=f"{date}_start_minutes", help="Time 1")
                    start_mins = st.selectbox( "Minute", options=(range( 60 )), key=f"{date}_start_minutes" )
                start_time = datetime.time( start_hours, start_mins )
                with col1:
                    st.markdown( '<div style="height: 40px;"></div>', unsafe_allow_html=True )
                    st.markdown( "<span style='font-size: 20px;'>End of shift time:</span>", unsafe_allow_html=True )
                # with col3:
                #     st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
                with col2:
                    # end_hours = st.selectbox(f"End of shift time on {date} (Hour):", options=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23), key=f"{date}_end_hours", help="Time 1")
                    end_hours = st.selectbox( 'Hour', options=(
                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),
                                              key=f"{date}_end_hours" )
                with col3:
                    # end_mins = st.selectbox(f"End of shift time on {date} (Hour):", options=(range(60)), key=f"{date}_end_minutes", help="Time 1")
                    end_mins = st.selectbox( "Minute", options=(range( 60 )), key=f"{date}_end_minutes" )
                end_time = datetime.time( end_hours, end_mins )
                # with col6:
                #     st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
                # with col6:
                #     st.write(end_time)
                # Change formats for variables
                date_obj = datetime.datetime.strptime( date, "%d/%m/%Y" )
                start_datetime = datetime.datetime.combine( date_obj, start_time )
                end_datetime = datetime.datetime.combine( date_obj, end_time )
                day_after = date_obj + datetime.timedelta( days=1 )
                day_before = date_obj - datetime.timedelta( days=1 )
                formatted_day_after = day_after.strftime( "%d-%m-%Y" )
                next_day_public_holiday = False
                # day_after_str = datetime.datetime.strptime(day_after, "%Y-%m-%d %H:%M:%S")
                # formatted_day_after_str = day_after_str.strftime("%Y-%m-%d")
                # Check if they worked on this day
                shift_check = st.checkbox( 'I did not work on this day.', key=f"{date}_shift_check]" )
                if shift_check == False:
                    end_date_check = st.checkbox( f'My shift finished the day after ({formatted_day_after})',
                                                  key=f"{date}_end_date_check" )
                    if (end_time < start_time) and end_date_check == False:
                        st.error( f'Please tick the box above if your shift ended on {formatted_day_after}. ' )
                    if end_date_check == True:
                        next_day_public_holiday = st.checkbox( f'Was {formatted_day_after} a public holiday?',
                                                               key=f"{date}_next_day_public_holiday_check",
                                                               value=False )

                    # broken_shift = st.checkbox('I had a broken shift on this day.', key = f"{date}_broken_shift_check")
                    public_holiday = st.checkbox( 'This day was a public holiday.', key=f"{date}_publicholiday_check" )
                    # rostered_day_off = st.checkbox('This was a rostered day off.', key = f"{date}_rostereddayoff_check")
                    end_date_dict[date] = end_date_check
                    # st.write(end_date_dict)
                    # st.write(day_before.date())
                    day_before = datetime.datetime.strftime( day_before, "%d/%m/%Y" )
                    if day_before in end_date_dict:
                        if end_date_dict[day_before] == True:
                            st.error(
                                f'You indicated that your previous shift on {day_before} ended on this day ({date}). Please ensure you enter your shift details correctly.' )
                        else:
                            pass
                            # public_holiday_date_dict[date] = public_holiday
                    # break_length = st.slider('How long was your break', key = f"{date}_break_length")
                    break_length = datetime.timedelta( minutes=0 )
                    # Change end time format if they finished shift day after
                    if end_date_check == True:
                        end_datetime = datetime.datetime.combine( day_after, end_time )
                end_date = end_datetime.date()
                # Calculate total hours worked

                # ordinary_hours = datetime.timedelta(hours=0, minutes=0)
                # st.write(total_time_worked)
                # Show how many hours worked per day
                # st.write(total)
                # Calculate Normal day

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
                time_interval = datetime.timedelta( minutes=1 )
                time_to_midnight = datetime.timedelta( minutes=0 )
                after2h_difference = datetime.timedelta( minutes=0 )
                start = start_datetime
                end = end_datetime
                overtime_first_two_hr = 0
                overtime_after_two_hr = 0
                public_overtime = 0
                # next_day_public_holiday = False
                public_holiday_hours = 0
                start_datetime_perm = start_datetime
                midnight_end_date = datetime.datetime.combine( end_date, datetime.time( 0, 0 ) )
                start_datetime2 = start_datetime
                ot_ph_dict = {}

                if shift_check == False:
                    if end_datetime < start_datetime:
                        break
                    else:
                        if overall_total / 60 < 38:
                            # if broken_shift == False and rostered_day_off == False and public_holiday == False:
                            if public_holiday == False and next_day_public_holiday == False:
                                # Check for Monday to Friday start time and end time
                                if (date_obj.strftime( "%A" ) == 'Monday' or date_obj.strftime(
                                        "%A" ) == 'Tuesday' or date_obj.strftime(
                                        "%A" ) == 'Wednesday' or date_obj.strftime(
                                        "%A" ) == 'Thursday' or date_obj.strftime( "%A" ) == 'Friday') and (
                                        end_date.strftime( "%A" ) == 'Monday' or end_date.strftime(
                                        "%A" ) == 'Tuesday' or end_date.strftime(
                                        "%A" ) == 'Wednesday' or end_date.strftime(
                                        "%A" ) == 'Thursday' or end_date.strftime( "%A" ) == 'Friday'):
                                    # Create dictionary containing all minutes between start and end of shift
                                    while start_datetime <= end_datetime:
                                        time_dict[start_datetime] = None
                                        start_datetime += time_interval
                                    # Count number of minutes between 7am - 7pm (Ordinary hours)
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine( date_obj, datetime.time( 7,
                                                                                                       0 ) ) and key <= datetime.datetime.combine(
                                                date_obj, datetime.time( 19, 0 ) )) or (
                                                key >= datetime.datetime.combine( end_date, datetime.time( 7,
                                                                                                           0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 19, 0 ) )):
                                            ordinary_counter += 1
                                    if start <= datetime.datetime.combine( date_obj, datetime.time( 19,
                                                                                                    0 ) ) and end >= datetime.datetime.combine(
                                            day_after, datetime.time( 7, 0 ) ):
                                        ordinary_counter = ordinary_counter - 2
                                    elif ordinary_counter != 0:
                                        ordinary_counter = ordinary_counter - 1
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine( date_obj, datetime.time( 19,
                                                                                                       0 ) ) and key <= datetime.datetime.combine(
                                                day_after, datetime.time( 0, 0 ) )) or (
                                                key >= datetime.datetime.combine( day_after, datetime.time( 19,
                                                                                                            0 ) ) and key <= datetime.datetime.combine(
                                                day_after, datetime.time( 23, 59 ) )):
                                            evening_counter += 1
                                    if end >= datetime.datetime.combine( day_after, datetime.time( 19, 0 ) ):
                                        evening_counter = evening_counter - 2
                                    elif evening_counter != 0:
                                        evening_counter = evening_counter - 1
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                       0 ) ) and key <= datetime.datetime.combine(
                                                date_obj, datetime.time( 7, 0 ) )) or (
                                                key >= datetime.datetime.combine( day_after, datetime.time( 0,
                                                                                                            0 ) ) and key <= datetime.datetime.combine(
                                                day_after, datetime.time( 7, 0 ) )):
                                            night_counter += 1
                                    if (start >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                     0 ) ) and start <= datetime.datetime.combine(
                                            date_obj, datetime.time( 7, 0 ) )) and (
                                            end >= datetime.datetime.combine( day_after, datetime.time( 0, 0 ) )):
                                        night_counter = night_counter - 2
                                    elif night_counter != 0:
                                        night_counter = night_counter - 1

                                # # Calculate Weekend hours
                                elif (date_obj.strftime( "%A" ) == 'Sunday' and end_date.strftime( "%A" ) == 'Monday'):
                                    while start_datetime <= end_datetime:
                                        time_dict[start_datetime] = None
                                        start_datetime += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                day_after, datetime.time( 0, 0 ) ):
                                            sunday_counter += 1
                                    sunday_counter = sunday_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 7, 0 ) ):
                                            night_counter += 1
                                    if night_counter != 0:
                                        night_counter = night_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( end_date, datetime.time( 7,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 19, 0 ) ):
                                            ordinary_counter += 1
                                    if ordinary_counter != 0:
                                        ordinary_counter = ordinary_counter - 1
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine( end_date, datetime.time( 19,
                                                                                                       0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 0, 0 ) )) or (
                                                key >= datetime.datetime.combine( end_date, datetime.time( 19,
                                                                                                           0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 23, 59 ) )):
                                            evening_counter += 1
                                    if evening_counter != 0:
                                        evening_counter = evening_counter - 1
                                elif (date_obj.strftime( "%A" ) == 'Friday' and end_date.strftime(
                                        "%A" ) == 'Saturday'):
                                    while start_datetime <= end_datetime:
                                        time_dict[start_datetime] = None
                                        start_datetime += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( date_obj, datetime.time( 7,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                date_obj, datetime.time( 19, 0 ) ):
                                            ordinary_counter += 1
                                    if ordinary_counter != 0:
                                        ordinary_counter = ordinary_counter - 1
                                    for key in time_dict:
                                        if (key >= datetime.datetime.combine( date_obj, datetime.time( 19,
                                                                                                       0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 0, 0 ) )):
                                            evening_counter += 1
                                    if evening_counter != 0:
                                        evening_counter = evening_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                date_obj, datetime.time( 7, 0 ) ):
                                            night_counter += 1
                                    if night_counter != 0:
                                        night_counter = night_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 23, 50 ) ):
                                            saturday_counter += 1
                                    saturday_counter = saturday_counter - 1
                                elif (date_obj.strftime( "%A" ) == 'Saturday' and end_date.strftime(
                                        "%A" ) == 'Sunday'):
                                    while start_datetime <= end_datetime:
                                        time_dict[start_datetime] = None
                                        start_datetime += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 0, 0 ) ):
                                            saturday_counter += 1
                                    saturday_counter = saturday_counter - 1
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                end_date, datetime.time( 23, 59 ) ):
                                            sunday_counter += 1
                                    sunday_counter = sunday_counter - 1
                                elif date_obj.strftime( "%A" ) == 'Saturday':
                                    while start_datetime <= end_datetime:
                                        time_dict[start_datetime] = None
                                        start_datetime += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                day_after, datetime.time( 0, 0 ) ):
                                            saturday_counter += 1
                                    saturday_counter = saturday_counter - 1
                                elif date_obj.strftime( "%A" ) == 'Sunday':
                                    while start_datetime <= end_datetime:
                                        time_dict[start_datetime] = None
                                        start_datetime += time_interval
                                    for key in time_dict:
                                        if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                day_after, datetime.time( 0, 0 ) ):
                                            sunday_counter += 1
                                    sunday_counter = sunday_counter - 1



                            # Public holiday - check when shift ends next day
                            elif (
                                    public_holiday == True and next_day_public_holiday == True and end_date_check == True):
                                while start_datetime <= end_datetime:
                                    time_dict[start_datetime] = None
                                    start_datetime += time_interval
                                for key in time_dict:
                                    public_holiday_counter += 1
                                public_holiday_counter = public_holiday_counter - 1

                            elif public_holiday == True and end_date_check == True and next_day_public_holiday == False and (
                                    end_date.strftime( "%A" ) == 'Monday' or end_date.strftime(
                                    "%A" ) == 'Tuesday' or end_date.strftime(
                                    "%A" ) == 'Wednesday' or end_date.strftime(
                                    "%A" ) == 'Thursday' or end_date.strftime( "%A" ) == 'Friday'):
                                while start_datetime <= end_datetime:
                                    time_dict[start_datetime] = None
                                    start_datetime += time_interval
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( day_after, datetime.time( 0, 0 ) ):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                  0 ) ) and key <= datetime.datetime.combine(
                                            end_date, datetime.time( 7, 0 ) ):
                                        night_counter += 1
                                if night_counter != 0:
                                    night_counter = night_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( end_date, datetime.time( 19,
                                                                                                  0 ) ) and key >= datetime.datetime.combine(
                                            end_date, datetime.time( 7, 0 ) ):
                                        ordinary_counter += 1
                                if ordinary_counter != 0:
                                    ordinary_counter = ordinary_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( end_date, datetime.time( 23,
                                                                                                  59 ) ) and key >= datetime.datetime.combine(
                                            end_date, datetime.time( 19, 0 ) ):
                                        evening_counter += 1
                                if evening_counter != 0:
                                    evening_counter = evening_counter - 1

                            elif public_holiday == True and next_day_public_holiday == False and end_date_check == True and (
                                    end_date.strftime( "%A" ) == 'Sunday'):
                                while start_datetime <= end_datetime:
                                    time_dict[start_datetime] = None
                                    start_datetime += time_interval
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( day_after, datetime.time( 0, 0 ) ):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                        sunday_counter += 1
                                if sunday_counter != 0:
                                    sunday_counter = sunday_counter - 1



                            elif (
                                    public_holiday == True and next_day_public_holiday == False and end_date_check == True) and (
                                    end_date.strftime( "%A" ) == 'Saturday'):
                                while start_datetime <= end_datetime:
                                    time_dict[start_datetime] = None
                                    start_datetime += time_interval
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                        saturday_counter += 1
                                if saturday_counter != 0:
                                    saturday_counter = saturday_counter - 1



                            elif public_holiday == False and next_day_public_holiday == True and end_date_check == True and (
                                    date_obj.strftime( "%A" ) == 'Monday' or date_obj.strftime(
                                    "%A" ) == 'Tuesday' or date_obj.strftime(
                                    "%A" ) == 'Wednesday' or date_obj.strftime(
                                    "%A" ) == 'Thursday' or date_obj.strftime( "%A" ) == 'Friday'):
                                while start_datetime <= end_datetime:
                                    time_dict[start_datetime] = None
                                    start_datetime += time_interval
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                  0 ) ) and key <= datetime.datetime.combine(
                                            date_obj, datetime.time( 7, 0 ) ):
                                        night_counter += 1
                                if night_counter != 0:
                                    night_counter = night_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( date_obj, datetime.time( 19,
                                                                                                  0 ) ) and key >= datetime.datetime.combine(
                                            date_obj, datetime.time( 7, 0 ) ):
                                        ordinary_counter += 1
                                if ordinary_counter != 0:
                                    ordinary_counter = ordinary_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( date_obj, datetime.time( 23,
                                                                                                  59 ) ) and key >= datetime.datetime.combine(
                                            date_obj, datetime.time( 19, 0 ) ):
                                        evening_counter += 1

                            elif public_holiday == False and next_day_public_holiday == True and end_date_check == True and (
                                    end_date.strftime( "%A" ) == 'Saturday'):
                                while start_datetime <= end_datetime:
                                    time_dict[start_datetime] = None
                                    start_datetime += time_interval
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                  0 ) ) and key <= datetime.datetime.combine(
                                            date_obj, datetime.time( 7, 0 ) ):
                                        night_counter += 1
                                if night_counter != 0:
                                    night_counter = night_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( date_obj, datetime.time( 19,
                                                                                                  0 ) ) and key >= datetime.datetime.combine(
                                            date_obj, datetime.time( 7, 0 ) ):
                                        ordinary_counter += 1
                                if ordinary_counter != 0:
                                    ordinary_counter = ordinary_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( date_obj, datetime.time( 23,
                                                                                                  59 ) ) and key >= datetime.datetime.combine(
                                            date_obj, datetime.time( 19, 0 ) ):
                                        evening_counter = evening_counter + 1

                            elif public_holiday == False and next_day_public_holiday == True and end_date_check == True and (
                                    end_date.strftime( "%A" ) == 'Sunday'):
                                while start_datetime <= end_datetime:
                                    time_dict[start_datetime] = None
                                    start_datetime += time_interval
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                  0 ) ) and key <= datetime.datetime.combine(
                                            date_obj, datetime.time( 7, 0 ) ):
                                        night_counter += 1
                                if night_counter != 0:
                                    night_counter = night_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( date_obj, datetime.time( 19,
                                                                                                  0 ) ) and key >= datetime.datetime.combine(
                                            date_obj, datetime.time( 7, 0 ) ):
                                        ordinary_counter += 1
                                if ordinary_counter != 0:
                                    ordinary_counter = ordinary_counter - 1
                                for key in time_dict:
                                    if key <= datetime.datetime.combine( date_obj, datetime.time( 23,
                                                                                                  59 ) ) and key >= datetime.datetime.combine(
                                            date_obj, datetime.time( 19, 0 ) ):
                                        evening_counter = evening_counter + 1

                            # Cases when shift is only on one day
                            elif public_holiday == True and end_date_check == False and next_day_public_holiday == False:
                                while start_datetime <= end_datetime:
                                    time_dict[start_datetime] = None
                                    start_datetime += time_interval
                                for key in time_dict:
                                    if key >= datetime.datetime.combine( date_obj, datetime.time( 0, 0 ) ):
                                        public_holiday_counter += 1
                                if public_holiday_counter != 0:
                                    public_holiday_counter = public_holiday_counter - 1

                            total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr + public_overtime + overtime_sunday + overtime_saturday
                            date_value_dict[date] = {
                                'ordinary': int( ordinary_counter ),
                                'night': int( night_counter ),
                                'evening': int( evening_counter ),
                                'sunday': int( sunday_counter ),
                                'saturday': int( saturday_counter ),
                                'public_holiday': int( public_holiday_counter ),
                                'overtime_first2': int( overtime_first_two_hr ),
                                'overtime_after2': int( overtime_after_two_hr ),
                                'public_hol_overtime': int( public_overtime ),
                                'overtime_sunday': int( overtime_sunday ),
                                'overtime_saturday': int( overtime_saturday ),
                                'total': int( total_for_date ),
                            }

                            overall_total = sum( item['total'] for item in date_value_dict.values() )
                            date_value_dict[date]['overall'] = overall_total

                            st.write( 'ordinary', ordinary_counter )
                            st.write( 'evening', evening_counter )
                            st.write( 'night', night_counter )
                            st.write( 'sunday', sunday_counter )
                            st.write( 'saturday', saturday_counter )
                            st.write( 'publicholiday', public_holiday_counter )
                            st.write( 'overall', overall_total )

                            # Calculate overtime when it goes over 38 hours during the shift.
                            if overall_total / 60 >= 38 and public_holiday == False and next_day_public_holiday == False:
                                overtime_mins_int = overall_total - 2280
                                overtime_mins_timedelta = datetime.timedelta( minutes=overtime_mins_int )
                                overtime_start_counter = end_datetime - overtime_mins_timedelta
                                overtime_date = overtime_start_counter
                                # if overtime_start_counter.date() != end_datetime.date():
                                # Calculate case for Friday into Saturday shift
                                if overtime_start_counter.strftime( "%A" ) == 'Friday' and end_datetime.strftime(
                                        "%A" ) == 'Saturday':
                                    # Case for when overtime starts and ends before or on midnight saturday
                                    if (overtime_start_counter + overtime_mins_timedelta) <= datetime.datetime.combine(
                                            end_date, datetime.time( 0, 0 ) ):
                                        if overtime_mins_int <= 120:
                                            overtime_first_two_hr = overtime_mins_int
                                        elif overtime_mins_int > 120:
                                            overtime_first_two_hr = 120
                                            overtime_after_two_hr = overtime_mins_int - 120
                                        # Store overtime section of shift in mins in a dict
                                        while overtime_start_counter <= end_datetime:
                                            overtime_dict[overtime_start_counter] = None
                                            overtime_start_counter += time_interval
                                        for key in overtime_dict:
                                            if ordinary_counter != 0:
                                                # Find ordinary hours during Friday that were considered overtime
                                                if key <= datetime.datetime.combine( overtime_date.date(),
                                                                                     datetime.time( 19,
                                                                                                    0 ) ) and key >= datetime.datetime.combine(
                                                        overtime_date.date(), datetime.time( 7, 0 ) ):
                                                    overtime_ordinary += 1
                                        if overtime_ordinary != 0:
                                            overtime_ordinary = overtime_ordinary - 1
                                            ordinary_counter = ordinary_counter - overtime_ordinary
                                        for key in overtime_dict:
                                            if evening_counter != 0:
                                                # Find evening hours during Friday that were considered overtime
                                                if key >= datetime.datetime.combine( overtime_date.date(),
                                                                                     datetime.time( 19,
                                                                                                    0 ) ) and key <= datetime.datetime.combine(
                                                        end_date, datetime.time( 0, 0 ) ):
                                                    overtime_evening += 1
                                        if overtime_evening != 0:
                                            overtime_evening = overtime_evening - 1
                                            evening_counter = evening_counter - overtime_evening
                                        for key in overtime_dict:
                                            if night_counter != 0:
                                                # Find night hours during Friday that were considered overtime
                                                if key >= datetime.datetime.combine( overtime_date.date(),
                                                                                     datetime.time( 0,
                                                                                                    0 ) ) and key <= datetime.datetime.combine(
                                                        overtime_date.date, datetime.time( 7, 0 ) ):
                                                    overtime_night += 1
                                        if overtime_night != 0:
                                            overtime_night = overtime_night - 1
                                            night_counter = night_counter - overtime_night


                                    # Case for when overtime ends after midnight saturday
                                    elif (overtime_start_counter + overtime_mins_timedelta) > datetime.datetime.combine(
                                            end_date, datetime.time( 0, 0 ) ):
                                        # Case for when there is less than 120 minutes of overtime before Sat midnight
                                        if (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                0 ) ) - overtime_start_counter).total_seconds() / 60 < 120:
                                            overtime_first_two_hr = (datetime.datetime.combine( end_date,
                                                                                                datetime.time( 0,
                                                                                                               0 ) ) - overtime_start_counter).total_seconds() / 60
                                            overtime_after_two_hr = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                               datetime.time(
                                                                                                                   0,
                                                                                                                   0 ) )).total_seconds() / 60
                                        # Case for when there are over or equal to 120 minutes of overtime before sat midnight
                                        else:
                                            overtime_first_two_hr = 120
                                            overtime_after_two_hr = (datetime.datetime.combine( end_date,
                                                                                                datetime.time( 0,
                                                                                                               0 ) ) - (
                                                                                 overtime_start_counter + datetime.timedelta(
                                                                             minutes=120 ))).total_seconds() / 60
                                            overtime_after_two_hr = overtime_after_two_hr + (
                                                        end_datetime - datetime.datetime.combine( end_date,
                                                                                                  datetime.time( 0,
                                                                                                                 0 ) )).total_seconds() / 60
                                        # Store overtime section of shift in mins in a dict
                                        while overtime_start_counter <= end_datetime:
                                            overtime_dict[overtime_start_counter] = None
                                            overtime_start_counter += time_interval
                                        for key in overtime_dict:
                                            if ordinary_counter != 0:
                                                # Find ordinary hours during Friday that were considered overtime
                                                if (key <= datetime.datetime.combine( overtime_date.date(),
                                                                                      datetime.time( 19,
                                                                                                     0 ) ) and key >= datetime.datetime.combine(
                                                        overtime_date.date(), datetime.time( 7, 0 ) )):
                                                    overtime_ordinary += 1
                                        if overtime_ordinary != 0:
                                            overtime_ordinary = overtime_ordinary - 1
                                            ordinary_counter = ordinary_counter - overtime_ordinary
                                        for key in overtime_dict:
                                            if evening_counter != 0:
                                                # Find evening hours during Friday that were considered overtime
                                                if (key >= datetime.datetime.combine( overtime_date.date(),
                                                                                      datetime.time( 19,
                                                                                                     0 ) ) and key <= datetime.datetime.combine(
                                                        end_date, datetime.time( 0, 0 ) )):
                                                    overtime_evening += 1
                                        if overtime_evening != 0:
                                            overtime_evening = overtime_evening - 1
                                            evening_counter = evening_counter - overtime_evening
                                        for key in overtime_dict:
                                            if night_counter != 0:
                                                # Find night hours during Friday that were considered overtime
                                                if key >= datetime.datetime.combine( overtime_date.date(),
                                                                                     datetime.time( 0,
                                                                                                    0 ) ) and key <= datetime.datetime.combine(
                                                        overtime_date.date(), datetime.time( 7, 0 ) ):
                                                    overtime_night += 1
                                        if overtime_night != 0:
                                            overtime_night = overtime_night - 1
                                            night_counter = night_counter - overtime_night
                                        for key in overtime_dict:
                                            if saturday_counter != 0:
                                                # Find saturday hours during saturday that were considered overtime
                                                if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                                    overtime_saturday += 1
                                        if overtime_saturday != 0:
                                            overtime_saturday = overtime_saturday - 1
                                            saturday_counter = saturday_counter - overtime_saturday






                                # Calculate Sunday to Monday
                                elif overtime_start_counter.strftime( "%A" ) == 'Sunday' and end_datetime.strftime(
                                        "%A" ) == 'Monday':
                                    while overtime_start_counter <= end_datetime:
                                        overtime_dict[overtime_start_counter] = None
                                        overtime_start_counter += time_interval
                                    if end_datetime <= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                        # Case for when overtime ends before or on midnight Monday
                                        for key in overtime_dict:
                                            if sunday_counter != 0:
                                                # Find number of minutes of overtime on sunday
                                                overtime_sunday += 1
                                        if overtime_sunday != 0:
                                            overtime_sunday = overtime_sunday - 1
                                            overtime_after_two_hr = overtime_sunday
                                            sunday_counter = sunday_counter - overtime_after_two_hr

                                    elif end_datetime > datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                        if datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                               0 ) ) - overtime_date >= datetime.timedelta(
                                                minutes=120 ):
                                            for key in overtime_dict:
                                                if sunday_counter != 0:
                                                    if key <= datetime.datetime.combine( end_date,
                                                                                         datetime.time( 0, 0 ) ):
                                                        overtime_sunday += 1
                                            if overtime_sunday != 0:
                                                overtime_sunday = overtime_sunday - 1
                                                overtime_after_two_hr = overtime_sunday
                                                sunday_counter = sunday_counter - overtime_sunday
                                            for key in overtime_dict:
                                                if ordinary_counter != 0:
                                                    if key >= datetime.datetime.combine( end_date, datetime.time( 7,
                                                                                                                  0 ) ) and key <= datetime.datetime.combine(
                                                            end_date, datetime.time( 19, 0 ) ):
                                                        overtime_ordinary += 1
                                            if overtime_ordinary != 0:
                                                overtime_ordinary = overtime_ordinary - 1
                                                overtime_after_two_hr = overtime_ordinary
                                                ordinary_counter = ordinary_counter - overtime_after_two_hr
                                            for key in overtime_dict:
                                                if night_counter != 0:
                                                    if key >= datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                  0 ) ) and key <= datetime.datetime.combine(
                                                            end_date, datetime.time( 7, 0 ) ):
                                                        overtime_night += 1
                                            if overtime_night != 0:
                                                overtime_night = overtime_night - 1
                                                overtime_after_two_hr = overtime_night
                                                night_counter = night_counter - overtime_after_two_hr
                                            for key in overtime_dict:
                                                if evening_counter != 0:
                                                    if key <= datetime.datetime.combine( end_date, datetime.time( 23,
                                                                                                                  59 ) ) and key >= datetime.datetime.combine(
                                                            end_date, datetime.time( 19, 0 ) ):
                                                        evening_counter += 1
                                            if overtime_evening != 0:
                                                overtime_evening = overtime_evening - 1
                                                overtime_after_two_hr = overtime_evening
                                                evening_counter = evening_counter - overtime_after_two_hr
                                            overtime_after_two_hr = overtime_evening + overtime_ordinary + overtime_night + overtime_sunday

                                        elif datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                 0 ) ) - overtime_date < datetime.timedelta(
                                                minutes=120 ):
                                            time_to_midnight = datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                   0 ) ) - overtime_date
                                            after2h_difference = datetime.timedelta( minutes=120 ) - time_to_midnight
                                            after2h_time_start = datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                     0 ) ) + after2h_difference
                                            for key in overtime_dict:
                                                if sunday_counter != 0:
                                                    if key <= datetime.datetime.combine( end_date,
                                                                                         datetime.time( 0, 0 ) ):
                                                        overtime_sunday += 1
                                            if overtime_sunday != 0:
                                                overtime_sunday = overtime_sunday - 1
                                                after2h_difference = overtime_sunday
                                                sunday_counter = sunday_counter - after2h_difference

                                            for key in overtime_dict:
                                                if night_counter != 0:
                                                    if key <= after2h_time_start and key <= datetime.datetime.combine(
                                                            end_date, datetime.time( 7,
                                                                                     0 ) ) and key >= datetime.datetime.combine(
                                                            end_date, datetime.time( 0, 0 ) ):
                                                        overtime_night += 1
                                            if overtime_night != 0:
                                                overtime_night = overtime_night - 1
                                                overtime_first_two_hr = overtime_night
                                                night_counter = night_counter - overtime_first_two_hr

                                            for key in overtime_dict:
                                                if night_counter != 0:
                                                    if key >= after2h_time_start and key <= datetime.datetime.combine(
                                                            end_date, datetime.time( 7, 0 ) ):
                                                        overtime_night_sun_to_mon += 1
                                            if overtime_night_sun_to_mon != 0:
                                                overtime_night_sun_to_mon = overtime_night_sun_to_mon - 1
                                                overtime_after_two_hr = overtime_night_sun_to_mon
                                                night_counter = night_counter - overtime_after_two_hr

                                            for key in overtime_dict:
                                                if ordinary_counter != 0:
                                                    if key >= datetime.datetime.combine( end_date, datetime.time( 7,
                                                                                                                  0 ) ) and key <= datetime.datetime.combine(
                                                            end_date, datetime.time( 19, 0 ) ):
                                                        overtime_ordinary += 1
                                            if overtime_ordinary != 0:
                                                overtime_ordinary = overtime_ordinary - 1
                                                overtime_after_two_hr = overtime_ordinary
                                                ordinary_counter = ordinary_counter - overtime_after_two_hr
                                            for key in overtime_dict:
                                                if evening_counter != 0:
                                                    if key >= datetime.datetime.combine( end_date, datetime.time( 19,
                                                                                                                  0 ) ) and key <= datetime.datetime.combine(
                                                            end_date, datetime.time( 23, 59 ) ):
                                                        overtime_evening += 1
                                            if overtime_evening != 0:
                                                overtime_evening = overtime_evening - 1
                                                overtime_after_two_hr = overtime_evening
                                                evening_counter = evening_counter - overtime_after_two_hr
                                            overtime_after_two_hr = overtime_night_sun_to_mon + overtime_sunday + overtime_ordinary + overtime_evening

                                            # Calculate for Mon - Fri end
                                elif (overtime_date.strftime( "%A" ) == 'Monday' or overtime_date.strftime(
                                        "%A" ) == 'Tuesday' or overtime_date.strftime(
                                        "%A" ) == 'Wednesday' or overtime_date.strftime(
                                        "%A" ) == 'Thursday' or overtime_date.strftime( "%A" ) == 'Friday') and (
                                        end_datetime.strftime( "%A" ) == 'Monday' or end_datetime.strftime(
                                        "%A" ) == 'Tuesday' or end_datetime.strftime(
                                        "%A" ) == 'Tuesday' or end_datetime.strftime(
                                        "%A" ) == 'Wednesday' or end_datetime.strftime(
                                        "%A" ) == 'Thursday' or end_datetime.strftime( "%A" ) == 'Friday'):
                                    if overtime_mins_int <= 120:
                                        overtime_first_two_hr = overtime_mins_int
                                    elif overtime_mins_int > 120:
                                        overtime_first_two_hr = 120
                                        overtime_after_two_hr = overtime_mins_int - 120
                                    # Store overtime section of shift in mins in a dict
                                    while overtime_start_counter <= end_datetime:
                                        overtime_dict[overtime_start_counter] = None
                                        overtime_start_counter += time_interval
                                    for key in overtime_dict:
                                        if ordinary_counter != 0:
                                            # Find ordinary hours during weekdays that were considered overtime
                                            if key <= datetime.datetime.combine( overtime_date.date(),
                                                                                 datetime.time( 19,
                                                                                                0 ) ) and key >= datetime.datetime.combine(
                                                    overtime_date.date(),
                                                    datetime.time( 7, 0 ) ) or key <= datetime.datetime.combine(
                                                    end_date,
                                                    datetime.time( 19, 0 ) ) and key >= datetime.datetime.combine(
                                                    end_date, datetime.time( 7, 0 ) ):
                                                overtime_ordinary += 1
                                    if overtime_date <= datetime.datetime.combine( overtime_date, datetime.time( 19,
                                                                                                                 0 ) ) and end_datetime >= datetime.datetime.combine(
                                            day_after, datetime.time( 7, 0 ) ):
                                        overtime_ordinary = overtime_ordinary - 2
                                        ordinary_counter = ordinary_counter - overtime_ordinary
                                    elif overtime_ordinary != 0:
                                        overtime_ordinary = overtime_ordinary - 1
                                        ordinary_counter = ordinary_counter - overtime_ordinary
                                    for key in overtime_dict:
                                        if evening_counter != 0:
                                            # Find evening hours during weekdays that were considered overtime
                                            if key >= datetime.datetime.combine( overtime_date.date(),
                                                                                 datetime.time( 19,
                                                                                                0 ) ) and key <= datetime.datetime.combine(
                                                    end_date,
                                                    datetime.time( 0, 0 ) ) or key >= datetime.datetime.combine(
                                                    end_date,
                                                    datetime.time( 19, 0 ) ) and key <= datetime.datetime.combine(
                                                    end_date, datetime.time( 23, 59 ) ):
                                                overtime_evening += 1
                                    if end_datetime >= datetime.datetime.combine( day_after, datetime.time( 19, 0 ) ):
                                        overtime_evening = overtime_evening - 2
                                        evening_counter = evening_counter - overtime_evening
                                    elif overtime_evening != 0:
                                        overtime_evening = overtime_evening - 1
                                        evening_counter = evening_counter - overtime_evening
                                    for key in overtime_dict:
                                        if night_counter != 0:
                                            # Find night hours during Friday that were considered overtime
                                            if key >= datetime.datetime.combine( overtime_date.date(), datetime.time( 0,
                                                                                                                      0 ) ) and key <= datetime.datetime.combine(
                                                    overtime_date.date(),
                                                    datetime.time( 7, 0 ) ) or key >= datetime.datetime.combine(
                                                    end_date,
                                                    datetime.time( 0, 0 ) ) and key <= datetime.datetime.combine(
                                                    end_date, datetime.time( 7, 0 ) ):
                                                overtime_night += 1
                                    if (overtime_date >= datetime.datetime.combine( overtime_date, datetime.time( 0,
                                                                                                                  0 ) ) and overtime_date <= datetime.datetime.combine(
                                            overtime_date, datetime.time( 7, 0 ) )) and (
                                            end_datetime >= datetime.datetime.combine( day_after,
                                                                                       datetime.time( 0, 0 ) )):
                                        overtime_night = overtime_night - 2
                                        night_counter = night_counter - overtime_night
                                    elif overtime_night != 0:
                                        overtime_night = overtime_night - 1
                                        night_counter = night_counter - overtime_night



                                # Calculate saturday and sunday
                                elif overtime_start_counter.strftime( "%A" ) == 'Saturday' and end_datetime.strftime(
                                        "%A" ) == 'Sunday':
                                    while overtime_start_counter <= end_datetime:
                                        overtime_dict[overtime_start_counter] = None
                                        overtime_start_counter += time_interval
                                    for key in overtime_dict:
                                        if saturday_counter != 0:
                                            if key <= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                                overtime_saturday += 1
                                            elif key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                                overtime_sunday += 1
                                    if overtime_saturday != 0:
                                        overtime_saturday = overtime_saturday - 1
                                        overtime_after_two_hr = overtime_saturday
                                        saturday_counter = saturday_counter - overtime_after_two_hr
                                    if overtime_sunday != 0:
                                        overtime_after_two_hr = overtime_sunday
                                        sunday_counter = sunday_counter - overtime_after_two_hr
                                    overtime_after_two_hr = overtime_saturday + overtime_sunday

                                # calculate only sunday or only saturday
                                elif overtime_start_counter.strftime(
                                        "%A" ) == 'Saturday' or overtime_start_counter.strftime( "%A" ) == 'Sunday':
                                    while overtime_start_counter <= end_datetime:
                                        overtime_dict[overtime_start_counter] = None
                                        overtime_start_counter += time_interval
                                    if overtime_start_counter.strftime( "%A" ) == 'Saturday':
                                        for key in overtime_dict:
                                            if saturday_counter != 0:
                                                if key <= datetime.datetime.combine( day_after, datetime.time( 0, 0 ) ):
                                                    overtime_saturday += 1
                                        if overtime_saturday != 0:
                                            overtime_saturday = overtime_saturday - 1
                                            overtime_after_two_hr = overtime_saturday
                                            saturday_counter = saturday_counter - overtime_after_two_hr
                                    elif overtime_start_counter.strftime( "%A" ) == 'Sunday':
                                        for key in overtime_dict:
                                            if saturday_counter != 0:
                                                if key <= datetime.datetime.combine( day_after, datetime.time( 0, 0 ) ):
                                                    overtime_sunday += 1
                                        if overtime_sunday != 0:
                                            overtime_sunday = overtime_sunday - 1
                                            overtime_after_two_hr = overtime_sunday
                                            sunday_counter = sunday_counter - overtime_after_two_hr

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                date_value_dict[date] = {
                                    'ordinary': int( ordinary_counter ),
                                    'night': int( night_counter ),
                                    'evening': int( evening_counter ),
                                    'sunday': int( sunday_counter ),
                                    'saturday': int( saturday_counter ),
                                    'public_holiday': int( public_holiday_counter ),
                                    'overtime_first2': int( overtime_first_two_hr ),
                                    'overtime_after2': int( overtime_after_two_hr ),
                                    'public_hol_overtime': int( public_overtime ),
                                    'overtime_sunday': int( overtime_sunday ),
                                    'overtime_saturday': int( overtime_saturday ),
                                    'total': int( total_for_date ),
                                }
                                overall_total = sum( item['total'] for item in date_value_dict.values() )
                                date_value_dict[date]['overall'] = overall_total
                                st.write( 'ordinary', ordinary_counter )
                                st.write( 'OT FIRST TWO', overtime_first_two_hr )
                                st.write( 'OT AFTER 2H', overtime_after_two_hr )

                            # Public holiday during shift overtime
                            elif overall_total / 60 >= 38 and (
                                    public_holiday == True or next_day_public_holiday == True):
                                # if len(date_value_dict)>= 2:
                                #     dict_length = len(date_value_dict)
                                #     day_before_total = date_value_dict[dict_length-2]
                                #     second_most_recent_overall_total = day_before_total['overall']
                                #     st.write('a',second_most_recent_overall_total)
                                # st.write(date_value_dict[date-datetime.timedelta(days=1)])
                                st.write( 'date', date )
                                st.write( 'end_date', end_date_check )
                                st.write( next_day_public_holiday )
                                st.write( 'overall total', overall_total )

                                st.write( 'uptohere' )
                                ordinary_counter = 0
                                night_counter = 0
                                evening_counter = 0
                                saturday_counter = 0
                                saturday_counter = 0
                                overtime_mins_int = overall_total - 2280
                                overtime_mins_timedelta = datetime.timedelta( minutes=overtime_mins_int )
                                overtime_start_counter = end_datetime - overtime_mins_timedelta
                                st.write( 'end datetime', end_datetime )
                                a = end_datetime - datetime.timedelta( hours=15 )

                                overtime_date = overtime_start_counter
                                first_two_hour_end = overtime_date + datetime.timedelta( minutes=120 )
                                st.write( 'ot mins', overtime_mins_int )
                                st.write( 'ot start time', overtime_start_counter )
                                if public_holiday == True and end_date_check == False and next_day_public_holiday == False:
                                    public_holiday_counter = (overtime_date - start_datetime_perm).total_seconds() / 60
                                    public_overtime = (end_datetime - overtime_date).total_seconds() / 60
                                elif public_holiday == True and end_date_check == True and next_day_public_holiday == False:
                                    while midnight_end_date <= overtime_date:
                                        ot_ph_dict[midnight_end_date] = None
                                        midnight_end_date += time_interval
                                    if end_date.strftime( "%A" ) == 'Monday' or end_date.strftime(
                                            "%A" ) == 'Tuesday' or end_date.strftime(
                                            "%A" ) == 'Wednesday' or end_date.strftime(
                                            "%A" ) == 'Thursday' or end_date.strftime( "%A" ) == 'Friday':
                                        if overtime_date > datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                            for key in ot_ph_dict:
                                                if key <= datetime.datetime.combine( end_date, datetime.time( 7, 0 ) ):
                                                    night_counter = night_counter + 1
                                            for key in ot_ph_dict:
                                                if key >= datetime.datetime.combine( end_date, datetime.time( 7,
                                                                                                              0 ) ) and key <= datetime.datetime.combine(
                                                        end_date, datetime.time( 19, 0 ) ):
                                                    ordinary_counter = ordinary_counter + 1
                                            for key in ot_ph_dict:
                                                if key >= datetime.datetime.combine( end_date, datetime.time( 19,
                                                                                                              0 ) ) and key <= datetime.datetime.combine(
                                                        end_date, datetime.time( 23, 59 ) ):
                                                    evening_counter = evening_counter + 1
                                            if night_counter != 0:
                                                night_counter = night_counter - 1
                                            if ordinary_counter != 0:
                                                ordinary_counter = ordinary_counter - 1
                                            if evening_counter != 0:
                                                evening_counter = evening_counter - 1
                                            if overtime_mins_int <= 120:
                                                overtime_first_two_hr = overtime_mins_int
                                            elif overtime_mins_int > 120:
                                                overtime_first_two_hr = 120
                                                overtime_after_two_hr = (
                                                                                    end_datetime - overtime_date).total_seconds() / 60

                                        elif overtime_date <= datetime.datetime.combine( end_date,
                                                                                         datetime.time( 0, 0 ) ):
                                            if first_two_hour_end > datetime.datetime.combine( end_date,
                                                                                               datetime.time( 0, 0 ) ):
                                                overtime_first_two_hr = (first_two_hour_end - datetime.datetime.combine(
                                                    end_date, datetime.time( 0, 0 ) )).total_seconds() / 60
                                                public_overtime = (datetime.datetime.combine( end_date,
                                                                                              datetime.time( 0,
                                                                                                             0 ) ) - overtime_date).total_seconds() / 60
                                                if first_two_hour_end <= end_datetime:
                                                    overtime_after_two_hr = (
                                                                                        end_datetime - first_two_hour_end).total_seconds() / 60
                                                elif first_two_hour_end > end_datetime:
                                                    overtime_after_two_hr = 0
                                            elif first_two_hour_end <= datetime.datetime.combine( end_date,
                                                                                                  datetime.time( 0,
                                                                                                                 0 ) ):
                                                overtime_first_two_hr = 0
                                                overtime_after_two_hr = (end_datetime - datetime.datetime.combine(
                                                    end_date, datetime.time( 0, 0 ) )).total_seconds() / 60
                                                public_overtime = (datetime.datetime.combine( end_date,
                                                                                              datetime.time( 0,
                                                                                                             0 ) ) - overtime_date).total_seconds() / 60

                                    elif end_date.strftime( "%A" ) == 'Saturday':
                                        if overtime_date > datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                            overtime_saturday = (end_datetime - overtime_date).total_seconds() / 60
                                            saturday_counter = (overtime_date - datetime.datetime.combine( end_date,
                                                                                                           datetime.time(
                                                                                                               0,
                                                                                                               0 ) )).total_seconds() / 60
                                        elif overtime_date <= datetime.datetime.combine( end_date,
                                                                                         datetime.time( 0, 0 ) ):
                                            public_overtime = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                   0 ) ) - overtime_date).total_seconds() / 60
                                            overtime_saturday = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                           datetime.time(
                                                                                                               0,
                                                                                                               0 ) )).total_seconds() / 60
                                    elif end_date.strftime( "%A" ) == 'Sunday':
                                        if overtime_date > datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                            overtime_saturday = (end_datetime - overtime_date).total_seconds() / 60
                                            sunday_counter = (overtime_date - datetime.datetime.combine( end_date,
                                                                                                         datetime.time(
                                                                                                             0,
                                                                                                             0 ) )).total_seconds() / 60
                                        elif overtime_date <= datetime.datetime.combine( end_date,
                                                                                         datetime.time( 0, 0 ) ):
                                            public_overtime = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                   0 ) ) - overtime_date).total_seconds() / 60
                                            overtime_sunday = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                         datetime.time(
                                                                                                             0,
                                                                                                             0 ) )).total_seconds() / 60

                                elif public_holiday == False and end_date_check == True and next_day_public_holiday == True:
                                    while start_datetime2 <= overtime_date:
                                        ot_ph_dict[start_datetime2] = None
                                        start_datetime2 += time_interval
                                    if start_datetime_perm.strftime( "%A" ) == 'Monday' or start_datetime_perm.strftime(
                                            "%A" ) == 'Tuesday' or start_datetime_perm.strftime(
                                            "%A" ) == 'Wednesday' or start_datetime_perm.strftime(
                                            "%A" ) == 'Thursday' or start_datetime_perm.strftime( "%A" ) == 'Friday':
                                        if overtime_date > datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                            public_overtime = (end_datetime - overtime_date).total_seconds() / 60
                                            public_holiday_counter = (
                                                                                 overtime_date - midnight_end_date).total_seconds() / 60
                                            for key in ot_ph_dict:
                                                if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                              0 ) ) and key <= datetime.datetime.combine(
                                                        date_obj, datetime.time( 7, 0 ) ):
                                                    night_counter = night_counter + 1
                                            for key in ot_ph_dict:
                                                if key >= datetime.datetime.combine( date_obj, datetime.time( 7,
                                                                                                              0 ) ) and key <= datetime.datetime.combine(
                                                        date_obj, datetime.time( 19, 0 ) ):
                                                    ordinary_counter = ordinary_counter + 1
                                            for key in ot_ph_dict:
                                                if key >= datetime.datetime.combine( date_obj, datetime.time( 7,
                                                                                                              0 ) ) and key <= datetime.datetime.combine(
                                                        end_date, datetime.time( 0, 0 ) ):
                                                    evening_counter = evening_counter + 1
                                            if night_counter != 0:
                                                night_counter = night_counter - 1
                                            if ordinary_counter != 0:
                                                ordinary_counter = ordinary_counter - 1
                                            if evening_counter != 0:
                                                evening_counter = evening_counter - 1
                                        elif overtime_date <= datetime.datetime.combine( end_date,
                                                                                         datetime.time( 0, 0 ) ):
                                            st.write( 'ot mins', overtime_mins_int )
                                            public_overtime = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                         datetime.time(
                                                                                                             0,
                                                                                                             0 ) )).total_seconds() / 60
                                            if overtime_mins_int <= 120:
                                                overtime_first_two_hr = overtime_mins_int
                                            elif overtime_mins_int > 120:
                                                overtime_first_two_hr = 120
                                                overtime_after_two_hr = (datetime.datetime.combine( end_date,
                                                                                                    datetime.time( 0,
                                                                                                                   0 ) ) - first_two_hour_end).total_seconds() / 60
                                            for key in ot_ph_dict:
                                                if key >= datetime.datetime.combine( date_obj, datetime.time( 0,
                                                                                                              0 ) ) and key <= datetime.datetime.combine(
                                                        date_obj, datetime.time( 7, 0 ) ):
                                                    night_counter = night_counter + 1
                                            for key in ot_ph_dict:
                                                if key >= datetime.datetime.combine( date_obj, datetime.time( 7,
                                                                                                              0 ) ) and key <= datetime.datetime.combine(
                                                        date_obj, datetime.time( 19, 0 ) ):
                                                    ordinary_counter = ordinary_counter + 1
                                            for key in ot_ph_dict:
                                                if key >= datetime.datetime.combine( date_obj, datetime.time( 7,
                                                                                                              0 ) ) and key <= datetime.datetime.combine(
                                                        end_date, datetime.time( 0, 0 ) ):
                                                    evening_counter = evening_counter + 1
                                            if night_counter != 0:
                                                night_counter = night_counter - 1
                                            if ordinary_counter != 0:
                                                ordinary_counter = ordinary_counter - 1
                                            if evening_counter != 0:
                                                evening_counter = evening_counter - 1
                                    elif start_datetime_perm.strftime( "%A" ) == 'Saturday':
                                        if overtime_date > datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                            public_overtime = (end_datetime - overtime_date).total_seconds() / 60
                                            public_holiday_counter = (
                                                                                 overtime_date - midnight_end_date).total_seconds() / 60
                                            saturday_counter = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                    0 ) ) - start_datetime_perm).total_seconds() / 60
                                        elif overtime_date <= datetime.datetime.combine( end_date,
                                                                                         datetime.time( 0, 0 ) ):
                                            saturday_counter = (
                                                                           overtime_date - start_datetime_perm).total_seconds() / 60
                                            public_overtime = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                         datetime.time(
                                                                                                             0,
                                                                                                             0 ) )).total_seconds() / 60
                                            overtime_saturday = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                     0 ) ) - overtime_date).total_seconds() / 60
                                    elif start_datetime_perm.strftime( "%A" ) == 'Sunday':
                                        if overtime_date > datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                            public_overtime = (end_datetime - overtime_date).total_seconds() / 60
                                            public_holiday_counter = (
                                                                                 overtime_date - midnight_end_date).total_seconds() / 60
                                            sunday_counter = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                  0 ) ) - start_datetime_perm).total_seconds() / 60
                                        elif overtime_date <= datetime.datetime.combine( end_date,
                                                                                         datetime.time( 0, 0 ) ):
                                            sunday_counter = (overtime_date - start_datetime_perm).total_seconds() / 60
                                            public_overtime = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                         datetime.time(
                                                                                                             0,
                                                                                                             0 ) )).total_seconds() / 60
                                            overtime_sunday = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                   0 ) ) - overtime_date).total_seconds() / 60

                                    total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr + public_overtime + overtime_sunday + overtime_saturday
                                    date_value_dict[date] = {
                                        'ordinary': int( ordinary_counter ),
                                        'night': int( night_counter ),
                                        'evening': int( evening_counter ),
                                        'sunday': int( sunday_counter ),
                                        'saturday': int( saturday_counter ),
                                        'public_holiday': int( public_holiday_counter ),
                                        'overtime_first2': int( overtime_first_two_hr ),
                                        'overtime_after2': int( overtime_after_two_hr ),
                                        'public_hol_overtime': int( public_overtime ),
                                        'overtime_sunday': int( overtime_sunday ),
                                        'overtime_saturday': int( overtime_saturday ),
                                        'total': int( total_for_date ),
                                    }

                                    overall_total = sum( item['total'] for item in date_value_dict.values() )
                                    date_value_dict[date]['overall'] = overall_total


                                elif public_holiday == True and end_date_check == True and next_day_public_holiday == True:
                                    public_overtime = (end_datetime - overtime_date).total_seconds() / 60
                                    public_holiday_counter = (overtime_date - start_datetime_perm).total_seconds() / 60

                                    total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr + public_overtime + overtime_sunday + overtime_saturday
                                    date_value_dict[date] = {
                                        'ordinary': int( ordinary_counter ),
                                        'night': int( night_counter ),
                                        'evening': int( evening_counter ),
                                        'sunday': int( sunday_counter ),
                                        'saturday': int( saturday_counter ),
                                        'public_holiday': int( public_holiday_counter ),
                                        'overtime_first2': int( overtime_first_two_hr ),
                                        'overtime_after2': int( overtime_after_two_hr ),
                                        'public_hol_overtime': int( public_overtime ),
                                        'overtime_sunday': int( overtime_sunday ),
                                        'overtime_saturday': int( overtime_saturday ),
                                        'total': int( total_for_date ),
                                    }

                                    overall_total = sum( item['total'] for item in date_value_dict.values() )
                                    date_value_dict[date]['overall'] = overall_total

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr + public_overtime + overtime_sunday + overtime_saturday
                                date_value_dict[date] = {
                                    'ordinary': int( ordinary_counter ),
                                    'night': int( night_counter ),
                                    'evening': int( evening_counter ),
                                    'sunday': int( sunday_counter ),
                                    'saturday': int( saturday_counter ),
                                    'public_holiday': int( public_holiday_counter ),
                                    'overtime_first2': int( overtime_first_two_hr ),
                                    'overtime_after2': int( overtime_after_two_hr ),
                                    'public_hol_overtime': int( public_overtime ),
                                    'overtime_sunday': int( overtime_sunday ),
                                    'overtime_saturday': int( overtime_saturday ),
                                    'total': int( total_for_date ),
                                }

                                overall_total = sum( item['total'] for item in date_value_dict.values() )
                                date_value_dict[date]['overall'] = overall_total
                                shift_length = (end_datetime - start_datetime_perm).total_seconds() / 60
                                st.write( 'shift length', shift_length )
                                st.write( 'date_total', total_for_date )
                                st.write( 'overtime ordinary', overtime_ordinary )
                                st.write( 'evening overtime', overtime_evening )
                                st.write( 'night overtime', overtime_night )
                                st.write( 'sat overtime', overtime_saturday )
                                st.write( 'sun overtime', overtime_sunday )
                                st.write( 'final ordinary', ordinary_counter )
                                st.write( 'final evening', evening_counter )
                                st.write( 'final sat', saturday_counter )
                                st.write( 'final night', night_counter )
                                st.write( 'final sun', sunday_counter )
                                st.write( 'overall hours', overall_total )
                                result = ordinary_counter + evening_counter + overtime_first_two_hr + overtime_after_two_hr + saturday_counter + night_counter
                                st.write( 'TOTAL HOURS AT END', result )
                                st.write( 'public OT', public_overtime )
                                st.write( 'first', overtime_first_two_hr )
                                st.write( 'after', overtime_after_two_hr )
                                st.write( date_value_dict )








                        elif overall_total / 60 >= 38:
                            overtime_mins_int = (end_datetime - start_datetime).total_seconds() / 60
                            overtime_mins_timedelta = datetime.timedelta( minutes=overtime_mins_int )
                            overtime_start_counter = end_datetime - overtime_mins_timedelta
                            overtime_date = start_datetime
                            # if overtime_mins_int <= 120:
                            #     overtime_first_two_hr = overtime_mins_int
                            #     first_two_hour_end = start_datetime + overtime_mins_timedelta
                            # elif overtime_mins_int > 120:
                            #     after2h_time_start = start_datetime + datetime.timedelta(minutes =120)
                            #     after2h_difference = end_datetime - after2h_time_start
                            if public_holiday == False and next_day_public_holiday == True and end_date_check == True:
                                public_overtime = (end_datetime - datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                      0 ) )).total_seconds() / 60
                                if (start_datetime.strftime( "%A" ) == 'Monday' or start_datetime.strftime(
                                        "%A" ) == 'Tuesday' or start_datetime.strftime(
                                        "%A" ) == 'Wednesday' or start_datetime.strftime(
                                        "%A" ) == 'Thursday' or start_datetime.strftime( "%A" ) == 'Friday'):
                                    if (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                            0 ) ) - start_datetime).total_seconds() / 60 <= 120:
                                        overtime_first_two_hr = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                     0 ) ) - start_datetime).total_seconds() / 60
                                    elif (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                              0 ) ) - start_datetime).total_seconds() / 60 > 120:
                                        overtime_first_two_hr = 120
                                        overtime_after_two_hr = (datetime.datetime.combine( end_date,
                                                                                            datetime.time( 0, 0 ) ) - (
                                                                             start_datetime + datetime.timedelta(
                                                                         minutes=120 ))).total_seconds() / 60
                                elif start_datetime.strftime( "%A" ) == 'Saturday':
                                    overtime_saturday = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                             0 ) ) - start_datetime).total_seconds() / 60
                                elif start_datetime.strftime( "%A" ) == 'Sunday':
                                    overtime_sunday = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                           0 ) ) - start_datetime).total_seconds() / 60

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                date_value_dict[date] = {
                                    'ordinary': int( ordinary_counter ),
                                    'night': int( night_counter ),
                                    'evening': int( evening_counter ),
                                    'sunday': int( sunday_counter ),
                                    'saturday': int( saturday_counter ),
                                    'public_holiday': int( public_holiday_counter ),
                                    'overtime_first2': int( overtime_first_two_hr ),
                                    'overtime_after2': int( overtime_after_two_hr ),
                                    'public_hol_overtime': int( public_overtime ),
                                    'overtime_sunday': int( overtime_sunday ),
                                    'overtime_saturday': int( overtime_saturday ),
                                    'total': int( total_for_date ),
                                }
                                overall_total = sum( item['total'] for item in date_value_dict.values() )
                                date_value_dict[date]['overall'] = overall_total
                                st.write( 'public OT', public_overtime )
                                st.write( 'overtime_sunday', overtime_sunday )
                                st.write( 'overtime_saturday', overtime_saturday )

                                st.write( 'first', overtime_first_two_hr )
                                st.write( 'after', overtime_after_two_hr )


                            elif public_holiday == False and next_day_public_holiday == False:
                                if overtime_start_counter.strftime( "%A" ) == 'Friday' and end_datetime.strftime(
                                        "%A" ) == 'Saturday':
                                    if overtime_mins_int <= 120:
                                        first_two_hour_end = start_datetime + overtime_mins_timedelta

                                        while start_datetime <= end_datetime:
                                            overtime_dict[start_datetime] = None
                                            start_datetime += time_interval
                                        if first_two_hour_end <= datetime.datetime.combine( end_date,
                                                                                            datetime.time( 0, 0 ) ):
                                            overtime_first_two_hr = overtime_mins_int
                                        else:
                                            for key in overtime_dict:
                                                if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                                    overtime_after_two_hr += 1
                                            overtime_after_two_hr = overtime_after_two_hr - 1
                                            overtime_first_two_hr = overtime_mins_int - overtime_after_two_hr

                                    elif overtime_mins_int > 120:
                                        after2h_time_start = start_datetime + datetime.timedelta( minutes=120 )
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

                                elif overtime_start_counter.strftime( "%A" ) == 'Sunday' and end_datetime.strftime(
                                        "%A" ) == 'Monday':
                                    if overtime_mins_int <= 120:
                                        first_two_hour_end = start_datetime + overtime_mins_timedelta
                                        while start_datetime <= end_datetime:
                                            overtime_dict[start_datetime] = None
                                            start_datetime += time_interval
                                        if first_two_hour_end <= datetime.datetime.combine( end_date,
                                                                                            datetime.time( 0, 0 ) ):
                                            overtime_after_two_hr = overtime_mins_int
                                        else:
                                            for key in overtime_dict:
                                                if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                                    overtime_first_two_hr += 1
                                            overtime_first_two_hr = overtime_first_two_hr - 1
                                            overtime_after_two_hr = overtime_mins_int - overtime_first_two_hr

                                    elif overtime_mins_int > 120:
                                        after2h_time_start = start_datetime + datetime.timedelta( minutes=120 )
                                        first_two_hour_end = after2h_time_start
                                        after2h_difference = end_datetime - after2h_time_start
                                        while start_datetime <= end_datetime:
                                            overtime_dict[start_datetime] = None
                                            start_datetime += time_interval
                                        for key in overtime_dict:
                                            if key <= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                                overtime_after_two_hr += 1
                                        if overtime_after_two_hr != 0:
                                            overtime_after_two_hr = overtime_after_two_hr - 1
                                        if after2h_time_start == datetime.datetime.combine( end_date,
                                                                                            datetime.time( 0, 0 ) ):
                                            for key in overtime_dict:
                                                if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                                    overtime_after_two_hr += 1
                                            overtime_after_two_hr = overtime_after_two_hr - 1
                                        elif after2h_time_start > datetime.datetime.combine( end_date,
                                                                                             datetime.time( 0, 0 ) ):
                                            after2h_after_midnight = first_two_hour_end - datetime.datetime.combine(
                                                end_date, datetime.time( 0, 0 ) )
                                            overtime_after_two_hr = overtime_after_two_hr + after2h_difference.total_seconds() / 60
                                            overtime_first_two_hr = after2h_after_midnight.total_seconds() / 60
                                        elif after2h_time_start < datetime.datetime.combine( end_date,
                                                                                             datetime.time( 0, 0 ) ):
                                            for key in overtime_dict:
                                                if key >= datetime.datetime.combine( end_date, datetime.time( 0, 0 ) ):
                                                    overtime_after_two_hr += 1
                                            overtime_after_two_hr = overtime_after_two_hr - 1

                                elif overtime_start_counter.strftime( "%A" ) == 'Saturday' and end_datetime.strftime(
                                        "%A" ) == 'Sunday':
                                    overtime_after_two_hr = overtime_mins_int
                                elif (overtime_start_counter.strftime(
                                        "%A" ) == 'Monday' or overtime_start_counter.strftime(
                                        "%A" ) == 'Tuesday' or overtime_start_counter.strftime(
                                        "%A" ) == 'Wednesday' or overtime_start_counter.strftime(
                                        "%A" ) == 'Thursday' or overtime_start_counter.strftime(
                                        "%A" ) == 'Friday') and (
                                        end_datetime.strftime( "%A" ) == 'Monday' or end_datetime.strftime(
                                        "%A" ) == 'Tuesday' or end_datetime.strftime(
                                        "%A" ) == 'Wednesday' or end_datetime.strftime(
                                        "%A" ) == 'Thursday' or end_datetime.strftime( "%A" ) == 'Friday'):
                                    while start_datetime <= end_datetime:
                                        overtime_dict[start_datetime] = None
                                        start_datetime += time_interval
                                    if overtime_mins_int <= 120:
                                        overtime_first_two_hr = overtime_mins_int
                                    elif overtime_mins_int > 120:
                                        overtime_first_two_hr = 120
                                        overtime_after_two_hr = overtime_mins_int - 120

                                elif overtime_start_counter.strftime(
                                        "%A" ) == 'Saturday' or overtime_start_counter.strftime( "%A" ) == 'Sunday':
                                    overtime_after_two_hr = overtime_mins_int

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr
                                date_value_dict[date] = {
                                    'ordinary': int( ordinary_counter ),
                                    'night': int( night_counter ),
                                    'evening': int( evening_counter ),
                                    'sunday': int( sunday_counter ),
                                    'saturday': int( saturday_counter ),
                                    'public_holiday': int( public_holiday_counter ),
                                    'overtime_first2': int( overtime_first_two_hr ),
                                    'overtime_after2': int( overtime_after_two_hr ),
                                    'total': int( total_for_date ),
                                }
                                overall_total = sum( item['total'] for item in date_value_dict.values() )
                                date_value_dict[date]['overall'] = overall_total

                                st.write( 'overtime ordinary', overtime_ordinary )
                                st.write( 'evening overtime', overtime_evening )
                                st.write( 'night overtime', overtime_night )
                                st.write( 'sat overtime', overtime_saturday )
                                st.write( 'sun overtime', overtime_sunday )

                                st.write( 'overtimestart', overtime_date )
                                st.write( 'final ordinary', ordinary_counter )
                                st.write( 'final evening', evening_counter )
                                st.write( 'final sat', saturday_counter )
                                st.write( 'final night', night_counter )
                                st.write( 'final sun', sunday_counter )

                                result = ordinary_counter + evening_counter + overtime_first_two_hr + overtime_after_two_hr + saturday_counter + night_counter
                                st.write( 'TOTAL HOURS AT END', result )
                                st.write( 'first', overtime_first_two_hr )
                                st.write( 'after', overtime_after_two_hr )
                                st.write( 'total overtime', overtime_mins_int )
                                st.write( date_value_dict )

                            elif public_holiday == True and next_day_public_holiday == False and end_date_check == False:
                                public_overtime = overtime_mins_int
                                date_value_dict[date] = {

                                    'ordinary': int( ordinary_counter ),
                                    'night': int( night_counter ),
                                    'evening': int( evening_counter ),
                                    'sunday': int( sunday_counter ),
                                    'saturday': int( saturday_counter ),
                                    'public_holiday': int( public_holiday_counter ),
                                    'overtime_first2': int( overtime_first_two_hr ),
                                    'overtime_after2': int( overtime_after_two_hr ),
                                    'total': int( total_for_date ),
                                }
                                overall_total = sum( item['total'] for item in date_value_dict.values() )
                                date_value_dict[date]['overall'] = overall_total
                                st.write( 'overtime ordinary', overtime_ordinary )
                                st.write( 'evening overtime', overtime_evening )
                                st.write( 'night overtime', overtime_night )
                                st.write( 'sat overtime', overtime_saturday )
                                st.write( 'sun overtime', overtime_sunday )
                                st.write( 'public OT', public_overtime )
                                st.write( 'overtimestart', overtime_date )
                                st.write( 'final ordinary', ordinary_counter )
                                st.write( 'final evening', evening_counter )
                                st.write( 'final sat', saturday_counter )
                                st.write( 'final night', night_counter )
                                st.write( 'final sun', sunday_counter )

                                result = ordinary_counter + evening_counter + overtime_first_two_hr + overtime_after_two_hr + saturday_counter + night_counter
                                st.write( 'TOTAL HOURS AT END', result )
                                st.write( 'first', overtime_first_two_hr )
                                st.write( 'after', overtime_after_two_hr )
                                st.write( 'total overtime', overtime_mins_int )

                            elif public_holiday == True and end_date_check == True and next_day_public_holiday == False:
                                public_holiday_hours = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                            0 ) ) - start_datetime).total_seconds() / 60
                                if end_datetime.strftime( "%A" ) == 'Monday' or end_datetime.strftime(
                                        "%A" ) == 'Tuesday' or end_datetime.strftime(
                                        "%A" ) == 'Wednesday' or end_datetime.strftime(
                                        "%A" ) == 'Thursday' or end_datetime.strftime( "%A" ) == 'Friday':
                                    if public_holiday_hours <= 120:
                                        public_overtime = public_holiday_hours
                                        overtime_first_two_hr = (120 - public_overtime)
                                        first_two_hour_end = (datetime.datetime.combine( end_date, datetime.time( 0,
                                                                                                                  0 ) ) + datetime.timedelta(
                                            minutes=overtime_first_two_hr ))
                                        overtime_after_two_hr = (end_datetime - first_two_hour_end).total_seconds() / 60
                                    elif public_holiday_hours > 120:
                                        public_overtime = public_holiday_hours
                                        overtime_after_two_hr = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                           datetime.time(
                                                                                                               0,
                                                                                                               0 ) )).total_seconds() / 60

                                elif end_datetime.strftime( "%A" ) == 'Saturday':
                                    public_overtime = public_holiday_hours
                                    overtime_saturday = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                   datetime.time( 0,
                                                                                                                  0 ) )).total_seconds() / 60
                                elif end_datetime.strftime( "%A" ) == 'Sunday':
                                    public_overtime = public_holiday_hours
                                    overtime_sunday = (end_datetime - datetime.datetime.combine( end_date,
                                                                                                 datetime.time( 0,
                                                                                                                0 ) )).total_seconds() / 60

                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday
                                date_value_dict[date] = {
                                    'ordinary': int( ordinary_counter ),
                                    'night': int( night_counter ),
                                    'evening': int( evening_counter ),
                                    'sunday': int( sunday_counter ),
                                    'saturday': int( saturday_counter ),
                                    'public_holiday': int( public_holiday_counter ),
                                    'overtime_first2': int( overtime_first_two_hr ),
                                    'overtime_after2': int( overtime_after_two_hr ),
                                    'public_hol_overtime': int( public_overtime ),
                                    'overtime_sunday': int( overtime_sunday ),
                                    'overtime_saturday': int( overtime_saturday ),
                                    'total': int( total_for_date ),
                                }
                                overall_total = sum( item['total'] for item in date_value_dict.values() )
                                date_value_dict[date]['overall'] = overall_total
                                st.write( 'public OT', public_overtime )
                                st.write( 'overtime_sunday', overtime_sunday )
                                st.write( 'overtime_saturday', overtime_saturday )

                                st.write( 'first', overtime_first_two_hr )
                                st.write( 'after', overtime_after_two_hr )

                            elif public_holiday == True and end_date_check == True and next_day_public_holiday == True:
                                public_overtime = (end_datetime - start_datetime).total_seconds() / 60
                                total_for_date = ordinary_counter + night_counter + evening_counter + sunday_counter + saturday_counter + public_holiday_counter + overtime_first_two_hr + overtime_after_two_hr + public_overtime + overtime_saturday + overtime_sunday + public_overtime
                                date_value_dict[date] = {
                                    'ordinary': int( ordinary_counter ),
                                    'night': int( night_counter ),
                                    'evening': int( evening_counter ),
                                    'sunday': int( sunday_counter ),
                                    'saturday': int( saturday_counter ),
                                    'public_holiday': int( public_holiday_counter ),
                                    'overtime_first2': int( overtime_first_two_hr ),
                                    'overtime_after2': int( overtime_after_two_hr ),
                                    'public_hol_overtime': int( public_overtime ),
                                    'overtime_sunday': int( overtime_sunday ),
                                    'overtime_saturday': int( overtime_saturday ),
                                    'total': int( total_for_date ),
                                }
                                overall_total = sum( item['total'] for item in date_value_dict.values() )
                                date_value_dict[date]['overall'] = overall_total
                                st.write( 'public OT', public_overtime )
                                st.write( 'overtime_sunday', overtime_sunday )
                                st.write( 'overtime_saturday', overtime_saturday )

                                st.write( 'first', overtime_first_two_hr )
                                st.write( 'after', overtime_after_two_hr )
                                st.write( 'overall total hours', overall_total )


        return date_value_dict


# timesheet()# for value in dictionary:
st.write( timesheet() )


