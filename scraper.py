from dataclasses import dataclass
from enum import Enum

import requests

from utils import get_random_header


class SalutationEnum(str, Enum):
    MR = 'MR'
    MRS = 'MRS'


@dataclass
class FormData:
    email: str
    first_name: str
    last_name: str
    phone_number: str
    salutation: SalutationEnum
    number_of_persons: int
    number_of_kids: int
    monthly_net_income: int


@dataclass
class OfferConditions:
    price_min: int
    price_max: int  # warm, in €
    size_min: int  # in square meters
    size_max: int
    rooms_min: int
    rooms_max: int


class Offers:
    def __init__(self, conditions: OfferConditions):
        self.conditions = conditions

    def _make_request(self) -> dict:
        url = (
            'https://immosuche.degewo.de/de/search.json?utf8=✓&property_type_id=1&categories[]=1'
            '&property_number=&address[raw]=&address[street]=&address[city]=&address[zipcode]='
            '&address[district]=&district=&price_switch=on&price_radio=custom'
            '&price_from={price_min}&price_to={price_max}&qm_radio=custom&qm_from={size_min}'
            '&qm_to={size_max}&rooms_radio=custom&rooms_from={rooms_min}&rooms_to={rooms_max}'
            '&features[]=&wbs_required=0&order=rent_total_without_vat_asc&'
        )

        built_url = url.format(
            price_min=self.conditions.price_min,
            price_max=self.conditions.price_max,
            size_min=self.conditions.size_min,
            size_max=self.conditions.size_max,
            rooms_min=self.conditions.rooms_min,
            rooms_max=self.conditions.rooms_max,
        )
        header = get_random_header()
        response = requests.get(built_url, headers=header)
        return response.json()

    @staticmethod
    def _parse_response(response: dict):
        return response['immos']

    def get_ids(self):
        raw_response = self._make_request()
        response = self._parse_response(raw_response)
        return [immo['id'] for immo in response]


class Form:

    @staticmethod
    def _convert_id(id_: str) -> str:
        new_id = id_.split('-')
        new_id = '{}.{}.{}-{}'.format(*new_id)
        return new_id

    @classmethod
    def fill(cls, id_: str, data: FormData) -> str:
        id_ = cls._convert_id(id_)
        url = (
            'https://app.wohnungshelden.de/api/applicationFormEndpoint/3.0/form'
            f'/create-application/6e18d067-8058-4485-99a4-5b659bd8ad01/{id_}'
        )

        header = get_random_header()
        header['authority'] = 'app.wohnungshelden.de'
        header['referer'] = (
            f'https://app.wohnungshelden.de/public/listings/{id_}'
            '/application?c=6e18d067-8058-4485-99a4-5b659bd8ad01'
        )

        json_data = {
            'defaultApplicantFormDataTO': {
                'applicantMessage': None,
                'email': data.email,
                'firstName': data.first_name,
                'lastName': data.last_name,
                'phoneNumber': data.phone_number,
                'salutation': data.salutation.value,
                'street': None,
                'houseNumber': None,
                'zipCode': None,
                'city': None,
            },
            'saveFormDataTO': {
                'formData': {
                    'numberPersonsTotal': str(data.number_of_persons),
                    'kids': str(data.number_of_kids),
                    '$$_monthly_net_income_$$': str(data.monthly_net_income),
                },
                'files': [],
            },
        }
        response = requests.post(
            url,
            headers=header,
            json=json_data,
        )
        return response.text
