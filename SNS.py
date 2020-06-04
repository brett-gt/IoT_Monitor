''' Handle send text messages through AWS SNS service.
'''
#Need to pip install boto3 to support

import boto3
import Secrets

class SNS(object):

    #----------------------------------------------------------------------------
    def __init__(self, phone_numbers):
        ''' Initialize the SNS topic and connect to AWS
        '''
        # Create an SNS client
        self.client = boto3.client(
            "sns",
            aws_access_key_id = Secrets.aws_access_key_id,
            aws_secret_access_key = Secrets.aws_secret_access_key,
            region_name="us-east-1")

        self.topic_arn = self.create_topic(phone_numbers)


    #----------------------------------------------------------------------------
    def create_topic(self, phone_numbers):
        ''' Create a topic so can send one text to multiple numbers
        '''
        # Create the topic if it doesn't exist (this is idempotent)
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
        self.client.publish(Message=message, TopicArn= self.topic_arn)


#----------------------------------------------------------------------------
def main():
    ''' Unit test '''
    #TODO: Remove phone number before github
    messanger = SNS([Secrets.phone_number])
    messanger.send_text("Test")
    print("Text sent...")

if __name__ == '__main__':
    print("SMS Unit Test:")
    main()


