import time
import gspread
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('direction',
                    help='Whether to enter of exit work',
                    choices=['entry', 'exit'])
parser.add_argument('-u',"--user",
                    help='Username to login to google docs',
                    default='luis.checa@sks-renewables.co.uk')
parser.add_argument('-p','--password',
                    help='Password to login to google docs',
                    default='eq=f#&aArj7q&jl-6.gZ&_')
parser.add_argument('-m','--month',
                    help='Manually add the month to search',
                    default=time.strftime('%b %y'))
parser.add_argument('-t','--time',
                    help='Time to enter into spreadsheet',
                    default=time.strftime('%H:%M:%S'))
parser.add_argument('-d','--day',
                    help='Day to enter into spreadsheet',
                    default=time.strftime('%d/%m/%Y'))
parser.add_argument('-s','--sheet',
                    help='Sheet name to enter information',
                    default='Invoices')
args = parser.parse_args()
gc = gspread.login(args.user,args.password)
sh = gc.open(args.sheet)
ws = sh.worksheet(args.month)
d = ws.find(args.day)
entry = ws.cell(d.row,d.col+1).value
exit = ws.cell(d.row,d.col+2).value
if args.direction == "entry":
    opt = 1
elif args.direction == "exit":
    opt = 2
ws.update_cell(d.row, d.col+opt, args.time)
print('Day: {} Entry: {} Exit: {} New: {}'.format(d.value, entry, exit, args.time))
