class BottomLine(object):
	def __init__(self, providers=None):
		self.providerList = list()
		
		if providers is not None:
			self.providerList.extend(providers)
		
		self.providerIndex = -1
		self.itemIndex = 0
		self.currentItemList = None
		
	def add_provider(self, bottomLineProvider):
		'''This method expects an object that inherits from BottomLineProvider
		   or implements a method named get_bottom_line_info() that returns 
		   a list of BottomLineItem objects'''
		self.providerList.append(bottomLineProvider)
		
	def get_next_item(self):
		if len(self.providerList) < 1:
			return None
		
		#Check for more items from current provider 
		if self.currentItemList is not None:
			self.itemIndex += 1
			
			if self.itemIndex < len(self.currentItemList):
				#Get the next item from the current list
				return self.currentItemList[self.itemIndex]
			else:
				#Get the info from the next provider
				return self._search_for_item()
		else:
			return self._search_for_item()
	
	def _search_for_item(self):
		#Reset itemIndex and move to the next provider
		self.itemIndex = 0
		self.providerIndex = (self.providerIndex + 1) % len(self.providerList)
		
		self.currentItemList = self.providerList[self.providerIndex].get_bottom_line_info()
		
		startingPoint = self.providerIndex
		
		#Don't return an empty item if we can help it
		while self.currentItemList is None or len(self.currentItemList) == 0:
			self.providerIndex = (self.providerIndex + 1) % len(self.providerList)
		
			self.currentItemList = self.providerList[self.providerIndex].get_bottom_line_info()
			
			#Stop searching if we reached the starting point, otherwise it will loop forever :/
			if self.providerIndex == startingPoint:
				return None
		
		#Everything is properly updated, so return the first item of the new item list
		return self.currentItemList[self.itemIndex]
			
		
class BottomLineProvider(object):
	def get_bottom_line_info(self):
		'''The default implementation is to return all of the fields
		   along with their values. When overridden in child classes, it
		   is expected to return a list of BottomLineItem objects'''
		itemsList = list()
		
		fields = vars(self)
		for fieldName in fields:
			item = BottomLineItem(fieldName, fields[fieldName])
			itemsList.append(item)
			
		return itemsList
				

class BottomLineItem(object):
	def __init__(self, header, details):
		self.header = header
		self.details = details		

