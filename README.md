intime
======
A Collection of scripts to manipulate a google spreadsheet timetable

Features
========
- Open a spreadsheet by it's name. (Default: Invoices)
- Insert the time of arrival.
- Insert the time of depature.
- Gather and send the table by email.

The reason I dediced to create these scripts is because I had a tendency to forget at 
what time I had left work and have to look through email and other stuff that would
give me a clue. It's mostly the same with the email, altough it's also convenient.

Requirements
============

Needs Python 3+. (mostly because of the syntax)
A readable spreadsheet in google drive.
The gspread library which saved me when I was struggling with the weird google api.
    You can find that [here](https://github.com/burnash/gspread)

Installing
==========
You can install the gspread library with pip or through github.
- From PyPI
```
pip install gspread
```
or
```
easy_install gspread
```

- From github
```
git clone https://github.com/burnash/gspread.git
cd gspread
python setup.py install
```

Clone this repo and create a file called secrets.py with your details.
```sh
git clone https://github.com/edhaker13/intime.git
cd intime
vim secrets.py # or whatever editor you use.
```

secrets.py
```python
user=<your google user> # the username for both the spreadsheet and the email.
pwd=<your password> # Sadly gspread does not support Two-factor auth.
book=<the workbook name> # Name of the workbook to manipulate.
to=<the destinataries email address> # Only needed for the email.
## This file won't leave your system; you can use encoded text, then assign the decoded text to the variables
```

The spreadsheet should have a format similar to this:

![example] (https://raw.github.com/edhaker13/intime/master/example.png)

The worksheet should be named: '<Month> <Year>'; e.g. Apr 13.

The name of the headers or the text format is not important,
but the entry time should be next to the date and before the exit time.
e.g. Date: 13/06/13,Entry: 9am, Exit: 8pm

Description
===========
There are 4 scripts: _clock-in, clock-out, clock-end_ and _clocking_

The _clock-*_ scripts are stand alones that will do specific functions.

I had to make them like this because they're intended to be used on android with sl4a
which does not allow passing arguments with the locale plugin.

*clocking* is the global version for use in a console.

*clock-in* will insert the current time into entry on the correspondent date.
*clock-out* will insert the current time into exit on the correspondent date.
*clock-end* will retrieve the table for the whole week, format and send as a html table.

_If it isn't friday the table will be sent to the sender as a test._

Thanks to resources used
======
- [Burnash](https://github.com/burnash) for an understable and easy to use API, 
I was going mad reading outdated documentation from google.
- [Stackoverflow](https://stackoverflow.com/questions/tagged/python) 
for great answers when I was looking how to make the data into a html table.
- [SL4A](https://code.google.com/p/android-scripting/) for a way to use python
on android without too much hassle.
- [Llama](https://play.google.com/store/apps/details?id=com.kebab.Llama) area detection and automation
- [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm)
for the missing bits in automation.
