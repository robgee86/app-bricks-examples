# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_bricks.web_ui import WebUI
from arduino.app_utils import App


FEED_URL = "http://192.168.1.5:7000/feed.xml"

ui = WebUI()

App.run()
