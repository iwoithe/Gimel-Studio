## THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## ----------------------------------------------------------------------------

import wx
import cv2
from PIL import Image
import numpy as np

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

from GimelStudio.utils.image import ArrayFromImage, ArrayToImage

  
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_tobumpmap"

    @property
    def NodeLabel(self):
        return "To Bump Map"

    @property
    def NodeCategory(self):
        return "CONVERT"

    @property
    def NodeDescription(self):
        return "Converts the image into a bump map texture for use in 3D." 

    @property
    def NodeVersion(self):
        return "1.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Saturation',
                prop_type='INTEGER',
                value=1
                ),
            Property('Brightness',
                prop_type='INTEGER',
                value=0
                ),
            Property('Gamma',
                prop_type='INTEGER',
                value=1
                ),
            ]

    @property
    def NodeParameters(self):
        return [
            Parameter('Image',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
        ]

   
    def NodePropertiesUI(self, node, parent, sizer):
        current_saturation_value = self.NodeGetPropValue('Saturation')
        current_brightness_value = self.NodeGetPropValue('Brightness')
        current_gamma_value = self.NodeGetPropValue('Gamma')

        # Saturation
        saturation_label = wx.StaticText(parent, label="Saturation:")
        sizer.Add(saturation_label, border=5)

        self.saturation_slider = wx.Slider(
            parent, wx.ID_ANY, 
            value=current_saturation_value,
            minValue=1, maxValue=50,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.saturation_slider.SetTickFreq(2)

        sizer.Add(self.saturation_slider, flag=wx.EXPAND|wx.ALL, border=5)

        # Brightness
        brightness_label = wx.StaticText(parent, label="Brightness:")
        sizer.Add(brightness_label, border=5)

        self.brightness_slider = wx.Slider(
            parent, wx.ID_ANY, 
            value=current_brightness_value,
            minValue=0, maxValue=50,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.brightness_slider.SetTickFreq(2)

        sizer.Add(self.brightness_slider, flag=wx.EXPAND|wx.ALL, border=5)

        # Gamma
        gamma_label = wx.StaticText(parent, label="Gamma:")
        sizer.Add(gamma_label, border=5)

        self.gamma_slider = wx.Slider(
            parent, wx.ID_ANY, 
            value=current_gamma_value,
            minValue=1, maxValue=50,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.gamma_slider.SetTickFreq(2)

        sizer.Add(self.gamma_slider, flag=wx.EXPAND|wx.ALL, border=5)

        # Bindings
        parent.Bind(
            wx.EVT_SCROLL_THUMBRELEASE, 
            self.OnSaturationChange, 
            self.saturation_slider
            )
        parent.Bind(
            wx.EVT_SCROLL_THUMBRELEASE, 
            self.OnBrightnessChange, 
            self.brightness_slider
            )
        parent.Bind(
            wx.EVT_SCROLL_THUMBRELEASE, 
            self.OnGammaChange, 
            self.gamma_slider
            )

    def OnSaturationChange(self, event):
        self.NodePropertiesUpdate('Saturation', self.saturation_slider.GetValue())

    def OnBrightnessChange(self, event):
        self.NodePropertiesUpdate('Brightness', self.brightness_slider.GetValue())

    def OnGammaChange(self, event):
        self.NodePropertiesUpdate('Gamma', self.gamma_slider.GetValue())

    def GammaCorrection(self, image, gamma):
        """ Corrects gamma of image. """
        inv_gamma = 1 / gamma
        table = np.array(
            [((i / 255) ** inv_gamma) * 255 for i in range(0, 256)]
            ).astype("uint8")
        return cv2.LUT(image, table)   

    def ComputeBumpMap(self, image, saturation, brightness, gamma):
        """ Calculates and returns a bump map. """
        gray_scale_img = cv2.bitwise_not(image)
        bump_map = cv2.convertScaleAbs(
            gray_scale_img, 
            alpha=saturation, 
            beta=brightness
            )
        gc_bump_map = self.GammaCorrection(bump_map, gamma)
        return gc_bump_map

    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        saturation_val = eval_info.EvaluateProperty('Saturation')
        brightness_val = eval_info.EvaluateProperty('Brightness')
        gamma_val = eval_info.EvaluateProperty('Gamma')

        # Convert the current image data to an array 
        # that we can use and greyscale it.
        im = ArrayFromImage(image1.GetImage())
        gray_scale_img = cv2.equalizeHist(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))

        generated_bump_map = self.ComputeBumpMap(
            gray_scale_img, 
            saturation_val, 
            brightness_val, 
            gamma_val
            )
        
        image = RenderImage()
        image.SetAsImage(
            ArrayToImage(generated_bump_map).convert('RGBA')
            )
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)