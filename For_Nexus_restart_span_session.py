
from cli import *
import json
import time

def go_up_session(session_id):
   go_cmd1 = clip("conf t ; monitor session " + session_id + " type erspan-source ; shut ; no shut ; end")
   print('session ' + session_id + ' is up')

def show_session():
   output1 = clid('show monitor')
   jd1 = json.loads(output1)
   session_id = (jd1["TABLE_session"]["ROW_session"]["session_number"])
   state_session = (jd1["TABLE_session"]["ROW_session"]["state"])
   if state_session == 'up':
     print('session ' + session_id + ' is up')
   elif state_session == 'down':
     go_up_session(session_id)
   #print(session_id)
   #print(state_session)


show_session()