"""
銘柄クラス
"""

class StockPriceBrand:
	def __init__(self, brandName:str, brandCode:str) -> None:
		""" 銘柄クラス コンストラクタ.

		Args:
			brandName (str): 銘柄名.
			brandCode (int): 銘柄コード.
		"""
		self.name = brandName
		self.code = brandCode