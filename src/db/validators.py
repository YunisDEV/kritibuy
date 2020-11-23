import re
import phonenumbers

email_regex = re.compile("""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$""")

phone_num_validation = lambda num: phonenumbers.is_valid_number(phonenumbers.parse(num,None))

if __name__ == '__main__':
    print(phone_num_validation('+994774043000'))