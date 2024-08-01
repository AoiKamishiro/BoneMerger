import bpy
from ..common import *
from ..Bases.Panel import PanelBase
from ..Operators.WeightAutoCleanup import WeightAutoCleanupOperator
from ..Operators.RemoveNonExistentBoneWeights import RemoveNonExistentBoneWeightsOperator


class OptionPanel(PanelBase):
    """
    オプション処理を行うパネル
    """

    bl_idname: str = "BONE_MERGER_PT_OPTION_PANEL"
    bl_label: str = "Option"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout

        # ウェイトの正規化を行うボタンを作成
        layout.operator(WeightAutoCleanupOperator.bl_idname, text=WeightAutoCleanupOperator.bl_label)

        # 存在しないボーンのウェイトを削除するボタンを作成
        layout.operator(RemoveNonExistentBoneWeightsOperator.bl_idname, text=RemoveNonExistentBoneWeightsOperator.bl_label)
