import bpy
from .common import *


class MergeBoneWeightToParentOperator(bpy.types.Operator):
    """
    ボーンのウェイトを親にマージするオペレーター
    """

    bl_idname: str = "bone_merger.merge_bone_weight_to_parent"
    bl_label: str = "ウェイトを親にマージ"

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

        armature = cast_to_armature(arm.data)

        # 保存されているボーンリストを取得
        target_bones = arm.get(dict_key_target_bones, [])

        # ボーンリストからウェイトをマージするボーンを取得し、配列に格納
        bones: list[bpy.types.Bone] = [bone for bone in armature.bones if bone.name in target_bones]

        # ボーンの階層をもとに、階層が深い順にソートする
        bones.sort(key=get_bone_depth, reverse=True)

        # arm を親に持つメッシュオブジェクトを取得
        mesh_objects = [obj for obj in find_objects_by_parent(arm) if obj.type == type_mesh]

        # 全てのメッシュオブジェクトに対して処理を行う
        for obj in mesh_objects:

            # obj をアクティブにする
            bpy.context.view_layer.objects.active = obj

            for bone in bones:

                # 頂点グループに bone が存在しない場合はスキップ
                if obj.vertex_groups.get(bone.name) is None:
                    continue

                # 頂点グループに bone.parent が存在しない場合は追加
                if obj.vertex_groups.get(bone.parent.name) is None:
                    obj.vertex_groups.new(name=bone.parent.name)

                # obj に 頂点ウェイト合成モディファイアー を追加
                modifier_name = f"BM_{bone.name}"
                modifier = obj.modifiers.new(name=modifier_name, type='VERTEX_WEIGHT_MIX')
                modifier = cast_to_vertex_weight_mix(modifier)

                # modifier が None であれば処理をスキップ
                if modifier is None:
                    continue

                log(f"Add modifier to {obj.name}, a:{bone.parent.name} -> b:{bone.name}")
                # modifier のプロパティを設定
                modifier.vertex_group_a = bone.parent.name
                modifier.vertex_group_b = bone.name
                modifier.mix_mode = 'ADD'
                modifier.mix_set = 'OR'
                modifier.default_weight_a = 0.0
                modifier.default_weight_b = 0.0

                # modifier をアクティブにする
                bpy.ops.object.modifier_set_active(modifier=modifier.name)

                # modifier の順番を一番上に移動
                bpy.ops.object.modifier_move_to_index(modifier=modifier.name, index=0)

                # modifier を適用
                bpy.ops.object.modifier_apply(modifier=modifier.name)

            # 頂点グループから bone を削除
            for bone in bones:
                if bone.name in obj.vertex_groups:
                    obj.vertex_groups.remove(obj.vertex_groups[bone.name])

        # ボーンを削除
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode=mode_edit)

        editBones: list[bpy.types.EditBone] = [bone for bone in armature.edit_bones if bone.name in target_bones]

        log(f"Remove bones: {editBones.__len__()}")
        for editBone in editBones:
            log(f"Remove bone: {editBone.name}")
            armature.edit_bones.remove(editBone)

        # オブジェクトモードに変更
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode=mode_object)

        return op_result_finished

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set:
        """メニューから呼び出された際の処理"""

        return self.execute(context)
