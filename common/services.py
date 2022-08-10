from time import sleep

def sleep_and_remove(obj):
       sleep(3600)
       obj.delete()
       
def hook_after_sleep(task):
       print('Story has been Deleted')
       
def sleep_and_send(secs = 15):
       sleep(secs)
       