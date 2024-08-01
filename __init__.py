import bpy
from .common import *
from .Panels.Main import MainPanel
from .Panels.Option import OptionPanel
from .Operators.MergeBoneWeightToParent import MergeBoneWeightToParentOperator
from .Operators.SaveBoneSelectionInArmature import SaveBoneSelectionInArmatureOperator
from .Operators.WeightAutoCleanup import WeightAutoCleanupOperator
from .Operators.SelectTargetBone import SelectTargetBoneOperator

# アドオンに関する情報
bl_info = {
    "name": "Bone Merger",
    "author": "神代アオイ (Aoi Kamishiro)",
    "version": (1, 2, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Tools ",
    "description": "Merge bone weight to parent bone.",
    "support": "COMMUNITY",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object"
}


# Blenderに登録するクラス
classes = [
    MainPanel,
    OptionPanel,
    SaveBoneSelectionInArmatureOperator,
    MergeBoneWeightToParentOperator,
    WeightAutoCleanupOperator,
    SelectTargetBoneOperator,
]


def register() -> None:
    """
    アドオン有効化時の処理
    """

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.bone_merger__show_target_bones = bpy.props.BoolProperty(name="対象ボーン", default=False)  # type: ignore

    log("addon enabled.")


def unregister() -> None:
    """
    アドオン無効化時の処理
    """

    for c in classes:
        bpy.utils.unregister_class(c)

    log("addon disabled.")


# 起動時処理
if __name__ == "__main__":
    register()
