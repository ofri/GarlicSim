
import math

import wx
import wx.lib.agw.piectrl as piectrl
import garlicsim_wx

from ... import prisoner


class StateViewer(piectrl.PieCtrl, garlicsim_wx.widgets.WorkspaceWidget):
    def __init__(self, frame):
        piectrl.PieCtrl.__init__(self, frame)
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        color_dict = {
            prisoner.Angel: wx.NamedColor("White"),
            prisoner.Asshole: wx.NamedColor("Black"),
            prisoner.Smarty: wx.NamedColor("Blue")
        }
        
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, True, 'Arial')
        self.GetLegend().SetLabelFont(font)
        self.SetAngle(math.pi)
    
        self.pie_part_dict = {}
        for player_type in prisoner.player_types:
            part = piectrl.PiePart()
            part.SetLabel(player_type.__name__)
            part.SetValue(1)
            part.SetColour(color_dict[player_type])
            self._series.append(part)
            self.pie_part_dict[player_type] = part
            
        self.gui_project.active_node_changed_emitter.add_output(
            lambda: self.show_state(self.gui_project.active_node.state)
        )
            
    def show_state(self, state):
        for player_type in prisoner.player_types:
            part = self.pie_part_dict[player_type]
            value = prisoner.how_many_players_of_certain_type(
                state.player_pool,
                player_type
            )
            part.SetValue(value)
