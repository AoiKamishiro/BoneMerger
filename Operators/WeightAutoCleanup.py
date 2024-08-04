import bpy
from ..common import *


class WeightAutoCleanupOperator(bpy.types.Operator):
    """
    ウェイトの自動クリーンアップを行うオペレーター
    """

    bl_idname: str = "bone_merger.weight_auto_cleanup"
    bl_label: str = "ウェイトの自動クリーンアップ"

    def execute(self, context: bpy.types.Context) -> set:
        """オペレーターの処理"""

        # オブジェクトモードに変更
        bpy.ops.object.mode_set(mode=mode_object)

        # context.active_object が None であれば中止
        if context.active_object is None:
            report_error(self, msg_not_armature)
            return op_result_cancelled

        # アーマチュアを取得
        arm = get_armature_object(context.active_object)

        # 選択中のオブジェクトの型チェック
        if arm is None or arm.type != type_armature:
            report_error(self, msg_not_armature)
            return op_result_cancelled

        # アーマチュアをアクティブにして、非表示状態を取得
        bpy.context.view_layer.objects.active = arm
        arm_isHide: bool = bpy.context.view_layer.objects.active.hide_get()

        # アーマチュアを表示
        bpy.context.view_layer.objects.active.hide_set(False)

        # arm を親に持つメッシュオブジェクトを取得
        mesh_objects = [obj for obj in find_objects_by_parent(arm) if obj.type == type_mesh]

        # 全てのメッシュオブジェクトに対して処理を行う
        for obj in mesh_objects:

            report(self, f"Cleanup: {obj.name}")
            # obj をアクティブにする
            bpy.context.view_layer.objects.active = obj

            isHide: bool = bpy.context.view_layer.objects.active.hide_get()
            bpy.context.view_layer.objects.active.hide_set(False)

            # ウェイトペインとモードに切り替え
            bpy.ops.object.mode_set(mode=mode_weight_paint)

            # Weight->LimitTotal
            bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)

            # Weight->NormalizeAll
            bpy.ops.object.vertex_group_normalize_all(group_select_mode='ALL')

            # Weight->Quantize
            bpy.ops.object.vertex_group_quantize(group_select_mode='ALL', steps=128)

            # Weight->Clean
            bpy.ops.object.vertex_group_clean(group_select_mode='ALL', limit=0.0001)

            # オブジェクトモードに変更
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode=mode_object)

            bpy.context.view_layer.objects.active.hide_set(isHide)

        # オブジェクトモードに変更
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode=mode_object)

        # アーマチュアの非表示状態を元に戻す
        bpy.context.view_layer.objects.active.hide_set(arm_isHide)

        return op_result_finished

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        """メニューから呼び出された際の処理"""

        return self.execute(context)
