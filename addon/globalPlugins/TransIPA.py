# -*- coding:utf-8 -*-
# A part of the NVDA Volume Adjustment add-on
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2024 Cary-rowen <manchen_0528@outlook.com>

import os
import scriptHandler
import globalPluginHandler
import globalCommands
import globalVars
import speechDictHandler
import ui
import addonHandler
addonHandler.initTranslation()


dictFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'IPAData.dic')
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
		description=_("Toggle reporting of Phonetic"), 
gesture="kb:NVDA+Shift+P")
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
