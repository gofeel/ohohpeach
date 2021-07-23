from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
import re
from django.conf import settings


def sendsms(to, message):
    pattern = re.compile(r'^010\d{8}$')
    if not pattern.match(to):
        return

    api_key = settings.NOTIFICATION_SMS_ACCESS_KEY
    api_secret = settings.NOTIFICATION_SMS_SECRET_KEY
    sender = settings.NOTIFICATION_SMS_SENDER

    params = dict()
    params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
    params['to'] = to
    params['from'] = sender
    params['text'] = message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
