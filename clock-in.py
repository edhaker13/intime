import time as now
import gspread
month = now.strftime('%b %y')
time = now.strftime('%H:%M:00')
day = now.strftime('%d/%m/%Y')
gc = gspread.login('luis.checa@sks-renewables.co.uk','eq=f#&aArj7q&jl-6.gZ&_')
sh = gc.open('Invoices')
ws = sh.worksheet(month)
d = ws.find(day)
entry = ws.cell(d.row,d.col+1).value
exit = ws.cell(d.row,d.col+2).value
ws.update_cell(d.row, d.col+1, time)
print(d.value, entry, exit, time)
