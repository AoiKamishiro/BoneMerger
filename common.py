import bpy

# region: 定数
dict_key_target_bones = "BoneMerger.TargetBone"
type_armature = 'ARMATURE'
type_mesh = 'MESH'
mode_edit_armature = 'EDIT_ARMATURE'
mode_edit = 'EDIT'
mode_pose = 'POSE'
mode_object = 'OBJECT'
mode_weight_paint = 'WEIGHT_PAINT'
op_result_cancelled = {'CANCELLED'}
op_result_finished = {'FINISHED'}
icon_tria_down = 'TRIA_DOWN'
icon_tria_right = 'TRIA_RIGHT'
action_deselect = 'DESELECT'
prop_show_target_bones = "bone_merger__show_target_bones"
msg_not_armature = "アーマチュアが選択されていません。"
# endregion


# region: キャスト関数


def cast_to_armature(data: bpy.types.ID) -> bpy.types.Armature:
    """IDオブジェクトをアーマチュアにキャスト"""
    d = data if isinstance(data, bpy.types.Armature) else None

    if d is None:
        raise TypeError(f"Invalid type: {data}")

    return d


def cast_to_mesh(data: bpy.types.ID) -> bpy.types.Mesh:
    """IDオブジェクトをメッシュにキャスト"""
    d = data if isinstance(data, bpy.types.Mesh) else None

    if d is None:
        raise TypeError(f"Invalid type: {data}")

    return d


def cast_to_vertex_weight_mix(modifier: bpy.types.Modifier) -> bpy.types.VertexWeightMixModifier:
    """モディファイアを頂点ウェイト合成モディファイアにキャスト"""
    m = modifier if isinstance(modifier, bpy.types.VertexWeightMixModifier) else None

    if m is None:
        raise TypeError(f"Invalid type: {modifier}")

    return m
# endregion


def log(msg: str) -> None:
    """ログを出力"""

    print("[Bone Merger] "+msg)


def get_armature_object(object: bpy.types.Object) -> bpy.types.Object | None:
    """
    自身がアーマチュアであれば自身を、そうでない場合は再帰的に親がアーマチュアになるまで探索する
    """

    obj = object
    while obj is not None and obj.type != type_armature:
        obj = obj.parent
    return obj


def find_objects_by_parent(object: bpy.types.Object) -> list[bpy.types.Object]:
    """
    指定したオブジェクトの子オブジェクトを再帰的に取得する
    """

    objects = []
    for obj in object.children:
        objects.append(obj)
        objects.extend(find_objects_by_parent(obj))
    return objects


def get_bone_depth(bone: bpy.types.Bone) -> int:
    """
    ボーンの階層を再帰的に調査する
    """

    return get_bone_depth(bone.parent) + 1 if bone.parent else 0
