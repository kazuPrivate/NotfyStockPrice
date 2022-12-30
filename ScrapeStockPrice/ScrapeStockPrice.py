import pandas_datareader.data as web
import datetime as datetime
import pandas

def main():
	brandCodeList = ["4826.JP", "9104.JP"]
	#取得期間を指定
	start = datetime.date(2022,12,9)
	end = datetime.date(2022,12,12)

	ScrapeStockPriceFromStooq(brandCodeList, start, end)
	SplitBrandStockPriceToCsv()
	return

def ScrapeStockPriceFromStooq(brandCodeList:list, dateStart:datetime.date, dateEnd:datetime.date):
	# 終了日が開始日より若い場合はエラー.
	if dateEnd < dateStart:
		print("株価を取得する期間の終了日は開始日より後の日付を入力してください")

	df = web.DataReader(brandCodeList, 'stooq', start=dateStart, end=dateEnd)
	df.to_csv("ScrapeData.csv")

# スクレイピングした株価のcsvファイルを読み込む.
def SplitBrandStockPriceToCsv():
	stockPriceDf = pandas.read_csv("ScrapeData.csv",index_col = 0, header=[0,1])
	
	# ヘッダー取得.
	attrList = []
	brandList = []
	for header in stockPriceDf.columns.values:
		attrList.append(header[0])
		brandList.append(header[1])
	attrList = list(set(attrList))
	brandList = list(set(brandList))

	# 銘柄毎にcsvファイルを分割する.
	for brandcode in brandList:
		concatedDf = pandas.DataFrame()
		for attribute in attrList:
			workDf = stockPriceDf.loc[:, (attribute, brandcode)]
			workDf.name = attribute
			concatedDf = pandas.concat([concatedDf, workDf], axis=1)
		concatedDf.to_csv(brandcode +".csv")

if __name__ == "__main__":
	main()