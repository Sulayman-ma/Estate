import requests
import json



class Transaction:
    def __init__(self, secret_key, **kwargs) -> None:
        super().__init__(**kwargs)
        self.auth = 'Bearer {}'.format(secret_key)
        self.api_url = 'https://api.paystack.co/transaction'


    def initialize(self, email: str, amount: str, **kwargs) -> dict:
        """Initialize a transaction to accept a payment(one time) from a customer.
        
        Keyword arguments:
        :param email: The customer's email
        :param amount: Payment amount in NGN, two extra 0s for kobo, e.g. 200000 for twenty thousand naira and zero kobo
        
        Optional arguments (kwargs):
        :param label: String that replaces customer email as shown on the checkout form
        :param callback_url: Fully qualified url, e.g. https://example.com/ . Use this to override the callback url provided on the dashboard for this transaction
        :param reference: Unique transaction reference. Only -, ., = and alphanumeric characters allowed
        :param channels: An array of payment channels to control what channels you want to make available to the user to make a payment with. Available channels include; ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']

        Return: Paystack transaction data dictionary
        """

        # merge with required parameters with optional ones for the body
        body = {'email': email, 'amount':amount, **kwargs}
        response = requests.post(
            url = self.api_url + "/initialize",
            headers = {
                'Authorization': self.auth,
                'Content-Type': 'application/json'
            },
            # jsonify the dictionary for POST
            data = json.dumps(body)
        ).json()
        response = response.get('data')
        return response
        

    def verify(self, reference: str) -> bool:
        """Verify a transaction made by a customer.
        
        Keyword arguments:
        :param reference: The transaction reference gotten from the initialize method

        Return: Boolean for the transaction status
        """
        
        response = requests.get(
            url = "{}/verify/{}".format(self.api_url, reference),
            headers = {
                'Authorization': self.auth
            }
        ).json().get('data')
        # transaction status from the response JSON's data object
        response = response.get('status')
        return True if response == 'success' else False


    def fetch(self, id: int) -> dict:
        """Fetch a transaction's details
        
        Keyword arguments:
        :param id: The ID of the transaction

        Return: Transaction respose data dictionary
        """
        
        response = requests.get(
            url = "{}/{}".format(self.api_url, id),
            headers = {
                'Authorization': self.auth
            }
        ).json().get('data')
        return response


    def list(self, **kwargs) -> list:
        """Fetch all transactions perfomermed on your integration.
        
        Optional arguments (kwargs):
        :param perPage (int): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
        :param page (int): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
        :param customer (int): Specify an ID for the customer whose transactions you want to retrieve
        :param terminalid (string): The Terminal ID for the transactions you want to retrieve
        :param status (str): Filter transactions by status ('failed', 'success', 'abandoned')
        :param from (datetime): A timestamp from which to start listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
        :param to (datetime): A timestamp at which to stop listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
        :param amount (int): Filter transactions by amount using the supported currency code

        Return: List of transaction dictionaries
        """
        response = requests.get(
            url = self.api_url,
            headers = {
                'Authorization': self.auth
            },
            params = kwargs
        ).json().get('data')
        return response


    def total(self, **kwagrs) -> dict:
        """Total amount received on your account and other information.
        
        Optional arguments (kwargs):
        :param perPage (int): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
        :param page (int): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
        :param from (datetime): A timestamp from which to start listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
        :param to (datetime): A timestamp at which to stop listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Return: Transaction totals dictionary
        """
        response = requests.get(
            url = "{}/totals".format(self.api_url),
            headers = {
                'Authorization': self.auth
            },
            params = kwagrs
        ).json().get('data')
        return response