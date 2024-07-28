import bpy
from .MainPanel import MainPanel
from .SaveBoneSelectionInArmatureOperator import SaveBoneSelectionInArmatureOperator
from .MergeBoneWeightToParentOperator import MergeBoneWeightToParentOperator

# アドオンに関する情報
bl_info = {
    "name": "Bone Merger",
    "author": "神代アオイ (Aoi Kamishiro)",
    "version": (1, 0),
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
    SaveBoneSelectionInArmatureOperator,
    MergeBoneWeightToParentOperator,
]


def register() -> None:
    """
    アドオン有効化時の処理
    """

    for c in classes:
        bpy.utils.register_class(c)

    print("BoneMerger has been enabled.")


def unregister() -> None:
    """
    アドオン無効化時の処理
    """

    for c in classes:
        bpy.utils.unregister_class(c)

    print("Addon BoneMerger has been disabled.")


# 起動時処理
if __name__ == "__main__":
    register()
