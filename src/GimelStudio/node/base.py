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
##
## FILE: base.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the base toplevel-class for subclassing to create nodes
## ----------------------------------------------------------------------------

import wx

from .object import NodeObject


class NodeBase(NodeObject):
    """ Subclass this to create a node. 

    Only methods starting with 'Node' should be overridden 
    by the user, with few exceptions.
    """
    def __init__(self, _id):
        NodeObject.__init__(self, _id)
        self._MetaInit()
        self.NodeInitProps()
        self.NodeInitParams()
        self.Model.UpdateSockets()
        self.NodeSetThumb(self.Model.GetThumbImage())

    def _MetaInit(self):
        """ Internal method to initilize the 
        node data from the given node meta. 
        """
        meta = self.NodeMeta
        self.Model.SetCategory(meta['category'])
        self.Model.SetLabel(meta['label'])

    def GetType(self):
        """ Node type identifier

        :returns str: node type identifier.
        """
        return self.Model.GetType()

    def GetId(self):
        """ The node's unique internal id (wxPython).

        :returns str: unique id string.
        """
        return self.Model.GetId()

    def IsOutputNode(self):
        return self.Model.IsOutputNode()

    def SetRect(self, rect):
        self.Model.SetRect(rect)

    def IsSelected(self):
        return self.Model.IsSelected()

    def SetSelected(self, selected):
        self.Model.SetSelected(selected)

    def IsActive(self):
        return self.Model.IsActive()

    def SetActive(self, active):
        self.Model.SetActive(active)

    def IsMuted(self):
        return self.Model.IsMuted()

    def SetMuted(self, muted):
        self.Model.SetMuted(muted)

    def GetPosition(self):
        return self.Model.GetPosition()

    def SetPosition(self, pos):
        self.Model.SetPosition(pos)

    def GetSockets(self):
        return self.Model.GetSockets()

    def GetLabel(self):
        return self.Model.GetLabel()

    @property
    def Parameters(self):
        return self.Model.GetParameters()

    @property
    def Properties(self):
        return self.Model.GetProperties()

    @property
    def EvaluateNode(self):
        return self.NodeEvaluation

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "...",
            "author": "",
            "version": (0, 0, 1),
            "supported_app_version": (0, 0, 0),
            "category": "DEFAULT",
            "description": "..."
        }
        return meta_info

    def NodeInitProps(self):
        """ Define node properties for the node. These will translate 
        into widgets for editing the property in the Node Properties Panel if
        the Property is not hidden with `visible=False`. 

        Subclasses of the `Property` object such as `LabelProp`, etc. are to be
        added with the `NodeAddProp` method.

        Example:

            self.lbl_prop = api.LabelProp(
                idname="Example",
                default="", 
                label="Example label:",
                visible=True, # Default is True
                )

            self.NodeAddProp(self.lbl_prop)
        """
        pass

    def NodeInitParams(self):
        """ Define node parameters for the node. These will translate 
        into node sockets on the node itself.

        Subclasses of the Parameter` object such as `RenderImageParam` are to 
        be added with the `NodeAddParam` method.

        Example:

            p = api.RenderImageParam('Image')
            self.NodeAddParam(p)
        """
        pass
        
    def NodeAddProp(self, prop):
        """ Add a property to this node.
        
        :param prop: instance of PropertyField property class
        :returns: dictionary of the current properties
        """
        prop.SetWidgetEventHook(self.WidgetEventHook)
        return self.Model.AddProperty(prop)

    def NodeAddParam(self, param):
        """ Add a parameter to this node.
        
        :param prop: instance of Parameter parameter class
        :returns: dictionary of the current parameter
        """
        return self.Model.AddParameter(param)

    def NodeEditProp(self, idname, value):
        """ Edit a property of this node.
        
        :param name: name of the property
        :param value: new value of the property
        :returns: the current property value
        """
        return self.Model.EditProperty(idname, value)
        
    def NodePanelUI(self, parent, sizer):
        """ Create the Node property widgets for the 
        Node Property Panel.
        """
        for prop in self.Model._properties:
            self.Model._properties[prop].CreateUI(parent, sizer)

    def NodeEvaluation(self, eval_info):
        """ This is the method that is called during rendering 
        of the image. This should contain the actual code which does
        something to the image (e.g: blurs the image, etc.)
        and should return it as a RenderImage object.

        :param eval_info: object exposing methods to get evaluated ``Parameter`` and ``Property`` values to use for evaluating this node.
        :returns: this should return a RenderImage object
        """
        pass

    def WidgetEventHook(self, idname, value):
        """ Property widget callback event hook. This method is called
        after the property widget has returned the new value. It is useful
        for updating the node itself or other node properties as a result of
        a change in the value of the property.

        *Keep in mind that this is only called after a property is edited by the user. If you are looking for more flexibility, you should look into creating your own Property.*

        :prop idname: idname of the property which was updated and 
        is calling this method
        :prop value: updated value of the property
        """
        pass

    def Draw(self, dc):
        """ Draw this node on the Node Graph. This is 
        an internal method which shouldn't be used directly by users.
        """
        self.UpdateView()
        self.View.Draw(dc)

    def RefreshNodeGraph(self):
        """ Force a refresh of the Node Graph panel. """
        self.NodeGraphMethods.RefreshGraph()

    def RefreshPropertyPanel(self): 
        """ Force a refresh of the Node Properties panel. """
        self.NodeGraphMethods.NodePropertiesPanel.UpdatePanelContents(self)

    @property
    def NodeGraphMethods(self):
        """ Access internal Node Graph methods. 
        
        *Please only use this if you know what you're doing...*
        """
        return self.Model.GetParent()

    def HitTest(self, x, y):
        """ Node hittest handler. Please do not override. """
        return self.Model.HitTest(x, y)

    def NodeSetThumb(self, image, force_refresh=False):
        """ Update the thumbnail for this node.

        :param image: PIL Image to set as the thumbnail
        :param force_refresh: if True, updates will apply and 
        everything will be refreshed right away.
        """
        self.Model.UpdateThumbnail(image)
        if force_refresh == True:
            self.Draw(self.NodeGraphMethods.GetPDC())
            self.RefreshNodeGraph()
