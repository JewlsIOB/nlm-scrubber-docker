# This code is not used at all by the Dockerfile. It was used to create sql_dates.nci2.txt.
# It is kept here in case it needs to be edited.
def generate_sql_dates(file_name):
    """
    Given a file_name, writes a list of SQL dates to exclude from the NPM scrubber
    """
    with open(file_name, 'w') as file:
        for year_idx in range(129):
            year = 70 + year_idx
            whole_year = 1900 + year
            if year > 99:
                year = 100 - year # ensure year is only 2 digits
            year_with_zero = year
            if year < 10:
                year_with_zero = "0" + str(year)
            file.write(str(whole_year) + "\n")

            for month_idx in range(12):
                month = 1 + month_idx
                month_with_zero = month
                if month < 10:
                    month_with_zero = "0" + str(month)

                for day_idx in range(31):
                    day = 1 + day_idx
                    day_with_zero = day
                    if day < 10:
                        day_with_zero = "0" + str(day)

                    # handle non-leap years
                    if (day == 29 and month == 2 and whole_year % 4 != 0):
                        break
                    # handle Feb. 30/31
                    if (day > 29 and month == 2):
                        break
                    # handle months that don't have 30 days
                    if (day == 31 and (month == 4 or month == 6 or month == 9 or month == 11)):
                        break

                    # SQL formatted dates to preserve
                    file.write(str(whole_year) + "-" + str(month_with_zero) + "-" + str(day_with_zero)  + "\n")

