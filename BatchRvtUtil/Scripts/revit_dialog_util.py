# -*- coding: utf-8 -*-
#
# Revit Batch Processor
#
# Copyright (c) 2020  Dan Rumery, BVN
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from re import S
import clr
import System

from System import EventHandler
from System.Text import StringBuilder

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs, TaskDialogShowingEventArgs, MessageBoxShowingEventArgs

import exception_util

IDOK = 1
IDCANCEL = 2
IDYES = 6
IDNO = 7
IDCLOSE = 8

def Try(action):
    result = None
    try:
        result = action()
    except:
        pass
    return result

def to_unicode(string):
    try:
        mybytes=bytes(string, 'utf-8')
        unicode_str =mybytes.decode('utf-8')
        return unicode_str
    except UnicodeDecodeError:
        # 如果解码失败，返回一个错误信息
        return "解码错误：无法将字节串转换为Unicode字符串"

def DialogShowingEventHandler(sender, eventArgs, output):
    try:
        dialogResult = IDOK
        msg = StringBuilder()
        msg.AppendLine()
        msg.AppendLine("Dialog box shown:")
        msg.AppendLine()
        if isinstance(eventArgs, TaskDialogShowingEventArgs):
            output("DialogShowingEventHandler Exec")        
            eventArgsMessageutf8 = to_unicode(eventArgs.Message)
            eventArgsDialogIdutf8 = to_unicode(eventArgs.DialogId)
            msg.AppendLine("\tMessage: " + eventArgsMessageutf8)
            if eventArgsDialogIdutf8 == "TaskDialog_Missing_Third_Party_Updater":
                dialogResult = 1001 # Continue working with the file.
            elif eventArgsDialogIdutf8 == "TaskDialog_Location_Position_Changed":
                dialogResult = 1002 # Do not save.
            elif eventArgsDialogIdutf8 == "TaskDialog_Unresolved_References":
                dialogResult = 1002 # Do not save.
                output("dialogResult = 1002")        

            elif eventArgsDialogIdutf8 == "TaskDialog_Save_File":
                dialogResult = 1002 # Do not save.
        elif isinstance(eventArgs, MessageBoxShowingEventArgs):
            msg.AppendLine("\tMessage: " + eventArgsMessageutf8)
            msg.AppendLine("\tDialogType: " + to_unicode(eventArgs.DialogType))
        dialogId = Try(lambda: eventArgsDialogIdutf8) # Available on DialogBoxShowingEventArgs in Revit 2017+
        if dialogId is not None:
            msg.AppendLine("\tDialogId: " + to_unicode(dialogId))
        helpId = Try(lambda: eventArgs.HelpId) # No longer available in Revit 2018+
        if helpId is not None:
            msg.AppendLine("\tHelpId: " + to_unicode(helpId))
        output(msg.ToString())
        output("eventArgs.OverrideResult(dialogResult)")
        eventArgs.OverrideResult(dialogResult)
    except Exception, e:
        errorMsg = StringBuilder()
        errorMsg.AppendLine()
        errorMsg.AppendLine("Caught exception in dialog event handler!")
        errorMsg.AppendLine("Exception message: " + e.message)
        output(errorMsg.ToString())
        exception_util.LogOutputErrorDetails(e, output)
    return

def WithDialogBoxShowingHandler(uiapp, action, output):
    result = None
    dialogShowingEventHandler = (
            EventHandler[DialogBoxShowingEventArgs](
                    lambda sender, eventArgs: DialogShowingEventHandler(sender, eventArgs, output)
                )
        )
    uiapp.DialogBoxShowing += dialogShowingEventHandler
    try:
        result = action()
    finally:
        uiapp.DialogBoxShowing -= dialogShowingEventHandler
    return result

