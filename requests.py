import json

import requests
import pprint


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, json=data)
            elif request_type == 'PUT':
                response = requests.put(url, json=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True
        return response

    def get(self, endpoint, endpoint_id, expected_error=True):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response.json()

    def post(self, endpoint, endpoint_id='', body=None):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'POST', data=body, expected_error=True)
        return response.json()

    def delete(self, endpoint, endpoint_id=''):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response.json()['message']

    def put(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'PUT', data=body)
        return response.json()['message']


BASE_URL_PETSTORE = 'https://petstore.swagger.io/v2'
base_request = BaseRequest(BASE_URL_PETSTORE)

data = {
        "id": 1,
        "petId": 1,
        "quantity": 6,
        "shipDate": "2023-05-13T23:54:30.827Z",
        "status": "placed",
        "complete": True
}

user_data = {
        "id": 1,
        "username": "john",
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@me.com",
        "password": "john$123",
        "phone": "+900 928 00 13",
        "userStatus": 1
  }

push_order = base_request.post('store', 'order', data) #Добавить заказ

base_request.delete('store/order', 3) #Удалить заказ

store_info = base_request.get('store', 'inventory') #Получить информацию о списке товаров
pprint.pprint(store_info)

result = base_request.get('store/order', 3)   #Получить информацию о заказе
pprint.pprint(result)

user = base_request.post('user', body=user_data) #Добавить пользователя
pprint.pprint(user)

user = base_request.put('user', 'DS', user_data) #Изменить пользователя
pprint.pprint(user)

user2 = base_request.get('user', 'DS') #Получить информацию о пользователе
pprint.pprint(user2)

delete = base_request.delete('user', 'DS') #Удалить пользователя
print(delete)
