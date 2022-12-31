"""
通知判定モジュール.
"""
import pandas
import datetime

def main():
	return

def JudgeNotfyCond(defineNotfyList:list):
	for defineNotfy in defineNotfyList:
		# 判定する銘柄の株価ファイルを開く.
		stockPriceDf = pandas.read_csv(defineNotfy.brandCode + ".csv", index_col=0, header=0)

		# 判定する種別の値の開始日と終了日の価格を取得する.
		dateStartStr = ConvertDateToString(defineNotfy.dateStart)
		dateStartStr = SearchNearDate(dateStartStr, stockPriceDf.index.values)
		dateEndStr = ConvertDateToString(defineNotfy.dateEnd)
		dateEndStr = SearchNearDate(dateEndStr, stockPriceDf.index.values)

		try:
			priceStart = stockPriceDf.at[dateStartStr, defineNotfy.compTarget]
			priceEnd = stockPriceDf.at[dateEndStr, defineNotfy.compTarget]
		except:
			print("通知判定に利用する価格の取得に失敗したためプログラムを終了します。")
			return
		
		# 比率を計算して、通知条件に合致するか判定する.
		if defineNotfy.rateChange > 1:
			# 変動率が1より大きい場合、計算結果が変動率を上回った場合に通知する.
			if defineNotfy.rateChange <= (priceEnd / priceStart):
				defineNotfy.isNotfyFlag = True
		elif defineNotfy.rateChange < 1:
			# 変動率が1より小さい場合、計算結果が変動率を下回った場合に通知する.
			if defineNotfy.rateChange >= (priceEnd / priceStart):
				defineNotfy.isNotfyFlag = True
		else:
			# 変動率が1の設定の場合は何もしない.
			pass
	return

def SearchNearDate(pointDateStr:str, dateStrList:list)->str:
	retDate = pointDateStr
	if not(pointDateStr in dateStrList):
		compDate = ConvertStringToDate(pointDateStr)
		for dateStr in dateStrList:
			retDate = ConvertStringToDate(dateStr)
			if compDate > retDate:
				retDate = ConvertDateToString(retDate)
				break
	return retDate

def ConvertDateToString(date:datetime.date)->str:
	return str(date.year) + "-" + str(date.month) + "-" + str(date.day)

def ConvertStringToDate(date:str)->datetime.date:
	dateList = date.split("-", 3)
	return datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))

if __name__ == "__main__":
	main()