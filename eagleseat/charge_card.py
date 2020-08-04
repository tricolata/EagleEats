from authorizenet import apicontractsv1
from authorizenet.apicontrollers import*
from decimal import*



def charge(card_number, expiration_date, amount, merchant_id):
	merchantAuth = apicontractsv1.merchantAuthenticationType()
	merchantAuth.name = '4K24xbCW'
	merchantAuth.transactionKey = '8m39rKgQ92C4MRvx'

	creditCard = apicontractsv1.creditCardType()
	creditCard.cardNumber = card_number
	creditCard.expirationDate = expiration_date

	payment = apicontractsv1.paymentType()
	payment.creditCard = creditCard

	transactionrequest = apicontractsv1.transactionRequestType()
	transactionrequest.transactionType ="authCaptureTransaction"
	transactionrequest.amount = Decimal(amount)
	transactionrequest.payment = payment


	createtransactionrequest = apicontractsv1.createTransactionRequest()
	createtransactionrequest.merchantAuthentication = merchantAuth
	createtransactionrequest.refId = merchant_id

	createtransactionrequest.transactionRequest = transactionrequest
	createtransactioncontroller = createTransactionController(createtransactionrequest)
	createtransactioncontroller.execute()

	response = createtransactioncontroller.getresponse()

	if (response.messages.resultCode=="Ok"):
		return (True, "Transaction ID : %s" % response.transactionResponse.transId)
	else:
		return (False, "response code: %s" % response.messages.resultCode)

'''
#Custom transaction data - feel free to define your own!
card_number = "4111111111111111"
expiration_date = "2020-12"
amount = '13.37'
merchant_id = "Pied-Piper"

# Invoke the charge function to execute the transaction
response=charge(card_number, expiration_date, amount, merchant_id)

print(response)
'''
