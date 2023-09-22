import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

filename = 'rhel-8.oval.xml'  #../xml/<filename>
filepath = os.path.join(BASE_DIR, 'files' ,filename)