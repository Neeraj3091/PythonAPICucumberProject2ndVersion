from behave import *
import requests
import os
from dotenv import load_dotenv

@given('the API endpoint is "{endpoint}"')
def step_impl_given(context,endpoint):
    context.endpoint = endpoint

@when('I request the conversion rate')
def send_api(context):
    load_dotenv()
    api_key = os.environ.get('API_KEY')
    url = f'{context.endpoint}?apikey={api_key}'
    print(url)
    response = requests.get(url)
    context.response = response
    print(response)

@then('the API should be up and return status code 200')
def validate_api(context):
    assert context.response.status_code == 200

@then('the response generated takes EUR as default base currency')
def validate_default_currency(context):
    data = context.response.json()
    assert data["base"] == "EUR"

@when('I request the conversion rate with invalid API key')
def invalid_api(context):
    load_dotenv()
    api_key = os.environ.get('API_KEY_WRONG')
    url = f'{context.endpoint}?apikey={api_key}'
    response = requests.get(url)
    context.response = response

@then('the API should return status code 401')
def validate_api(context):
    assert context.response.status_code == 401

@then('it should return message as "Invalid authentication credentials"')
def message(context):
    data = context.response.json()
    assert data["message"] == "Invalid authentication credentials"

@when('I request the conversion rate for valid "{base}" and "{symbols}"')
def base_symbol_con(context,base,symbols):
    load_dotenv()
    api_key = os.environ.get('API_KEY')
    url = f'{context.endpoint}?apikey={api_key}&base={base}&symbols={symbols}'
    response = requests.get(url)
   # context.response_data = json.loads(response.text)
    context.response = response
    context.base = base
    context.symbols = symbols

@then('the API should return result only for given input')
def given_currency_result(context):
    data = context.response.json()
    assert data['base'] == context.base
    assert data["rates"][context.symbols]

@then('the conversion rate for given symbols should not be empty or null')
def check_rate_not_empty(context):
    data = context.response.json()
    assert data["rates"][context.symbols] is not None

@when('I request the conversion rate for invalid "{base}" and "{symbols}"')
def check_invalid_curr(context,base,symbols):
    load_dotenv()
    api_key = os.environ.get('API_KEY')
    url = f'{context.endpoint}?apikey={api_key}&base={base}&symbols={symbols}'
    response = requests.get(url)
    context.response = response

@then('the API should return status as false and give appropriate message')
def message(context):
    data = context.response.json()
    assert data['success'] == False
    assert data['error']['type'] == "invalid_currency_codes"


