# Author: Eureka <manchen_0528@outlook.com>


import os
import scriptHandler
import globalPluginHandler
import globalCommands
import globalVars
import speechDictHandler
import ui

dictFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IPAData.dic")
speechDict = speechDictHandler.SpeechDict()
transIPA = False

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = globalCommands.SCRCAT_SPEECH

	def __init__(self):
		super().__init__()
		global speechDict, dictFile
		speechDict.load(dictFile)

	def terminate(self):
		transOff()
		global speechDict
		speechDict = None


	@scriptHandler.script(
		description=_("切换读出盲文音标的开关"), 
gesture=_("kb:NVDA+Shift+P"))
	def script_toggle(self, gesture):
		if not globalVars.speechDictionaryProcessing:
			return
		if transIPA:
			transOff()
			ui.message(_("off"))
		else:
			transOn()
			ui.message(_("on"))

def transOn():
	global transIPA
	speechDictHandler.dictionaries["temp"].extend(speechDict)
	transIPA = True

def transOff():
	global transIPA
	for entry in speechDict:
		if entry in speechDictHandler.dictionaries["temp"]:
			speechDictHandler.dictionaries["temp"].remove(entry)
	transIPA = False
