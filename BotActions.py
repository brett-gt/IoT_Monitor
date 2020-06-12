''' Holds particular Bot actions to be executed on device output.

    Intent is for this file to be application specific, where other
    files are primarily generic.
'''

import re

#--------------------------------------------------------------------------------
def parse_device_input(text):
    results = []
    
    shout = find_shout(text)
    if(shout is not None):
        results.append(shout)
    
#--------------------------------------------------------------------------------
def find_shout(text):
    seq = re.compile("^\w+ shouts '(.*?)'")
    shout = seq.match(text)
    if(shout):
        print("SHOUT FOUND")
        return text
    else:
        return None



#----------------------------------------------------------------------------
def main():
    ''' Unit test '''
    find_shout("Cyrus shouts 'looking'")

if __name__ == '__main__':
    print("BotActions Unit Test:")
    main()





