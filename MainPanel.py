import bpy
from .common import *
from .PanelBase import PanelBase
from .SaveBoneSelectionInArmatureOperator import SaveBoneSelectionInArmatureOperator
from .MergeBoneWeightToParentOperator import MergeBoneWeightToParentOperator


class MainPanel(PanelBase):
    """
    マージを行うボーンを設定するパネル
    """

    bl_idname: str = "BONE_MERGER_PT_MAIN_PANEL"
    bl_label: str = "Main"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout

        # context.active_object が None であれば中止
        if context.active_object is None:
            layout.label(text=msg_not_armature)
            return

        # アーマチュアを取得
        arm = get_armature_object(context.active_object)

        # アーマチュアが取得できなかった場合は中止
        if arm is None:
            layout.label(text=msg_not_armature)
            return

        # update_bone_list を呼び出すボタンを作成
        layout.operator(SaveBoneSelectionInArmatureOperator.bl_idname, text=SaveBoneSelectionInArmatureOperator.bl_label)

        # copy_objects_to_new_collection を呼び出すボタンを作成
        layout.operator(MergeBoneWeightToParentOperator.bl_idname, text=MergeBoneWeightToParentOperator.bl_label)

        # 保存されているボーンリストを取得
        target_bones = arm.get(dict_key_target_bones, [])

        # foldout の作成
        row = layout.row()
        row.alignment = 'LEFT'
        row.prop(context.scene, prop_show_target_bones, icon=icon_tria_down if context.scene.get(prop_show_target_bones) else icon_tria_right, emboss=False)

        if context.scene.get(prop_show_target_bones):
            box = layout.box()
            for bone in target_bones:
                box.label(text=bone)
