import gspread
import smtplib
import re
try:
    from secrets import *
except Exception as exc:
    raise ImportError(
        'Create secrets.py with username, password, and destination address!'
    ) from exc
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def make_email(subject, who_from, who_to, text_body, html_body):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = who_from
    msg['To'] = who_to
    # Record the MIME types of both parts - text/plain and text/html
    # Using UTF-8 because of £s
    part1 = MIMEText(text_body, 'plain','UTF-8')
    part2 = MIMEText(html_body, 'html','UTF-8')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    return msg

def send_email(username, password, message, host='smtp.gmail.com'):
    # Send the message via gmail
    s = smtplib.SMTP()
    s.connect(host)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(username,password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send, if no addresses it looks them up from message
    s.send_message(message)
    try:
        s.quit()
    except:
        pass

def split_rows(alist, sublen):
    # Make a new sublist every sublen
    return [alist[i:i+sublen] for i in range(0, len(alist), sublen)]

def split_cols(alist, sublen):
    # Same but split into columns
    numrows = (len(alist)+sublen-1) // sublen
    return [alist[i::sublen] for i in range(numrows)]

def list_split(alist,sublength, by_column=False):
    # Wrapper for split cols/rows
    if by_column:
        lol = split_cols(alist, sublength)
    else:
        lol = split_rows(alist, sublength)
    return lol

def str_table(alist, sublength,by_column=False):
    # Make a nicely formatted string table
    string = ''
    width = len(max(alist, key=len))
    table = list_split(alist, sublength, by_column)
    for row in table:
        string +='|' + ('{:^{width}}|'*sublength).format(*row,width=width)+ '\n'
    return string

def html_table(alist,sublength, by_column=False):
    # Make a html table
    table = list_split(alist, sublength, by_column)
    string = '<table>'
    for row in table:
        string += '  <tr><td>'+'    </td><td>'.join(row)+'  </td></tr>'
    string += '</table>'
    return string

def get_table(username, password):
    # Get table data from Google Spreadsheets
    global subject, cols, to
    now = datetime.today()
    month = now.strftime('%b %y')
    friday = (now + timedelta(4 - now.weekday())).strftime('%d/%m/%Y')
    monday = (now + timedelta(0 - now.weekday())).strftime('%d/%m/%Y')
    today = now.strftime('%d/%m/%Y')
    if friday != today:
        # Informative message, not friday
        to = user
        warning = 'Warning!\n{} is not friday, week isn\'t over yet!\
                \nI\'ll go ahead and assume this is a test\
                \nSending email to: {}'.format(today, to).ljust(80)
        print(warning)
    sh = gspread.login(username,password).open(book)
    ws = sh.worksheet(month)
    m = str(ws.find(monday).row - 1)
    f = str(ws.find(friday).row + 2)
    week_list = ws.range('A'+m+':E'+f)
    # Declarations to be re-used outside of the function
    cols = ws.get_int_addr('E1')[-1]
    subject = 'Invoice from {} to {}'.format(monday,friday).replace('/','-')
    # Slightly formatted data, parsed None
    return ['' if (y.value is None) else re.sub(r':\d{2}$','', y.value) for y in week_list]
# More formatting of data
week = [re.sub(r'(\.\d{2})\d+', r'\1',string) for string in get_table(user,pwd)]
# Get tables
table_str = str_table(week, cols)
table_html = html_table(week,cols)

# Create the body of the message (a plain-text and an HTML version).
text = 'Hi, this is my invoice for this week.\n' + table_str
html = '<html><head></head><body><p>Hi!<br>This is my invoice for this week.</p><p>%s</p></body></html>'  % table_html

# Make outputs text file and email
with open(subject+'.txt', 'w+',encoding='utf-8') as f:
    f.write(table_str)
    f.close()
msg = make_email(subject, 'Luis Checa <%s>' % user, to, text, html)

# Send Email and print message
send_email(user, pwd, msg)
print('Success, %s sent!' % subject)
