# THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

from PIL import ImageEnhance

from GimelStudio import api


class SharpnessNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Sharpness",
            "author": "Correct Syntax",
            "version": (1, 2, 0),
            "supported_app_version": (0, 5, 0),
            "category": "FILTER",
            "description": "Sharpens the image by the given amount.",
        }
        return meta_info

    def NodeInitProps(self):
        p = api.PositiveIntegerProp(
            idname="Amount",
            default=1,
            min_val=1,
            max_val=50,
            widget=api.SLIDER_WIDGET,
            label="Amount:",
        )
        self.NodeAddProp(p)

    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        sharpness_amount = eval_info.EvaluateProperty('Amount')

        image = api.RenderImage()
        enhancer = ImageEnhance.Sharpness(image1.GetImage())
        image.SetAsImage(enhancer.enhance(sharpness_amount).convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(SharpnessNode, "corenode_sharpness")
