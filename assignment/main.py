import pandas as pd

df = pd.read_csv('Assignment_Timecard.xlsx - Sheet1.csv')

try:
    df['Start'] = pd.to_datetime(df['Time'], format="%m/%d/%Y %I:%M %p")
    df['End'] = pd.to_datetime(df['Time Out'], format="%m/%d/%Y %I:%M %p")
except ValueError:
    print("Warning: There's at least one misformatted time entry. Please check your data.")
    exit()

# Calculate Duration
df['Duration'] = (df['End'] - df['Start']).dt.total_seconds() / 3600

# a) Check for 7 consecutive days
grouped_dates = df.groupby('Employee Name')['Pay Cycle Start Date'].nunique()
names_7_days = grouped_dates[grouped_dates >= 7].index.tolist()

# b) Less than 10 hours but more than 1 hour between shifts
df_sorted = df.sort_values(['Employee Name', 'Start'])
df_sorted['Next_Start'] = df_sorted.groupby('Employee Name')['Start'].shift(-1)
df_sorted['Between_Shifts'] = (df_sorted['Next_Start'] - df_sorted['End']).dt.total_seconds() / 3600
names_shift_diff = df_sorted['Employee Name'][(df_sorted['Between_Shifts'] > 1) & (df_sorted['Between_Shifts'] < 10)].unique()

# c) More than 14 hours in a single shift
names_14_hours = df['Employee Name'][df['Duration'] > 14].unique()

# Display results
print("Employees who worked for 7 consecutive days:", names_7_days)
print("Employees with less than 10 hours but more than 1 hour between shifts:", names_shift_diff.tolist())
print("Employees who worked more than 14 hours in a single shift:", names_14_hours.tolist())

# Check for overlapping shifts
overlapping_shifts = df_sorted[df_sorted.duplicated(subset=['Employee Name', 'Start'], keep=False) | df_sorted.duplicated(subset=['Employee Name', 'End'], keep=False)]
if not overlapping_shifts.empty:
    print("\nWarning: Found potential overlapping shifts for the following employees:")
    print(overlapping_shifts[['Employee Name', 'Start', 'End']])
