import time
from random import random

from scraper import Offers, Form
from settings import FORM_DATA, OFFER_CONDITIONS
from utils import RequestHistory


def main():
    offers = Offers(conditions=OFFER_CONDITIONS)
    offer_ids = offers.get_ids()
    print(f'Available offers [{len(offer_ids)}]: {offer_ids}')
    print(f'Sending applications as {FORM_DATA.email}\n')

    request_history = RequestHistory()

    for offer_id in offer_ids:
        if request_history.is_application_already_submitted(FORM_DATA.email, offer_id):
            continue

        print('Sending application of', offer_id)
        status = Form.fill(offer_id, data=FORM_DATA)

        if status == 'true':
            request_history.add_application(FORM_DATA.email, offer_id)
            print('Application has been successfully submitted')

        elif status == 'Es existiert bereits eine Anfrage mit dieser E-Mail Adresse':
            request_history.add_application(FORM_DATA.email, offer_id)
            print(f'Warning: application of {offer_id} has been already submitted')

        else:
            print(f'Warning: {status}')

        time.sleep(30 * random() + 15)


if __name__ == '__main__':
    main()
