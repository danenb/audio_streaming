import glob, sys, datetime
files = glob.glob('*.mp3')
length = len(files)


def errorLog (message):
    'Log an error message to file'
    now = str(datetime.datetime.now())[:19]
    message = now + '  -  ' + message + '\n'
    try:
        errlog = open('Error Log.txt', 'a')
        errlog.write(message)
        errlog.close()
        del errlog
    except:
        print '\nFailed to log error:',message,'\n'


print "Content-type:text/html\r\n"

if length > 0:

    for i in range(0,len(files)):
        sys.stdout.write(files[i] + ',')
