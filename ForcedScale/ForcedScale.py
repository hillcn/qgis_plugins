# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ForcedScale
                                 A QGIS plugin
 Set scale only for Web Mecator
                              -------------------
        begin                : 2017-08-21
        git sha              : $Format:%H$
        copyright            : (C) 2017 by tsnav
        email                : hill@tsnav.cn
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .ForcedScale_dialog import ForcedScaleDialog
import os.path


class ForcedScale:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ForcedScale_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ForcedScaleDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ForcedScale')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'ForcedScale')
        self.toolbar.setObjectName(u'ForcedScale')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ForcedScale', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
    
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ForcedScale/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'zoom14'),
            callback=self.run14,
            add_to_toolbar=False,
            parent=self.iface.mainWindow())
        self.add_action(
            icon_path,
            text=self.tr(u'zoom15'),
            callback=self.run15,
            add_to_toolbar=False,
            parent=self.iface.mainWindow())
        self.add_action(
            icon_path,
            text=self.tr(u'forceScale'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&ForcedScale'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run14(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.iface.mapCanvas().zoomScale( 36112 )
        self.iface.mapCanvas().refresh()

    def run15(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.iface.mapCanvas().zoomScale( 18056 )
        self.iface.mapCanvas().refresh()

    def run(self):
        replayed = False
        # pre-defined scales
        scales = [
            1128,
            2257,
            4514,
            9028,
            18056,
            36112,
            72224,
            144448,
            288896,
            577790,
            1155581,
            2311162,
            4622324,
            9244648,
            18489296,
            36978592,
            73957184,
            147914368,
            295828736
        ]

        def setScale(scale):
            self.iface.mapCanvas().scaleChanged.disconnect(setScale)
            
            print("initial scale: %s" % scale)
            
            targetScale = min(
                scales, 
                key=lambda x:abs(x-scale)
            )
            if targetScale == scale:
                return
            
            print("zoom to %s" % targetScale)
            self.iface.mapCanvas().zoomScale( targetScale )
            self.iface.mapCanvas().scaleChanged.connect(setScale)
        
        # avoid loop
        self.iface.mapCanvas().scaleChanged.connect(setScale)
        
