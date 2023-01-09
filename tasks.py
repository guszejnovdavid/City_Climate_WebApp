from celery import celery
import config

celery_client = celery(config.APP_NAME +"-worker", broker=config.CELERY_BROKER_URL)

@celery_client.task
def send_mail_async(data):
    print("Sending mail to {}".format(data))
    return "Mail sent to {}".format(data)