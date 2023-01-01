"""
NotfyStockPrice メインモジュール.
"""
import datetime as datetime
import schedule
import time

from ReadSettingFile import ReadSettingFile
from ScrapeStockPrice import ScrapeStockPrice
from JudgeNotfyCond import JudgeNotfyCond
from SendGmail import SendGmail

def main():
	# 毎朝7時に通知処理を実行する.
	schedule.every().day.at("07:00").do(NotfyStockPrice)
	while True:
		schedule.run_pending()
		time.sleep(10)
	return

def NotfyStockPrice():
	brandCodeList = []

	# 設定ファイル読み込み.
	settingFileData = ReadSettingFile.NotfyStockPriceConfig()
	for brandData in settingFileData.brandDataList:
		brandCodeList.append(brandData.code)

	#取得期間を指定
	dateStart = datetime.date.today() - datetime.timedelta(days=21)
	dateEnd = datetime.date.today() - datetime.timedelta(days=1)

	# 株価を取得してcsvに出力.
	if True:
		logTimeStart = time.time()
		ScrapeStockPrice.ScrapeStockPriceFromStooq(brandCodeList, dateStart, dateEnd)
		print("ScrapeTime")
		print(time.time() - logTimeStart)
		ScrapeStockPrice.SplitBrandStockPriceToCsv()

	# 通知定義に合致したか判定する.
	JudgeNotfyCond.JudgeNotfyCond(settingFileData.defineNotfyList)
	
	# 通知フラグが立った条件はメールの送信を行う.
	for defineNotfy in settingFileData.defineNotfyList:
		if defineNotfy.isNotfyFlag:
			SendGmail.SendGmail(defineNotfy.brandCode, defineNotfy.dateStart, defineNotfy.dateEnd, defineNotfy.compTarget, defineNotfy.rateChange)
	return

if __name__ == "__main__":
	main()