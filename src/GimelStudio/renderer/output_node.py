# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2021 by Noah Rahm and contributors
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
#
# FILE: output_node.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Defines the output node in an abstract way
#
# This file includes code that was modified from imagegen
# (https://github.com/nfactorial/imagegen) which is licensed
# under the Apache License Version 2.0
# Copyright 2016 nfactorial
# ----------------------------------------------------------------------------

from .eval_info import EvalInfo


class OutputNode(object):
    """ Represents the evaluation of the composite output node. """

    def __init__(self):
        self.node = None

    def SetNode(self, node):
        """ Set the node object connected to the output node
        this class represents.

        :param node: output node object
        """
        self.node = node.Parameters["Image"].binding

    def RenderImage(self):
        """ Render the image for this output node. If the output
        node is not connected then the default image will be rendered.
        """
        if self.node != None:
            eval_info = EvalInfo(self.node)
            image = eval_info.node.EvaluateNode(eval_info)
            return image
