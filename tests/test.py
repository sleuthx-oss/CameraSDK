#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
from LxCameraSDK import *


def main():
    camera = LxCamera("./../linux/SDK/lib/linux_x64/libLxCameraApi.so")

    api_version = camera.DcGetApiVersion()
    print(f"API Version: {api_version}")

    state = camera.DcSetInfoOutput(2, False, "log/", 0)
    state, dev_list, dev_num = camera.DcGetDeviceList()
    assert dev_num > 0, "No device found"

    state, handle, device_info = camera.DcOpenDevice(LX_OPEN_MODE.OPEN_BY_INDEX, "0")
    print(f"Device Info: {device_info}")

    state = camera.DcStartStream(handle)
    camera.DcSetBoolValue(handle, LX_CAMERA_FEATURE.LX_BOOL_ENABLE_2D_STREAM, True)

    while True:
        state = camera.DcSetCmd(handle, LX_CAMERA_FEATURE.LX_CMD_GET_NEW_FRAME)
        state, data_ptr = camera.getFrame(handle)
        state, rgb_image = camera.getRGBImage(data_ptr)
        if state == LX_STATE.LX_SUCCESS:
            # rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            cv2.imshow("RGB Image", rgb_image)

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    state, points = camera.getPointCloud(handle)
    camera.DcSaveXYZ(handle, "./xxx.pcd")

    state = camera.DcStopStream(handle)
    state = camera.DcCloseDevice(handle)


if __name__ == "__main__":
    main()
 