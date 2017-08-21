# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ForcedScale
                                 A QGIS plugin
 Set scale only for Web Mecator
                             -------------------
        begin                : 2017-08-21
        copyright            : (C) 2017 by tsnav
        email                : hill@tsnav.cn
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ForcedScale class from file ForcedScale.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ForcedScale import ForcedScale
    return ForcedScale(iface)
