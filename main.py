import csv
from bs4 import BeautifulSoup
from datetime import datetime
import re

# extract amount from string
def extract_amount(text):
    match = re.search(r'₹(\d+\.\d+)', text)
    # match = re.search(r'₹(\d+(\.\d{1,2})?)', text)
    print("MATCH->", text)
    
    if match:
        amount = match.group(1)
        return amount
    else:
        # print("AMOUNT->", text)
        return None
    
 # Detect if amount paid or received
def paidOrReceived(str):
    text_lower = str.lower()
    if "paid" in text_lower:
        return "paid"
    elif "sent" in text_lower:
        return "sent"
    elif "received" in text_lower:
        return "received"
    else:
        print("Neither 'Paid' nor 'Received' found in the text")
        return None

# Open the CSV file in append mode
with open("output.csv", "a", newline="") as csv_file:
    writer = csv.writer(csv_file)

    with open("./activity.html", "r") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        writer.writerow(["DATA", "PAID", "SENT", "RECEIVED"])
    for tag in soup.find_all('div', {'class': 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'}):
        text = tag.get_text(strip=True)  # Get the text content of the <div>
        br_tag = tag.find("br")

        # Extract the text after the <br> tag
        if br_tag:
            # print("PRICE", text)
            # -- Yaha tk aaraha hai --
            DateToBeAppended = br_tag.find_next_sibling(string=True)
            # Convert the string to a datetime object
            date_object = datetime.strptime(DateToBeAppended, '%b %d, %Y, %I:%M:%S %p %Z')

            # Check if the month is November
            if date_object.month == 10 and date_object.year == 2023:
                amountToBeAppended = extract_amount(text)  # Extract the amount from the text
                # print("AMOUNT->", amountToBeAppended )
                if amountToBeAppended is not None:

                    isPaid = paidOrReceived(text)
                    if isPaid == "paid":
                        data = [DateToBeAppended, amountToBeAppended, "", ""] 
                    elif isPaid == "sent":
                        data = [DateToBeAppended, "", amountToBeAppended, ""]
                    elif isPaid == "received":
                        data = [DateToBeAppended, "" , "", amountToBeAppended]
                    # print(data)
                    writer.writerow(data)  # Write the data to the CSV file
            # else:
            #     print("Date is out of selected Date")



"""
    get DATE ->
    get amount ->
    Check if Paid or received
    if paid
        data = [DATE, amount_paid, "", ""] 
    elif received
        # data = [DATE, "", amount_received, ""] 
    elif sent
        # data = [DATE, "", "", sent] 

"""