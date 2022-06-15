import datetime
from Helpers import hepler
import logging


class Listener:

    @staticmethod
    def sendEmail(eventData):
        currentDateTime = datetime.datetime.now()
        if eventData == None:
            logging.info(
                "{} : Event data is not available. class = {}, function={}".format(currentDateTime, "Listener",
                                                                                   'SendEmail'))
        if 'receipt_email_id' not in eventData or 'message' not in eventData:
            logging.info(
                "{} :Receipt_email_id or message is not present. class = {}, function={}".format(currentDateTime,
                                                                                                 "Listener",
                                                                                                 'SendEmail'))
        try:
            hepler.sendEmail(eventData['receipt_email_id'], eventData['message'])
        except Exception as error:
            logging.error("{} Email is not sent {}".format(currentDateTime, error))
            exit()
