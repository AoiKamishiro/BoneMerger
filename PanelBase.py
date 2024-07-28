import bpy


class PanelBase(bpy.types.Panel):
    """
    Blenderのパネルを作成するための基底クラス
    """
    bl_category = "BoneMerger"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
