"""
通知定義クラス.
"""
import datetime

class DefineNotfy:
	def __init__(self, brandCode:str, dateStart:datetime.date, dateEnd:datetime.date, compTarget:str, rateChange:float) -> None:
		""" 通知定義コンストラクタ

		Args:
			brandCode (str): 銘柄コード.
			dateStart (datetime.date): 判定する開始日.
			dateEnd (datetime.date): 判定する終了日.
			compTarget (str): 比較対象.
			rateChange (float): 株価の変動率.
		"""
		self.brandCode = brandCode
		self.dateStart = dateStart
		self.dateEnd = dateEnd
		self.compTarget = compTarget
		self.rateChange = rateChange
		self.isNotfyFlag = False