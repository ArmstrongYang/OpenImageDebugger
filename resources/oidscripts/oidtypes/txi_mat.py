# -*- coding: utf-8 -*-

"""
This module is concerned with the analysis of each variable found by the
debugger, as well as identifying and describing the buffers that should be
plotted in the OpenImageDebugger window.
"""

import re

from oidscripts import symbols
from oidscripts.oidtypes import interface


class Mat(interface.TypeInspectorInterface):
    """
    Implementation for inspecting OpenCV Mat classes
    """
    def get_buffer_metadata(self, obj_name, picked_obj, debugger_bridge):
        buffer = debugger_bridge.get_casted_pointer('char', picked_obj['data'])

        width = int(picked_obj['cols'])
        height = int(picked_obj['rows'])
        flags = int(picked_obj['type'])

        channels = int(picked_obj['channel'])
        step = int(picked_obj['step'])
        row_stride = int(step/channels)

        if channels >= 3:
            pixel_layout = 'rgba'
        else:
            pixel_layout = 'bgra'

        type_value = symbols.OID_TYPES_UINT8

        return {
            'display_name':  obj_name + ' (' + str(picked_obj.type) + ')',
            'pointer': buffer,
            'width': width,
            'height': height,
            'channels': channels,
            'type': type_value,
            'row_stride': row_stride,
            'pixel_layout': pixel_layout,
            'transpose_buffer' : False
        }

    def is_symbol_observable(self, symbol, symbol_name):
        """
        Returns true if the given symbol is of observable type (the type of the
        buffer you are working with). Make sure to check for pointers of your
        type as well
        """
        # Check if symbol type is the expected buffer
        symbol_type = str(symbol.type)
        type_regex = r'(const\s+)?TongXueInno::Mat(\s+?[*&])?$'
        return re.match(type_regex, symbol_type) is not None
