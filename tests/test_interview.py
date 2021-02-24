import pandas as pd
from interview import providers

providers_mock = pd.DataFrame({
    'id': ['1234', '2345'],
    'email_x': [None, 'def@gmail.com'],
    'email_y': ['abc@gmaiml0.com', 'qwe@gmail.com'],    
})

def test_clean_email():
    clean_emails = providers_mock.apply(providers.clean_email, 1)

    assert 'email' in clean_emails.columns
    assert clean_emails['email'].to_list() == ['abc@gmaiml0.com', 'def@gmail.com']