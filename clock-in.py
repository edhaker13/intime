import time as now
import gspread
try:
    from secrets import *
except Exception as exc:
    raise ImportError(
        'Create secrets.py with username(user), password(pwd),\
            and destination address(to)!') from exc
month = now.strftime('%b %y')
time = now.strftime('%H:%M:00')
day = now.strftime('%d/%m/%Y')
gc = gspread.login(user,pwd)
sh = gc.open('Invoices')
ws = sh.worksheet(month)
d = ws.find(day)
entry = ws.cell(d.row,d.col+1).value
exit = ws.cell(d.row,d.col+2).value
ws.update_cell(d.row, d.col+1, time)
print('Day: {} Start: {} Finish: {} New Start: {}'\
      .format(d.value, entry, exit, time))
