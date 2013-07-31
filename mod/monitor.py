# -*- coding: utf-8 -*-

# Copyright 2012-2013 AGR Audio, Industria e Comercio LTDA. <contato@portalmod.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import socket

try:
    from tornado.tcpserver import TCPServer
except ImportError:
    # tornado 2.x
    from tornado.netutil import TCPServer


from mod.settings import (CLIPMETER_IN, CLIPMETER_OUT, CLIPMETER_L, CLIPMETER_R, 
                          PEAKMETER_IN, PEAKMETER_OUT, PEAKMETER_L, PEAKMETER_R, 
                          CLIPMETER_MON_L, CLIPMETER_MON_R, PEAKMETER_MON_L, PEAKMETER_MON_R,
                          TUNER)

from mod.session import SESSION

class MonitorServer(TCPServer):
    
    def _process_msg(self, msg):
        try:
            cmd, instance, port, value =  msg.replace("\x00", "").split()
            assert cmd == "monitor"
            instance = int(instance)
            value = float(value)
        except (ValueError, AssertionError), e:
            # TODO: tratar error
            pass
        else:
            if instance == CLIPMETER_IN:
                if port == CLIPMETER_MON_L:
                    SESSION.clipmeter(0, value)
                elif port == CLIPMETER_MON_R:
                    SESSION.clipmeter(1, value)
            elif instance == CLIPMETER_OUT:
                if port == CLIPMETER_MON_L:
                    SESSION.clipmeter(2, value)
                elif port == CLIPMETER_MON_R:
                    SESSION.clipmeter(3, value)
            elif instance == PEAKMETER_IN:
                if port == PEAKMETER_MON_L:
                    SESSION.peakmeter(0, value)
                elif port == PEAKMETER_MON_R:
                    SESSION.peakmeter(1, value)
            elif instance == PEAKMETER_OUT:
                if port == PEAKMETER_MON_L:
                    SESSION.peakmeter(2, value)
                elif port == PEAKMETER_MON_R:
                    SESSION.peakmeter(3, value)
            elif instance == TUNER:
                SESSION.tuner(value)
        self._handle_conn()

    def handle_stream(self, s, addr):
        self._stream = s
        self._handle_conn()
    
    def _handle_conn(self):
        self._stream.read_until("\x00", self._process_msg)
