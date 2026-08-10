from faker import Faker
from collections import defaultdict
# from PIL import Image
# from io import BytesIO
{'a': ['aba', 'add_provider', 'address', 'administrative_unit', 'am_pm', 'android_platform_token', 'ascii_company_email', 'ascii_email', 'ascii_free_email', 'ascii_safe_email'],
 'b': ['bank', 'bank_country', 'basic_phone_number', 'bban', 'binary', 'boolean', 'bothify', 'bs', 'building_number'],
 'c': ['cache_pattern', 'catch_phrase', 'century', 'chrome', 'city', 'city_prefix', 'city_suffix', 'color', 'color_hsl', 'color_hsv', 'color_name', 'color_rgb', 'color_rgb_float', 'company', 'company_email', 'company_suffix', 'coordinate', 'country', 'country_calling_code', 'country_code', 'credit_card_expire', 'credit_card_full', 'credit_card_number', 'credit_card_provider', 'credit_card_security_code', 'cryptocurrency', 'cryptocurrency_code', 'cryptocurrency_name', 'csv', 'currency', 'currency_code', 'currency_name', 'currency_symbol', 'current_country', 'current_country_code'],
 'd': ['date', 'date_between', 'date_between_dates', 'date_object', 'date_of_birth', 'date_this_century', 'date_this_decade', 'date_this_month', 'date_this_year', 'date_time', 'date_time_ad', 'date_time_between', 'date_time_between_dates', 'date_time_this_century', 'date_time_this_decade', 'date_time_this_month', 'date_time_this_year', 'day_of_month', 'day_of_week', 'del_arguments', 'dga', 'doi', 'domain_name', 'domain_word', 'dsv'],
 'e': ['ean', 'ean13', 'ean8', 'ein', 'email', 'emoji', 'enum'],
 'f': ['factories', 'file_extension', 'file_name', 'file_path', 'firefox', 'first_name', 'first_name_female', 'first_name_male', 'first_name_nonbinary', 'fixed_width', 'format', 'free_email', 'free_email_domain', 'future_date', 'future_datetime'],
 'g': ['generator_attrs', 'get_arguments', 'get_formatter', 'get_providers', 'get_words_list'],
 'h': ['hex_color', 'hexify', 'hostname', 'http_method', 'http_status_code'],
 'i': ['iana_id', 'iban', 'image', 'image_url', 'internet_explorer', 'invalid_ssn', 'ios_platform_token', 'ipv4', 'ipv4_network_class', 'ipv4_private', 'ipv4_public', 'ipv6', 'isbn10', 'isbn13', 'iso8601', 'items', 'itin'],
 'j': ['job', 'job_female', 'job_male', 'json', 'json_bytes'], 
 'l': ['language_code', 'language_name', 'last_name', 'last_name_female', 'last_name_male', 'last_name_nonbinary', 'latitude', 'latlng', 'lexify', 'license_plate', 'linux_platform_token', 'linux_processor', 'local_latlng', 'locale', 'locales', 'localized_ean', 'localized_ean13', 'localized_ean8', 'location_on_land', 'longitude'], 
 'm': ['mac_address', 'mac_platform_token', 'mac_processor', 'md5', 'military_apo', 'military_dpo', 'military_ship', 'military_state', 'mime_type', 'month', 'month_name', 'msisdn'], 
 'n': ['name', 'name_female', 'name_male', 'name_nonbinary', 'nic_handle', 'nic_handles', 'null_boolean', 'numerify'],
 'o': ['opera', 'optional'],
 'p': ['paragraph', 'paragraphs', 'parse', 'passport_dates', 'passport_dob', 'passport_full', 'passport_gender', 'passport_number', 'passport_owner', 'password', 'past_date', 'past_datetime', 'phone_number', 'port_number', 'postalcode', 'postalcode_in_state', 'postalcode_plus4', 'postcode', 'postcode_in_state', 'prefix', 'prefix_female', 'prefix_male', 'prefix_nonbinary', 'pricetag', 'profile', 'provider', 'providers', 'psv', 'pybool', 'pydecimal', 'pydict', 'pyfloat', 'pyint', 'pyiterable', 'pylist', 'pyobject', 'pyset', 'pystr', 'pystr_format', 'pystruct', 'pytimezone', 'pytuple'],
 'r': ['random', 'random_choices', 'random_digit', 'random_digit_above_two', 'random_digit_not_null', 'random_digit_not_null_or_empty', 'random_digit_or_empty', 'random_element', 'random_elements', 'random_int', 'random_letter', 'random_letters', 'random_lowercase_letter', 'random_number', 'random_sample', 'random_uppercase_letter', 'randomize_nb_elements', 'rgb_color', 'rgb_css_color', 'ripe_id'],
 's': ['safari', 'safe_color_name', 'safe_domain_name', 'safe_email', 'safe_hex_color', 'sbn9', 'secondary_address', 'seed', 'seed_instance', 'seed_locale', 'sentence', 'sentences', 'set_arguments', 'set_formatter', 'sha1', 'sha256', 'simple_profile', 'slug', 'ssn', 'state', 'state_abbr', 'street_address', 'street_name', 'street_suffix', 'suffix', 'suffix_female', 'suffix_male', 'suffix_nonbinary', 'swift', 'swift11', 'swift8'],
 't': ['tar', 'text', 'texts', 'time', 'time_delta', 'time_object', 'time_series', 'timezone', 'tld', 'tsv'], 
 'u': ['unique', 'unix_device', 'unix_partition', 'unix_time', 'upc_a', 'upc_e', 'uri', 'uri_extension', 'uri_page', 'uri_path', 'url', 'user_agent', 'user_name', 'uuid1', 'uuid4', 'uuid7'], 
 'v': ['vin'],
 'w': ['weights', 'windows_platform_token', 'word', 'words'],
 'x': ['xml'],
 'y': ['year'], 
 'z': ['zip', 'zipcode', 'zipcode_in_state', 'zipcode_plus4']}
fake = Faker()
# print(dir(fake))
# print(fake.name(),fake.domain_name())
# print(fake.random_number(digits=5))
print(fake.company_email())
# Image.open(BytesIO(fake.image())).show()