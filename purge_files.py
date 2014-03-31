import cgi, os, sys

POST = cgi.FieldStorage()

file_name = POST.getvalue('file_name')
print "Content-type:text/html\r\n"
if file_name != None:
    os.remove(file_name)
    sys.stdout.write('complete')
else:
    print 'Invalid file name'
