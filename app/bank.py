import humanize
import plaid
import requests

from . import settings


# Create plaid client.
client = plaid.Client(client_id=settings.PLAID_CLIENT_ID,
                      secret=settings.PLAID_SECRET,
                      public_key=settings.PLAID_PUBLIC_KEY,
                      environment=settings.PLAID_ENV
                      )

plaid_data = {
    'client_id': settings.PLAID_CLIENT_ID,
    'secret': settings.PLAID_SECRET,
    'access_token': settings.PLAID_ACCESS_TOKEN
}


def _get_balance(account_type, account_mask):
    '''
    Fetch account data and return the balance.
    '''

    error_msg = 'Error fetching account balance.'
    response = requests.post(settings.PLAID_URL, json=plaid_data)

    # Check that status code is valid.
    if response.status_code not in [200, 201]:
        return error_msg, '{} - {}'.format(error_msg, response.status_code)

    # Get accounts.
    account_list = response.json()['accounts']

    try:
        # Get account based on account mask.
        account = [
            acc for acc in account_list
            if acc.get('mask') == account_mask
        ][0]

        # Get balance amount.
        balance = account['balances']['available']
        balance = '{:.2f}'.format(balance)

        message = 'Balance in {} account is ${}.'.format(
            account_type, humanize.intcomma(balance)
        )
        return message, message
    except (IndexError, KeyError) as e:
        return error_msg, '{} - ({}) {}'.format(error_msg, type(e), e)


def get_savings_balance():
    return _get_balance('savings', settings.SAVINGS_ACCOUNT_MASK)


def get_checking_balance():
    return _get_balance('checking', settings.CHECKING_ACCOUNT_MASK)
