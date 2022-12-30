"""
設定ファイル読み込みモジュール.
"""
import openpyxl
import datetime
import pandas

if __name__ == "__main__":
	import Brand
	import DefineNotfy
else:
	from . import Brand
	from . import DefineNotfy

# 設定ファイルの各定義.
SETTING_FILE_NAME = "Setting.xlsx"	# 設定ファイル名.

### 銘柄リストシート.
BRAND_SHEET_NAME = "BrandList"		# シート名.
# 列名.
BRAND_SHEET_COL_CODE = "銘柄コード"
BRAND_SHEET_COL_NAME = "銘柄名"

### 通知定義シート.
NOTFY_SHEET_NAME = "DefineNotfy"	# シート名.
# 列名.
NOTFY_SHEET_COL_CODE = "銘柄コード"
NOTFY_SHEET_COL_START = "期間(開始)"
NOTFY_SHEET_COL_END = "期間(終了)"
NOTFY_SHEET_COL_COMP_TARGET = "比較対象"
NOTFY_SHEET_COL_CHANGE_RATE = "変動率"

### メーリングリストシート.
MAIL_SHEET_NAME = "Mail"	# シート名.
# 列名.
MAIL_SHEET_COL_NOTFY_ADDRESS = "通知先メールアドレス"

class NotfyStockPriceConfig:
	""" 設定ファイルクラス """
	def __init__(self) -> None:

		self.brandDataList = ReadSettingFileBrandList()
		self.defineNotfyList = ReadSettingFileDefineNotfy()
		self.mailList = ReadSettingFileMail()

def main():
	test = NotfyStockPriceConfig()

	for index in test.brandDataList:
		print(index.name)
		print(index.code)

	for index in test.defineNotfyList:
		print(index.brandCode)
		print(index.dateStart)
		print(index.dateEnd)
		print(index.compTarget)
		print(index.rateChange)
	
	for index in test.mailList:
		print(index)
	return

def ReadSettingFileBrandList()->list:
	""" "BrandList"シート読み込み関数.

	Returns:
		list: 銘柄データのリスト.
	"""
	brandDataList = []
	brandListDf = pandas.read_excel(SETTING_FILE_NAME, sheet_name=BRAND_SHEET_NAME)

	for index, rows in brandListDf.iterrows():
		brandCode = rows[BRAND_SHEET_COL_CODE]
		brandName = rows[BRAND_SHEET_COL_NAME]
		
		# 取得したデータでインスタンスを生成してメンバー変数に格納.
		brandData = Brand.StockPriceBrand(brandName, brandCode)
		brandDataList.append(brandData)
	
	return brandDataList

def ReadSettingFileDefineNotfy()->list:
	""" "DefineNotfy"シート読み込み関数.

	Returns:
		list: 通知定義データのリスト.
	"""
	defineNotfyDataList = []
	defineNotfyListDf = pandas.read_excel(SETTING_FILE_NAME, sheet_name=NOTFY_SHEET_NAME)

	for index, rows in defineNotfyListDf.iterrows():
		brandCode = rows[NOTFY_SHEET_COL_CODE]
		dateStart = ConvertStringToDate(rows[NOTFY_SHEET_COL_START])
		dateEnd = ConvertStringToDate(rows[NOTFY_SHEET_COL_END])
		compTarget = rows[NOTFY_SHEET_COL_COMP_TARGET]
		rateChange = rows[NOTFY_SHEET_COL_CHANGE_RATE]
		
		# 取得したデータでインスタンスを生成してメンバー変数に格納.
		defineNotfyData = DefineNotfy.DefineNotfy(brandCode, dateStart, dateEnd, compTarget, rateChange)
		defineNotfyDataList.append(defineNotfyData)
	
	return defineNotfyDataList

def ConvertStringToDate(dateData:str | datetime.datetime)->datetime.date:
	""" 相対的な日付を示す文字列を日付型に変換
		引数に日時型が入ってきたら、日付型に変換

	Args:
		dateData (str | datetime.datetime): 変換する文字列 or 日付

	Returns:
		datetime.date: 変換した日付
	"""
	retData = 0

	if type(dateData) is str:
		if dateData == "today":
			retData = datetime.date.today()
		if "day_ago" in dateData:
			agoDays = str(dateData).replace("day_ago", "")
			retData = datetime.date.today() - datetime.timedelta(days=int(agoDays))
	elif type(dateData) is datetime.datetime:
		retData = datetime.date(dateData.year, dateData.month, dateData.day)
	else:
		retData = dateData

	return retData

def ReadSettingFileMail()->list:
	""" "Mail"シート読み込み関数.

	Returns:
		list: メールのリスト.
	"""
	mailList = []
	mailListDf = pandas.read_excel(SETTING_FILE_NAME, sheet_name=MAIL_SHEET_NAME)

	for index, rows in mailListDf.iterrows():
		mailAddress = rows[MAIL_SHEET_COL_NOTFY_ADDRESS]

		mailList.append(mailAddress)
	
	return mailList

if __name__ == "__main__":
	main()