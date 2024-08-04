import bpy
from ..common import *


class SelectTargetBoneOperator(bpy.types.Operator):
    """
    選択中のボーンをアーマチュアに保存されたボーンを選択するオペレーター
    """

    bl_idname: str = "bone_merger.select_target_bone"
    bl_label: str = "対象ボーンを選択"

    def execute(self, context: bpy.types.Context) -> set:
        """オペレーターの処理"""

        # context.active_object が None であれば中止
        if context.active_object is None:
            report_error(self, msg_not_armature)
            return op_result_cancelled

        # アーマチュアを取得
        arm = get_armature_object(context.active_object)

        # 選択中のオブジェクトの型チェック
        if arm is None or arm.type != type_armature:
            report_error(self, "The selected object is not an armature.")
            return op_result_cancelled

        # 現在のモードが ポーズモード か アーマチュア編集モード でなければ、アーマチュアを選択してアーマチュア編集モードに変更
        if context.mode not in {mode_edit_armature, mode_pose}:
            bpy.ops.object.mode_set(mode=mode_object)
            bpy.ops.object.select_all(action=action_deselect)
            context.view_layer.objects.active = arm
            bpy.ops.object.mode_set(mode=mode_edit)

        # 保存されているボーンリストを取得
        target_bones = arm.get(dict_key_target_bones, [])

        # ボーンを非選択状態にする
        bpy.ops.armature.select_all(action=action_deselect)

        if context.mode == mode_edit_armature:

            # target_bones の名前と一致するボーンを列挙
            editable_bones: list[bpy.types.EditBone] = [bone for bone in cast_to_armature(arm.data).edit_bones if bone.name in target_bones]

            # ボーンを選択状態にする
            for bone in editable_bones:
                bone.select = True

        else:

            # target_bones の名前と一致するボーンを列挙
            pose_bones: list[bpy.types.PoseBone] = [bone for bone in arm.pose.bones if bone.name in target_bones]

            # ボーンを選択状態にする
            for bone in pose_bones:
                bone.bone.select = True

        return op_result_finished

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        """メニューから呼び出された際の処理"""

        return self.execute(context)
