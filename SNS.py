''' Handle send text messages through AWS SNS service.
'''
#Need to pip install boto3 to support

import boto3
from datetime import datetime
from dateutil.relativedelta import relativedelta
from CircularBuffer import CircularBuffer
import Secrets

from time import sleep #TODO: For testing only, can remove

class SNS(object):

    #----------------------------------------------------------------------------
    def __init__(self, phone_numbers, debug = False):
        ''' Initialize the SNS topic and connect to AWS
        '''
        
        #TODO: Could eventually do a log
        self.msgs_sent = 0;
        self.msg_limit_per_hour = 2;
        self.time_stamps = CircularBuffer(self.msg_limit_per_hour)
        self.debug = debug

        # Create an SNS client
        self.client = boto3.client(
            "sns",
            aws_access_key_id = Secrets.aws_access_key_id,
            aws_secret_access_key = Secrets.aws_secret_access_key,
            region_name="us-east-1")
        
        self.topic_arn = self.create_topic(phone_numbers)

    #----------------------------------------------------------------------------
    def safe_to_send(self):
        ''' Do any checks we want before we send the message.  Putting in a throughput
            limiter for now in case something goes crazy.

            Returns boolean True if safe to send, False if not.
        '''
        safe = False
        if(self.msgs_sent < self.msg_limit_per_hour):
            safe = True
        else:
            timeDiff = datetime.now() - self.time_stamps.get_oldest()
            if (timeDiff.total_seconds() < 3600):
                print("SNS: Text limit exceeded. " + str(self.msgs_sent) + " messages in last " + str(timeDiff.total_seconds()) + " seconds")
                safe = False
            else:
                safe = True
        return safe
                
    #----------------------------------------------------------------------------
    def create_topic(self, phone_numbers):
        ''' Create a topic so can send one text to multiple numbers
        '''
        topic = self.client.create_topic(Name="notifications")
        topic_arn = topic['TopicArn']  # get its Amazon Resource Name

        # Add SMS Subscribers
        for number in phone_numbers:
            self.client.subscribe(
                TopicArn=topic_arn,
                Protocol='sms',
                Endpoint=number  # <-- number who'll receive an SMS message.
            )
        return topic_arn


    #----------------------------------------------------------------------------
    def send_text(self, message):
        # Publish a message.
        if(self.safe_to_send()):
            if(not self.debug):
                self.client.publish(Message=message, TopicArn= self.topic_arn)

            self.time_stamps.append(datetime.now())
            self.msgs_sent += 1
            print("SNS Message Sent: " + message)
  

#----------------------------------------------------------------------------
def main():
    ''' Unit test '''
    #TODO: Comment out the actual publish line if don't want to send the text
    messanger = SNS([Secrets.phone_num], debug=True)
    messanger.send_text("Test")
    sleep(2)
    messanger.send_text("Test1")
    sleep(4)
    messanger.send_text("Test2")
    sleep(5)
    messanger.send_text("Test3")
    sleep(10)
    messanger.send_text("Test4")
    sleep(20)
    messanger.send_text("Test5")
    sleep(20)
    messanger.send_text("Test6")
    sleep(8)
    messanger.send_text("Test7")
    sleep(8)
    messanger.send_text("Test8")
    sleep(8)
    messanger.send_text("Test9")
    #print("Text sent...")

if __name__ == '__main__':
    print("SMS Unit Test:")
    main()


