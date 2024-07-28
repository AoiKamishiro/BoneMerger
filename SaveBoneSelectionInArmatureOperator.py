import bpy
from .common import *


class SaveBoneSelectionInArmatureOperator(bpy.types.Operator):
    """
    選択中のボーンをアーマチュアに保存するオペレーター
    """

    bl_idname: str = "bone_merger.save_bone_selection_in_armature"
    bl_label: str = "対象を選択中のボーンに変更"

    def execute(self, context: bpy.types.Context) -> set:
        """オペレーターの処理"""

        # context.active_object が None であれば中止
        if context.active_object is None:
            print(msg_not_armature)
            return {'CANCELLED'}

        # アーマチュアを取得
        arm = get_armature_object(context.active_object)

        # 選択中のオブジェクトの型チェック
        if arm is None or arm.type != type_armature:
            print("The selected object is not an armature.")
            return {'CANCELLED'}

        # 現在のモードが ポーズモード か アーマチュア編集モード でなければ中止
        if context.mode not in {mode_edit_armature, mode_pose}:
            print("The current mode is not POSE or EDIT_ARMATURE.")
            return {'CANCELLED'}

        # 選択されているボーンを取得
        if context.mode == mode_edit_armature:
            bones: list[str] = [bone.name for bone in context.selected_editable_bones]
        else:
            bones: list[str] = [bone.name for bone in context.selected_pose_bones]

        # 選択されているボーンを保存
        print("Selected bones:")
        for bone in bones:
            print(f"  {bone}")
        arm[dict_key_target_bones] = bones

        return {'FINISHED'}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        """メニューから呼び出された際の処理"""

        return self.execute(context)
