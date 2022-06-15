import threading
import datetime
import logging

class Event:
    instance = None

    @staticmethod
    def getInstance():
        if Event.instance == None:
            Event.instance = Event()

        return Event.instance

    @staticmethod
    def fire(eventFunction, eventData=None):
        currentDateTime = datetime.datetime.now()
        try:
            if eventFunction == "":
                logging.debug("{} :Listener is not present".format(currentDateTime))
                return ""

            if eventFunction is None:
                logging.debug("{} :Listener is not present in Listener".format(currentDateTime))
                return ""

            t = threading.Thread(
                target=eventFunction(eventData),
                args=(eventData,),
                daemon=True
            )

            t.start()
            t.join()
            logging.info("{} :Event is fired for {} and event data {}".format(currentDateTime, eventFunction, eventData))
        except Exception as error:
            logging.error("{} :Event fire is failed:-  {}".format(currentDateTime, error))
