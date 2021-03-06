from enum import Enum

class CustomerMessages:
    INVALID_CUTOMER_DATA_UPDATE = 'Invalid Data To Update'
    INVALID_CUSTOMER_DATA_PATCH = 'Invalid Data To Patch'
    SINGUP_UNSUCCESSFULL = 'Sign Up Unsuccessfull'
    ACCOUNT_DELETED = 'Account Deleted'
    PASSWORD_CHANGED = 'Password Successfully Changed'
    INVALID_INPUTS = 'Invalid Inputs'
    INVALID_DATA = 'Invalid Data'
    ACCOUNT_NOT_FOUND = 'Account Not Found'
    TOKEN_NOT_FOUND = 'Token Not Found'
    PASSWORD_RESET = 'Password Reset Successfull'
    PASSOWORD_RESET_INVALID= 'Password Reset Not Valid'
    LOGOUT = 'Logged Out Successfully'
    USER_ALREADY_A_MERCHANT = 'User Is Already A Merchant'
    MERCHANT_CREATED = "Merchant Account Successfully Created"
    EMAIL_VERIFIED = 'Email Successfully Verified'
    LIST_OF_CUSTOMERS = 'List Of All Customers'
    CUSTOMER_DETAILS = 'Customer Details'
    INVALID_TOKEN = 'Invalid Token'
    VERIFICATION_EMAIL_RESENT = 'Verification Email Resent'
    PASSWORD_NO_MATCH = 'Passwords Do Not Match'
    EMAIL_NOT_VERIFIED = 'Email Not Verified'
    INVALID_OLD_PASSWORD = 'Old Password Is Invalid'
    NOT_LOGGED_OUT = 'Not Logged out'