# Script converts CSV to IIF format.

import os
import sys, traceback, re

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

account = "Credit Card"
default = "Uncleared Transactions"


def error(trans):
    sys.stderr.write("%s\n" % trans)
    traceback.print_exc(None, sys.stderr)


def main(input_file_name):
    input_file = open(os.path.join(PROJECT_ROOT, input_file_name), 'r')
    output_file = open(os.path.join(PROJECT_ROOT, input_file_name + '.iif'), 'w')
    head='''!ACCNT	NAME	ACCNTTYPE	DESC
ACCNT	"%s"	EXP	"%s"

!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	NAME	AMOUNT	DOCNUM	MEMO	CLEAR
!SPL	SPLID	TRNSTYPE	DATE	ACCNT	NAME	AMOUNT	DOCNUM	MEMO	CLEAR
!ENDTRNS
'''
    template = '''
TRNS,,%s,%s,"%s","%s","%s","%s","%s",N
SPL,,%s,%s,"%s",,"%s","%s",,N
ENDTRNS''' 
# JPMC Biz Credit card template, 8 fileds in downoaded CSV
# Card	Transaction Date	Post Date	Description	Category	Type	Amount	Memo
    output_file.write(head % (default, default))
    for trans in input_file:
        trans = trans.strip()
        if trans == "":
            continue

        try:
            list = trans.split(',')
            print(len(list))
            print(list)
            assert (len(list) == 8 )
        except:
            error(trans)
            continue
        account1 = default
        try:
            (card, date, pdate, description, category, transtype, amount, memo) = list
        except:
            error(trans)
            continue
        amount = amount.strip('"')
        try:
            amount = float(amount)
        except:
            error(trans)
            continue
        docnum = ''
        transtype = transtype.strip('"')
        transtype = transtype.lstrip("0")
        description = description.strip('"')
        description = description.strip("\n")
        description = description.strip("\r")

        if "Food & Drink" in category:
            category = 'Meals and Entertainment:Food & Drink'
        elif "Bills & Utilities" in category:
            category = 'Utilities:Bills & Utilities'
        elif "Automotive" in category:
            category = 'Automobile Expense:Automotive'
        elif "Gas" in category:
            category = 'Automobile Expense:Gas'
        elif "Office & Shipping" in category:
            category = 'Office Supplies:Office & Shipping'
        elif "Professional Services" in category:
            category = 'Professional Fees:Professional Services'

        if "Payment" in transtype:
            transtype = 'PAYMENT'
        elif "Return" in transtype:
            transtype = 'CCARD REFUND'
        else:
            #name = 'Check ' + transtype
            #docnum = transtype
            transtype = 'CREDIT CARD'
            account1 = category #'Ask My Accountant'
        name = ''
        transact = template % (transtype,date,account,name,amount,docnum,description,transtype,date,account1,-amount,docnum)
        transact = transact.replace(",","\t")
        print(transact)
        output_file.write(transact)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("usage:	python3 convertiif.py numbers.csv")

    main(sys.argv[1])
