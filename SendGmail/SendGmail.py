from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import datetime

def main():
	print(CreateMailText("333.jp", datetime.date(2022,12,29), datetime.date(2022,12,30),"Close", 1.1))
	return

def SendGmail(brandCode:str, dateStart:datetime.date, dateEnd:datetime.date, compTarget:str, rateChange:float):
	scopes = ["https://mail.google.com/"]
	creds = Credentials.from_authorized_user_file("token.json", scopes)
	service = build("gmail", "v1", credentials=creds)

	message = MIMEText(CreateMailText(brandCode, dateStart, dateEnd, compTarget, rateChange))
	message["To"] = "kazu.r0304@gmail.com"
	message["From"] = "kazu.r0304@gmail.com"
	message["Subject"] = "[株価通知]" + brandCode
	raw = {"raw": messsage_base64_encode(message)}

	service.users().messages().send(
		userId = "me",
		body = raw
	).execute()
	return

def CreateMailText(brandCode:str, dateStart:datetime.date, dateEnd:datetime.date, compTarget:str, rateChange:float)->str:
	mailText = "銘柄コード:" + brandCode + "\n"
	mailText += "比較期間開始日:" + str(dateStart.year) + str(dateStart.month) + str(dateStart.day) + "\n"
	mailText += "比較期間終了日:" + str(dateEnd.year) + str(dateEnd.month) + str(dateEnd.day) + "\n"
	mailText += "比較対象値:" + compTarget + "\n"
	mailText += "比率:" + str(rateChange) + "\n"
	mailText += "-------------------------------" + "\n"
	mailText += "From NotfyStockPrice"
	return mailText

def messsage_base64_encode(message):
	return base64.urlsafe_b64encode(message.as_bytes()).decode()

if __name__ == "__main__":
	main()