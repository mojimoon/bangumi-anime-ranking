'''
before using this script,
copy the table from your Excel to table.txt
this script will convert \t to spaces to make columns aligned
for websites that doesn't understand \t (like Bangumi)

NOTE: do not use vscode to edit table.txt (it will convert \t to spaces)
(check your tab/space settings at right bottom status bar)
'''

with open('table.txt', 'r') as f:
    lines = f.readlines()

# determine the number of columns in the table
num_cols = len(lines[0].split('\t'))

# determine the maximum width of each column
col_widths = [max(len(line.split('\t')[i]) for line in lines) for i in range(num_cols)]

# replace tabs with spaces and left-align each column
for line in lines:
    cols = line.split('\t')
    new_line = ''
    for i in range(num_cols):
        new_line += cols[i].ljust(col_widths[i] + 2)
    print(new_line.rstrip())