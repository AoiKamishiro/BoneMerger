import bpy

# region: 定数
dict_key_target_bones = "BoneMerger.TargetBone"
type_armature = 'ARMATURE'
mode_edit_armature = 'EDIT_ARMATURE'
mode_edit = 'EDIT'
mode_pose = 'POSE'
mode_object = 'OBJECT'
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
    d = modifier if isinstance(modifier, bpy.types.VertexWeightMixModifier) else None

    if d is None:
        raise TypeError(f"Invalid type: {modifier}")

    return d
# endregion


def get_armature_object(object: bpy.types.Object) -> bpy.types.Object | None:
    """
    自身がアーマチュアであれば自身を、そうでない場合は再帰的に親がアーマチュアになるまで探索する
    """
    obj = object
    while obj is not None and obj.type != type_armature:
        obj = obj.parent
    return obj
