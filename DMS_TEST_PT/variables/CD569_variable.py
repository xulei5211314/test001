# -*- coding: utf-8 -*-
# @Time    : 2021/1/4
# @Author  : tingting.zhao
GLOBAL_LOCATOR = {
    "moudle": {
        "module_page_attr_OnlyCheckName": "(resource-id=com.iflytek.autofly.launcher:id/app_name, text=导航, class=android.widget.TextView)",
        "module_page_attr_(Click|Get)Name": [480, 70, 840, 344],
    },
    "应用中心": {
        "应用中心_首页_BUTTON_音乐": [600, 130, 720, 316],
    },
    "音乐": {
        "音乐_TAB页_BUTTON_QQ音乐": [600, 130, 720, 316],
        "音乐_QQ音乐_TEXT_随便听听": "(resource-id=com.iflytek.autofly.mediagroup:id/casual_music_name, text=随便听听)",
    },
    "工程模式": {
        "工程模式_主界面_BUTTON_BPU管理": [520, 660, 620, 710],
        "工程模式_BPU管理_BUTTON_获取APK版本信息": [120, 151, 620, 199],
        "工程模式_BPU管理_BUTTON_获取BPU版本信息": [120, 209, 620, 257],
        "工程模式_BPU管理_BUTTON_获取J2CHIPID": [120, 267, 620, 315],
        "工程模式_BPU管理_BUTTON_获取BPU运行状态": [120, 325, 620, 373],
        "工程模式_BPU管理_BUTTON_获取BPU运行时系统信息状态": [120, 383, 620, 431],
        "工程模式_BPU管理_BUTTON_获取BPU感知能力": [120, 441, 620, 489],
        "工程模式_BPU管理_TEXT_获取系统信息": "com.incall.apps.aiservice:id/bpu_system_info_title_tv,text=1.获取BPU系统信息",
        "工程模式_BPU管理_TEXT_APK版本信息": "com.incall.apps.aiservice:id/apk_version_result_tv",
        "工程模式_BPU管理_TEXT_BPU版本": "com.incall.apps.aiservice:id/version_result_tv",
        "工程模式_BPU管理_TEXT_J2chipID": "com.incall.apps.aiservice:id/chipID_result_tv",
        "工程模式_BPU管理_TEXT_BPU运行状态": "com.incall.apps.aiservice:id/run_state_result_tv",
        "工程模式_BPU管理_TEXT_BPU系统信息状态": "com.incall.apps.aiservice:id/sysinfo_result_tv",
        "工程模式_BPU管理_TEXT_BPU感知能力": "com.incall.apps.aiservice:id/capabilities_result_tv",
        },
}

GLOBAL_PAGE_ACTIVITY = {
    "工程界面": "com.incall.apps.aiservice/.ui.activity.FactoryTestActivity",
    "AIservice预览界面": "com.incall.apps.aiservice/.ui.activity.LauncherActivity",
}