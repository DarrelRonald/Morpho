# Morpho: A plugin to write Envimet 2.5D models.
# This file is part of Morpho project.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with Morpho project; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Construct an Inx 2.5D Model.
-
You can connect many envimet objects to it.
-
Icon by Envimet INX for Sketchup.
    Args:
        _inx_workspace: Workspace of your current project.
        _inx_grid: Inx Grid.
        _inx_location: Inx Location.
        _inx_objects_: Connect envimet objects [list]
        . inx_building;
        . inx_plant3d;
        . inx_plant2d;
        . inx_receptor;
        . inx_soil;
        . inx_source;
        . inx_terrain.
        _run_it: Set it to 'True' to create INX Model.
    
    Returns:
        read_me: Message for users.
        inx_model: INX Model.
        -
        Connect it to 'Morpho Write Model' to save *.inx file on your machine.
"""

ghenv.Component.Name = "Morpho Building"
ghenv.Component.NickName = "morpho_building"
ghenv.Component.Category = "Morpho"
ghenv.Component.SubCategory = "1 || IO"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import scriptcontext as sc
import os
import sys
import clr
##################Envimet INX####################
from System.Collections.Generic import *
try:
    user_path = os.getenv("APPDATA")
    sys.path.append(os.path.join(user_path, "Morpho"))
    clr.AddReference("Morpho25.dll")
    from Morpho25.Settings import Model
    from Morpho25.Utility import EnvimetUtility
    from Morpho25.Geometry import *
    
except ImportError as e:
    raise ImportError("\nFailed to import Morpho: {0}\n\nCheck your 'Morpho' folder in {1}".format(e, os.getenv("APPDATA")))
################################################
ghenv.Component.Message = "1.0.0 2.5D"

def main():
    
    if _inx_grid and _inx_location and _inx_workspace and _run_it:
        
        model = Model(_inx_grid, _inx_location, _inx_workspace)
        
        building = []
        plant3d = []
        plant2d = []
        receptor = []
        soil = []
        source = []
        terrain = []
        
        if _inx_objects_:
            for obj in _inx_objects_:
                if (type(obj) == Building):
                    building.append(obj)
                if (type(obj) == Plant3d):
                    plant3d.append(obj)
                if (type(obj) == Plant2d):
                    plant2d.append(obj)
                if (type(obj) == Receptor):
                    receptor.append(obj)
                if (type(obj) == Soil):
                    soil.append(obj)
                if (type(obj) == Source):
                    source.append(obj)
                if (type(obj) == Terrain):
                    terrain.append(obj)
        
        if building: model.BuildingObjects = List[Building](building)
        if plant3d: model.Plant3dObjects = List[Plant3d](plant3d)
        if plant2d: model.Plant2dObjects = List[Plant2d](plant2d)
        if receptor: model.ReceptorObjects = List[Receptor](receptor)
        if soil: model.SoilObjects = List[Soil](soil)
        if source: model.SourceObjects = List[Source](source)
        if terrain: model.TerrainObjects = List[Terrain](terrain)
        
        model.Calculation()
        
        return model
    else:
        return

inx_model = main()
if not inx_model: print("Please, connect _inx_workspace, _inx_grid, _inx_location and set _run_it to 'True'.")