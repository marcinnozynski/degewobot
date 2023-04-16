from scraper import FormData, OfferConditions, SalutationEnum

SCRAPEOPS_API_KEY = 'bb91da86-0296-423a-9875-d39c4ce9676b'
DATABASE_FILE_PATH = '../data/database.db'

FORM_DATA = FormData(
    first_name='Hans',
    last_name='Klaus',
    email='jarcin.max@gmail.com',
    salutation=SalutationEnum.MR,
    phone_number='12345678',
    number_of_kids=0,
    number_of_persons=1,
    monthly_net_income=3000,
)
OFFER_CONDITIONS = OfferConditions(
    price_min=0,
    price_max=1500,
    size_min=50,
    size_max=100,
    rooms_min=3,
    rooms_max=4,
)
