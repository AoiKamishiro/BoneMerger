import bpy
from ..common import *


class RemoveNonExistentBoneWeightsOperator(bpy.types.Operator):
    """
    存在しないボーンのウェイトを削除するオペレーター
    """

    bl_idname: str = "bone_merger.remove_non_existent_bone_weights"
    bl_label: str = "ボーンのない頂点グループの削除"

    def execute(self, context: bpy.types.Context) -> set:
        """オペレーターの処理"""

        # オブジェクトモードに変更
        bpy.ops.object.mode_set(mode=mode_object)

        # context.active_object が None であれば中止
        if context.active_object is None:
            log(msg_not_armature)
            return op_result_cancelled

        # アーマチュアを取得
        arm = get_armature_object(context.active_object)

        # 選択中のオブジェクトの型チェック
        if arm is None or arm.type != type_armature:
            log(msg_not_armature)
            return op_result_cancelled

        # アーマチュアをアクティブにして、非表示状態を取得
        bpy.context.view_layer.objects.active = arm
        arm_isHide: bool = bpy.context.view_layer.objects.active.hide_get()

        # アーマチュアを表示
        bpy.context.view_layer.objects.active.hide_set(False)

        # アーマチュアのボーン名を取得
        vertex_groups = cast_to_armature(arm.data).bones.keys()

        # arm を親に持つメッシュオブジェクトを取得
        mesh_objects = [obj for obj in find_objects_by_parent(arm) if obj.type == type_mesh]

        # 全てのメッシュオブジェクトに対して処理を行う
        for obj in mesh_objects:

            log(f"Cleanup: {obj.name}")
            # obj をアクティブにする
            bpy.ops.object.select_all(action=action_deselect)
            bpy.context.view_layer.objects.active = obj

            # obj の非表示状態を取得し、表示状態に変更
            isHide: bool = bpy.context.view_layer.objects.active.hide_get()
            bpy.context.view_layer.objects.active.hide_set(False)

            # 頂点グループから、vertex_groups　に存在しないボーンを削除
            for vertex_group in obj.vertex_groups:
                if vertex_group.name not in vertex_groups:
                    obj.vertex_groups.remove(vertex_group)

            # obj の非表示状態を元に戻す
            bpy.context.view_layer.objects.active.hide_set(isHide)

        # アーマチュアの非表示状態を元に戻す
        bpy.ops.object.select_all(action=action_deselect)
        bpy.context.view_layer.objects.active = arm
        bpy.context.view_layer.objects.active.hide_set(arm_isHide)

        return op_result_finished

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        """メニューから呼び出された際の処理"""

        return self.execute(context)
