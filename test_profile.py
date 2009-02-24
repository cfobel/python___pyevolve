import sys


def trace_dispatch(frame, event, arg):
   if event == "call":
      cod = frame.f_code

      print "Event: ", event
      print "co_name:   ", cod.co_name
      print cod.co_filename + ":" + str(cod.co_firstlineno)

      print "-" * 40


class K:
   def __init__(self):
      pass

   def B(self):
      return 0
   
def A():
   n = K()
   n.B()
   return 0

def run_main():
   print "sfdlksdlf"
   A()

if __name__ == "__main__":
   sys.setprofile(trace_dispatch)
   run_main()
    