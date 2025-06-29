#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from pathlib import Path
import re
from sebaubuntu_libs.libstring import removeprefix

IGNORE_BINARIES = [
	"awk", # https://cs.android.com/android/platform/superproject/main/+/main:external/one-true-awk/Android.bp
	"logwrapper", # https://cs.android.com/android/platform/superproject/main/+/main:system/logging/logwrapper/Android.bp
	"newfs_msdos", # https://cs.android.com/android/platform/superproject/main/+/main:external/newfs_msdos/Android.bp
	"sh",
	"vndservice", # https://cs.android.com/android/platform/superproject/main/+/main:frameworks/native/cmds/service/Android.bp
	"vndservicemanager", # https://cs.android.com/android/platform/superproject/main/+/main:frameworks/native/cmds/servicemanager/Android.bp
] + [
	# toolbox
	"toolbox",
	"toolbox_vendor",
] + [
	# toolbox symlinks
	# https://cs.android.com/android/platform/superproject/main/+/main:system/core/toolbox/Android.bp
	"getevent",
	"getprop",
	"modprobe",
	"setprop",
	"start",
	"stop",
] + [
	# toybox
	"toybox",
	"toybox_vendor",
] + [
	# toybox symlinks
	# https://cs.android.com/android/platform/superproject/main/+/main:external/toybox/Android.bp
	"[",
	"acpi",
	"base64",
	"basename",
	"blockdev",
	"brctl",
	"cal",
	"cat",
	"chattr",
	"chcon",
	"chgrp",
	"chmod",
	"chown",
	"chroot",
	"chrt",
	"cksum",
	"clear",
	"cmp",
	"comm",
	"cp",
	"cpio",
	"cut",
	"date",
	"dd",
	"devmem",
	"df",
	"diff",
	"dirname",
	"dmesg",
	"dos2unix",
	"du",
	"echo",
	"egrep",
	"env",
	"expand",
	"expr",
	"fallocate",
	"false",
	"fgrep",
	"file",
	"find",
	"flock",
	"fmt",
	"free",
	"fsync",
	"getconf",
	"getenforce",
	"gpiodetect",
	"gpiofind",
	"gpioget",
	"gpioinfo",
	"gpioset",
	"grep",
	"groups",
	"gunzip",
	"gzip",
	"head",
	"hostname",
	"hwclock",
	"i2cdetect",
	"i2cdump",
	"i2cget",
	"i2cset",
	"i2ctransfer",
	"iconv",
	"id",
	"ifconfig",
	"inotifyd",
	"insmod",
	"install",
	"ionice",
	"iorenice",
	"kill",
	"killall",
	"ln",
	"load_policy",
	"log",
	"logger",
	"logname",
	"losetup",
	"ls",
	"lsattr",
	"lsmod",
	"lsof",
	"lspci",
	"lsusb",
	"md5sum",
	"memeater",
	"microcom",
	"mkdir",
	"mkfifo",
	"mknod",
	"mkswap",
	"mktemp",
	"modinfo",
	"more",
	"mount",
	"mountpoint",
	"mv",
	"nc",
	"netcat",
	"netstat",
	"nice",
	"nl",
	"nohup",
	"nproc",
	"nsenter",
	"od",
	"paste",
	"patch",
	"pgrep",
	"pidof",
	"pkill",
	"pmap",
	"printenv",
	"printf",
	"ps",
	"pwd",
	"readelf",
	"readlink",
	"realpath",
	"renice",
	"restorecon",
	"rm",
	"rmdir",
	"rmmod",
	"rtcwake",
	"runcon",
	"sed",
	"sendevent",
	"seq",
	"setenforce",
	"setsid",
	"sha1sum",
	"sha224sum",
	"sha256sum",
	"sha384sum",
	"sha512sum",
	"sleep",
	"sort",
	"split",
	"stat",
	"strings",
	"stty",
	"swapoff",
	"swapon",
	"sync",
	"sysctl",
	"tac",
	"tail",
	"tar",
	"taskset",
	"tee",
	"test",
	"time",
	"timeout",
	"top",
	"touch",
	"tr",
	"true",
	"truncate",
	"tty",
	"uclampset",
	"ulimit",
	"umount",
	"uname",
	"uniq",
	"unix2dos",
	"unlink",
	"unshare",
	"uptime",
	"usleep",
	"uudecode",
	"uuencode",
	"uuidgen",
	"vi",
	"vmstat",
	"watch",
	"wc",
	"which",
	"whoami",
	"xargs",
	"xxd",
	"yes",
	"zcat",
]

"""
Use get_vndk_libs.py to update this list
"""
IGNORE_SHARED_LIBS = [
	"android.frameworks.automotive.display@1.0.so",
	"android.frameworks.cameraservice.common-V1-ndk.so",
	"android.frameworks.cameraservice.common@2.0.so",
	"android.frameworks.cameraservice.device-V1-ndk.so",
	"android.frameworks.cameraservice.device@2.0.so",
	"android.frameworks.cameraservice.service-V1-ndk.so",
	"android.frameworks.cameraservice.service@2.0.so",
	"android.frameworks.cameraservice.service@2.1.so",
	"android.frameworks.displayservice@1.0.so",
	"android.frameworks.schedulerservice@1.0.so",
	"android.frameworks.sensorservice@1.0.so",
	"android.frameworks.stats@1.0.so",
	"android.frameworks.vr.composer@1.0.so",
	"android.hardware.atrace@1.0.so",
	"android.hardware.audio.common-V1-ndk.so",
	"android.hardware.audio.common@2.0.so",
	"android.hardware.audio.common@4.0.so",
	"android.hardware.audio.common@5.0.so",
	"android.hardware.audio.common@6.0.so",
	"android.hardware.audio.effect@2.0.so",
	"android.hardware.audio.effect@4.0.so",
	"android.hardware.audio.effect@5.0.so",
	"android.hardware.audio.effect@6.0.so",
	"android.hardware.audio@2.0.so",
	"android.hardware.audio@4.0.so",
	"android.hardware.audio@5.0.so",
	"android.hardware.audio@6.0.so",
	"android.hardware.authsecret-V1-ndk.so",
	"android.hardware.authsecret-V1-ndk_platform.so",
	"android.hardware.authsecret@1.0.so",
	"android.hardware.automotive.audiocontrol@1.0.so",
	"android.hardware.automotive.audiocontrol@2.0.so",
	"android.hardware.automotive.can@1.0.so",
	"android.hardware.automotive.evs@1.0.so",
	"android.hardware.automotive.evs@1.1.so",
	"android.hardware.automotive.occupant_awareness-V1-ndk.so",
	"android.hardware.automotive.occupant_awareness-V1-ndk_platform.so",
	"android.hardware.automotive.sv@1.0.so",
	"android.hardware.automotive.vehicle@2.0.so",
	"android.hardware.biometrics.face@1.0.so",
	"android.hardware.biometrics.fingerprint@2.1.so",
	"android.hardware.biometrics.fingerprint@2.2.so",
	"android.hardware.bluetooth.a2dp@1.0.so",
	"android.hardware.bluetooth.audio-V2-ndk.so",
	"android.hardware.bluetooth.audio@2.0.so",
	"android.hardware.bluetooth@1.0.so",
	"android.hardware.bluetooth@1.1.so",
	"android.hardware.boot@1.0.so",
	"android.hardware.boot@1.1.so",
	"android.hardware.broadcastradio@1.0.so",
	"android.hardware.broadcastradio@1.1.so",
	"android.hardware.broadcastradio@2.0.so",
	"android.hardware.camera.common-V1-ndk.so",
	"android.hardware.camera.common@1.0.so",
	"android.hardware.camera.device-V1-ndk.so",
	"android.hardware.camera.device@1.0.so",
	"android.hardware.camera.device@3.2.so",
	"android.hardware.camera.device@3.3.so",
	"android.hardware.camera.device@3.4.so",
	"android.hardware.camera.device@3.5.so",
	"android.hardware.camera.device@3.6.so",
	"android.hardware.camera.metadata-V1-ndk.so",
	"android.hardware.camera.metadata@3.2.so",
	"android.hardware.camera.metadata@3.3.so",
	"android.hardware.camera.metadata@3.4.so",
	"android.hardware.camera.metadata@3.5.so",
	"android.hardware.camera.provider-V1-ndk.so",
	"android.hardware.camera.provider@2.4.so",
	"android.hardware.camera.provider@2.5.so",
	"android.hardware.camera.provider@2.6.so",
	"android.hardware.cas.native@1.0.so",
	"android.hardware.cas@1.0.so",
	"android.hardware.cas@1.1.so",
	"android.hardware.cas@1.2.so",
	"android.hardware.common-V1-ndk_platform.so",
	"android.hardware.common-V2-ndk.so",
	"android.hardware.common-V2-ndk_platform.so",
	"android.hardware.common.fmq-V1-ndk.so",
	"android.hardware.common.fmq-V1-ndk_platform.so",
	"android.hardware.configstore-utils.so",
	"android.hardware.configstore@1.0.so",
	"android.hardware.configstore@1.1.so",
	"android.hardware.confirmationui-support-lib.so",
	"android.hardware.confirmationui@1.0.so",
	"android.hardware.contexthub@1.0.so",
	"android.hardware.contexthub@1.1.so",
	"android.hardware.drm-V1-ndk.so",
	"android.hardware.drm@1.0.so",
	"android.hardware.drm@1.1.so",
	"android.hardware.drm@1.2.so",
	"android.hardware.drm@1.3.so",
	"android.hardware.dumpstate-V1-ndk.so",
	"android.hardware.dumpstate@1.0.so",
	"android.hardware.dumpstate@1.1.so",
	"android.hardware.fastboot@1.0.so",
	"android.hardware.gatekeeper@1.0.so",
	"android.hardware.gnss-V1-ndk_platform.so",
	"android.hardware.gnss-V2-ndk.so",
	"android.hardware.gnss.measurement_corrections@1.0.so",
	"android.hardware.gnss.measurement_corrections@1.1.so",
	"android.hardware.gnss.visibility_control@1.0.so",
	"android.hardware.gnss@1.0.so",
	"android.hardware.gnss@1.1.so",
	"android.hardware.gnss@2.0.so",
	"android.hardware.gnss@2.1.so",
	"android.hardware.graphics.allocator-V1-ndk.so",
	"android.hardware.graphics.allocator-V2-ndk.so",
	"android.hardware.graphics.allocator@2.0.so",
	"android.hardware.graphics.allocator@3.0.so",
	"android.hardware.graphics.allocator@4.0.so",
	"android.hardware.graphics.bufferqueue@1.0.so",
	"android.hardware.graphics.bufferqueue@2.0.so",
	"android.hardware.graphics.common-V1-ndk_platform.so",
	"android.hardware.graphics.common-V2-ndk_platform.so",
	"android.hardware.graphics.common-V3-ndk.so",
	"android.hardware.graphics.common-V4-ndk.so",
	"android.hardware.graphics.common@1.0.so",
	"android.hardware.graphics.common@1.1.so",
	"android.hardware.graphics.common@1.2.so",
	"android.hardware.graphics.composer3-V1-ndk.so",
	"android.hardware.graphics.composer@2.1.so",
	"android.hardware.graphics.composer@2.2.so",
	"android.hardware.graphics.composer@2.3.so",
	"android.hardware.graphics.composer@2.4.so",
	"android.hardware.graphics.mapper@2.0.so",
	"android.hardware.graphics.mapper@2.1.so",
	"android.hardware.graphics.mapper@3.0.so",
	"android.hardware.graphics.mapper@4.0.so",
	"android.hardware.health-V1-ndk.so",
	"android.hardware.health.storage-V1-ndk.so",
	"android.hardware.health.storage-V1-ndk_platform.so",
	"android.hardware.health.storage@1.0.so",
	"android.hardware.health@1.0.so",
	"android.hardware.health@2.0.so",
	"android.hardware.health@2.1.so",
	"android.hardware.identity-V2-ndk_platform.so",
	"android.hardware.identity-V3-ndk_platform.so",
	"android.hardware.identity-V4-ndk.so",
	"android.hardware.input.classifier@1.0.so",
	"android.hardware.input.common@1.0.so",
	"android.hardware.ir-V1-ndk.so",
	"android.hardware.ir@1.0.so",
	"android.hardware.keymaster-V2-ndk_platform.so",
	"android.hardware.keymaster-V3-ndk.so",
	"android.hardware.keymaster-V3-ndk_platform.so",
	"android.hardware.keymaster@3.0.so",
	"android.hardware.keymaster@4.0.so",
	"android.hardware.keymaster@4.1.so",
	"android.hardware.light-V1-ndk_platform.so",
	"android.hardware.light-V2-ndk.so",
	"android.hardware.light@2.0.so",
	"android.hardware.media.bufferpool@1.0.so",
	"android.hardware.media.bufferpool@2.0.so",
	"android.hardware.media.c2@1.0.so",
	"android.hardware.media.c2@1.1.so",
	"android.hardware.media.omx@1.0.so",
	"android.hardware.media@1.0.so",
	"android.hardware.memtrack-V1-ndk.so",
	"android.hardware.memtrack-V1-ndk_platform.so",
	"android.hardware.memtrack@1.0.so",
	"android.hardware.neuralnetworks@1.0.so",
	"android.hardware.neuralnetworks@1.1.so",
	"android.hardware.neuralnetworks@1.2.so",
	"android.hardware.neuralnetworks@1.3.so",
	"android.hardware.nfc-V1-ndk.so",
	"android.hardware.nfc@1.0.so",
	"android.hardware.nfc@1.1.so",
	"android.hardware.nfc@1.2.so",
	"android.hardware.oemlock-V1-ndk.so",
	"android.hardware.oemlock-V1-ndk_platform.so",
	"android.hardware.oemlock@1.0.so",
	"android.hardware.power-V1-ndk_platform.so",
	"android.hardware.power-V2-ndk_platform.so",
	"android.hardware.power-V3-ndk.so",
	"android.hardware.power.stats-V1-ndk.so",
	"android.hardware.power.stats-V1-ndk_platform.so",
	"android.hardware.power.stats@1.0.so",
	"android.hardware.power@1.0.so",
	"android.hardware.power@1.1.so",
	"android.hardware.power@1.2.so",
	"android.hardware.power@1.3.so",
	"android.hardware.radio-V1-ndk.so",
	"android.hardware.radio.config-V1-ndk.so",
	"android.hardware.radio.config@1.0.so",
	"android.hardware.radio.config@1.1.so",
	"android.hardware.radio.config@1.2.so",
	"android.hardware.radio.data-V1-ndk.so",
	"android.hardware.radio.deprecated@1.0.so",
	"android.hardware.radio.messaging-V1-ndk.so",
	"android.hardware.radio.modem-V1-ndk.so",
	"android.hardware.radio.network-V1-ndk.so",
	"android.hardware.radio.sim-V1-ndk.so",
	"android.hardware.radio.voice-V1-ndk.so",
	"android.hardware.radio@1.0.so",
	"android.hardware.radio@1.1.so",
	"android.hardware.radio@1.2.so",
	"android.hardware.radio@1.3.so",
	"android.hardware.radio@1.4.so",
	"android.hardware.radio@1.5.so",
	"android.hardware.rebootescrow-V1-ndk.so",
	"android.hardware.rebootescrow-V1-ndk_platform.so",
	"android.hardware.renderscript@1.0.so",
	"android.hardware.secure_element@1.0.so",
	"android.hardware.secure_element@1.1.so",
	"android.hardware.secure_element@1.2.so",
	"android.hardware.security.dice-V1-ndk.so",
	"android.hardware.security.keymint-V1-ndk_platform.so",
	"android.hardware.security.keymint-V2-ndk.so",
	"android.hardware.security.secureclock-V1-ndk.so",
	"android.hardware.security.secureclock-V1-ndk_platform.so",
	"android.hardware.security.sharedsecret-V1-ndk.so",
	"android.hardware.security.sharedsecret-V1-ndk_platform.so",
	"android.hardware.sensors-V1-ndk.so",
	"android.hardware.sensors@1.0.so",
	"android.hardware.sensors@2.0.so",
	"android.hardware.sensors@2.1.so",
	"android.hardware.soundtrigger3-V1-ndk.so",
	"android.hardware.soundtrigger@2.0-core.so",
	"android.hardware.soundtrigger@2.0.so",
	"android.hardware.soundtrigger@2.1.so",
	"android.hardware.soundtrigger@2.2.so",
	"android.hardware.soundtrigger@2.3.so",
	"android.hardware.tetheroffload.config@1.0.so",
	"android.hardware.tetheroffload.control@1.0.so",
	"android.hardware.thermal@1.0.so",
	"android.hardware.thermal@1.1.so",
	"android.hardware.thermal@2.0.so",
	"android.hardware.tv.cec@1.0.so",
	"android.hardware.tv.cec@2.0.so",
	"android.hardware.tv.input@1.0.so",
	"android.hardware.tv.tuner@1.0.so",
	"android.hardware.usb-V1-ndk.so",
	"android.hardware.usb.gadget@1.0.so",
	"android.hardware.usb.gadget@1.1.so",
	"android.hardware.usb@1.0.so",
	"android.hardware.usb@1.1.so",
	"android.hardware.usb@1.2.so",
	"android.hardware.uwb-V1-ndk.so",
	"android.hardware.vibrator-V1-ndk_platform.so",
	"android.hardware.vibrator-V2-ndk.so",
	"android.hardware.vibrator-V2-ndk_platform.so",
	"android.hardware.vibrator@1.0.so",
	"android.hardware.vibrator@1.1.so",
	"android.hardware.vibrator@1.2.so",
	"android.hardware.vibrator@1.3.so",
	"android.hardware.vr@1.0.so",
	"android.hardware.weaver-V1-ndk.so",
	"android.hardware.weaver-V1-ndk_platform.so",
	"android.hardware.weaver@1.0.so",
	"android.hardware.wifi.hostapd-V1-ndk.so",
	"android.hardware.wifi.hostapd@1.0.so",
	"android.hardware.wifi.hostapd@1.1.so",
	"android.hardware.wifi.hostapd@1.2.so",
	"android.hardware.wifi.offload@1.0.so",
	"android.hardware.wifi.supplicant-V1-ndk.so",
	"android.hardware.wifi.supplicant@1.0.so",
	"android.hardware.wifi.supplicant@1.1.so",
	"android.hardware.wifi.supplicant@1.2.so",
	"android.hardware.wifi.supplicant@1.3.so",
	"android.hardware.wifi@1.0.so",
	"android.hardware.wifi@1.1.so",
	"android.hardware.wifi@1.2.so",
	"android.hardware.wifi@1.3.so",
	"android.hardware.wifi@1.4.so",
	"android.hidl.allocator@1.0.so",
	"android.hidl.memory.block@1.0.so",
	"android.hidl.memory.token@1.0.so",
	"android.hidl.memory@1.0-impl.so",
	"android.hidl.memory@1.0.so",
	"android.hidl.safe_union@1.0.so",
	"android.hidl.token@1.0-utils.so",
	"android.hidl.token@1.0.so",
	"android.media.audio.common.types-V1-ndk.so",
	"android.media.soundtrigger.types-V1-ndk.so",
	"android.system.keystore2-V1-ndk_platform.so",
	"android.system.keystore2-V2-ndk.so",
	"android.system.net.netd@1.0.so",
	"android.system.net.netd@1.1.so",
	"android.system.suspend-V1-ndk.so",
	"android.system.suspend@1.0.so",
	"android.system.wifi.keystore@1.0.so",
	"audio.a2dp.default.so",
	"hidl.tests.vendor@1.0.so",
	"hidl.tests.vendor@1.1.so",
	"ld-android.so",
	"libEGL.so",
	"libETC1.so",
	"libFFTEm.so",
	"libGLESv1_CM.so",
	"libGLESv2.so",
	"libGLESv3.so",
	"libLLVM_android.so",
	"libOpenMAXAL.so",
	"libOpenSLES.so",
	"libRS.so",
	"libRSCacheDir.so",
	"libRSCpuRef.so",
	"libRSDriver.so",
	"libRS_internal.so",
	"libRScpp.so",
	"libaacextractor.so",
	"libaaudio.so",
	"libaaudioservice.so",
	"libadbconnection.so",
	"libadbconnectiond.so",
	"libadf.so",
	"libamrextractor.so",
	"libandroid.so",
	"libandroid_net.so",
	"libandroid_runtime.so",
	"libandroid_servers.so",
	"libandroidfw.so",
	"libappfuse.so",
	"libart-compiler.so",
	"libart-dexlayout.so",
	"libart-disassembler.so",
	"libart.so",
	"libartd-compiler.so",
	"libartd-dexlayout.so",
	"libartd.so",
	"libasyncio.so",
	"libaudioclient.so",
	"libaudioeffect_jni.so",
	"libaudioflinger.so",
	"libaudiohal.so",
	"libaudiohal@2.0.so",
	"libaudiohal_deathhandler.so",
	"libaudiomanager.so",
	"libaudiopolicyenginedefault.so",
	"libaudiopolicymanager.so",
	"libaudiopolicymanagerdefault.so",
	"libaudiopolicyservice.so",
	"libaudiopreprocessing.so",
	"libaudioprocessing.so",
	"libaudioroute.so",
	"libaudiospdif.so",
	"libaudioutils.so",
	"libavservices_minijail.so",
	"libavservices_minijail_vendor.so",
	"libbacktrace.so",
	"libbase.so",
	"libbcc.so",
	"libbcinfo.so",
	"libbinder.so",
	"libbinder_ndk.so",
	"libbinderthreadstate.so",
	"libbinderwrapper.so",
	"libblas.so",
	"libbluetooth-binder.so",
	"libbluetooth.so",
	"libbluetooth_jni.so",
	"libbootanimation.so",
	"libbrillo-binder.so",
	"libbrillo-stream.so",
	"libbrillo.so",
	"libbrotli.so",
	"libbufferhub.so",
	"libbufferhubqueue.so",
	"libbufferqueueconverter.so",
	"libbundlewrapper.so",
	"libbz.so",
	"libc++.so",
	"libc++_shared.so",
	"libc.so",
	"libc_malloc_debug.so",
	"libcamera2ndk.so",
	"libcamera_client.so",
	"libcamera_metadata.so",
	"libcameraservice.so",
	"libcap.so",
	"libcgrouprc.so",
	"libchrome.so",
	"libclang_rt.asan-aarch64-android.so",
	"libclang_rt.asan-arm-android.so",
	"libclang_rt.asan-i686-android.so",
	"libclang_rt.asan-mips-android.so",
	"libclang_rt.asan-mips64-android.so",
	"libclang_rt.asan-x86_64-android.so",
	"libclang_rt.hwasan-aarch64-android.so",
	"libclang_rt.scudo-aarch64-android.so",
	"libclang_rt.scudo-arm-android.so",
	"libclang_rt.scudo-i686-android.so",
	"libclang_rt.scudo-x86_64-android.so",
	"libclang_rt.scudo_minimal-aarch64-android.so",
	"libclang_rt.scudo_minimal-arm-android.so",
	"libclang_rt.scudo_minimal-i686-android.so",
	"libclang_rt.scudo_minimal-x86_64-android.so",
	"libclang_rt.ubsan_minimal-aarch64-android.so",
	"libclang_rt.ubsan_minimal-arm-android.so",
	"libclang_rt.ubsan_minimal-i686-android.so",
	"libclang_rt.ubsan_minimal-x86_64-android.so",
	"libclang_rt.ubsan_standalone-aarch64-android.so",
	"libclang_rt.ubsan_standalone-arm-android.so",
	"libclang_rt.ubsan_standalone-i686-android.so",
	"libclang_rt.ubsan_standalone-x86_64-android.so",
	"libcld80211.so",
	"libcn-cbor.so",
	"libcodec2.so",
	"libcodec2_hidl@1.0.so",
	"libcodec2_vndk.so",
	"libcom.android.tethering.connectivity_native.so",
	"libcompiler_rt.so",
	"libcrypto.so",
	"libcrypto_utils.so",
	"libcups.so",
	"libcurl.so",
	"libcutils.so",
	"libdebuggerd_client.so",
	"libdefcontainer_jni.so",
	"libdexfile.so",
	"libdiskconfig.so",
	"libdisplayservicehidl.so",
	"libdl.so",
	"libdl_android.so",
	"libdmabufheap.so",
	"libdng_sdk.so",
	"libdownmix.so",
	"libdrm.so",
	"libdrmframework.so",
	"libdrmframework_jni.so",
	"libdt_fd_forward.so",
	"libdt_socket.so",
	"libdumpstateaidl.so",
	"libdumpstateutil.so",
	"libeffectproxy.so",
	"libeffects.so",
	"libeffectsconfig.so",
	"libevent.so",
	"libexif.so",
	"libexpat.so",
	"libext2_blkid.so",
	"libext2_com_err.so",
	"libext2_e2p.so",
	"libext2_misc.so",
	"libext2_quota.so",
	"libext2_uuid.so",
	"libext2fs.so",
	"libext4_utils.so",
	"libf2fs_sparseblock.so",
	"libfilterfw.so",
	"libfilterpack_imageproc.so",
	"libflacextractor.so",
	"libfmq.so",
	"libframesequence.so",
	"libft2.so",
	"libfwdlockengine.so",
	"libgatekeeper.so",
	"libgiftranscode.so",
	"libgralloctypes.so",
	"libgraphicsenv.so",
	"libgtest_prod.so",
	"libgui.so",
	"libgui_vendor.so",
	"libhardware.so",
	"libhardware_legacy.so",
	"libharfbuzz_ng.so",
	"libheif.so",
	"libhidcommand_jni.so",
	"libhidl-gen-hash.so",
	"libhidl-gen-utils.so",
	"libhidlallocatorutils.so",
	"libhidlbase.so",
	"libhidlcache.so",
	"libhidlmemory.so",
	"libhidltransport.so",
	"libhwbinder.so",
	"libhwbinder_noltopgo.so",
	"libhwc2on1adapter.so",
	"libhwui.so",
	"libicui18n.so",
	"libicuuc.so",
	"libimg_utils.so",
	"libincident.so",
	"libinput.so",
	"libinputflinger.so",
	"libinputservice.so",
	"libion.so",
	"libiprouteutil.so",
	"libjavacore.so",
	"libjavacrypto.so",
	"libjdwp.so",
	"libjni_pacprocessor.so",
	"libjnigraphics.so",
	"libjpeg.so",
	"libjsoncpp.so",
	"libkeymaster4support.so",
	"libkeymaster_messages.so",
	"libkeymaster_portable.so",
	"libkeystore-engine.so",
	"libkeystore_aidl.so",
	"libkeystore_binder.so",
	"libkeystore_parcelables.so",
	"libkeyutils.so",
	"liblayers_proto.so",
	"libldacBT_abr.so",
	"libldacBT_enc.so",
	"libldnhncr.so",
	"liblog.so",
	"liblogwrap.so",
	"liblshal.so",
	"liblz4.so",
	"liblzma.so",
	"libm.so",
	"libmdnssd.so",
	"libmedia.so",
	"libmedia_helper.so",
	"libmedia_jni.so",
	"libmedia_omx.so",
	"libmediadrm.so",
	"libmediaextractorservice.so",
	"libmedialogservice.so",
	"libmediametrics.so",
	"libmediandk.so",
	"libmediaplayerservice.so",
	"libmediautils.so",
	"libmemtrack.so",
	"libmemunreachable.so",
	"libmetricslogger.so",
	"libmidiextractor.so",
	"libminijail.so",
	"libminikin.so",
	"libmkbootimg_abi_check.so",
	"libmkvextractor.so",
	"libmp3extractor.so",
	"libmp4extractor.so",
	"libmpeg2extractor.so",
	"libmtp.so",
	"libnativehelper.so",
	"libnativewindow.so",
	"libnbaio.so",
	"libnbaio_mono.so",
	"libnblog.so",
	"libnetd_client.so",
	"libnetdutils.so",
	"libnetlink.so",
	"libnetutils.so",
	"libneuralnetworks.so",
	"libnfc-nci.so",
	"libnfc_nci_jni.so",
	"libnl.so",
	"libnpt.so",
	"liboggextractor.so",
	"libopenjdk.so",
	"libopenjdkd.so",
	"libopenjdkjvm.so",
	"libopenjdkjvmd.so",
	"libopenjdkjvmti.so",
	"libopenjdkjvmtid.so",
	"libopus.so",
	"libpackagelistparser.so",
	"libpagemap.so",
	"libpcap.so",
	"libpcre2.so",
	"libpcrecpp.so",
	"libpdfium.so",
	"libpdx_default_transport.so",
	"libpiex.so",
	"libpixelflinger.so",
	"libpng.so",
	"libpower.so",
	"libpowermanager.so",
	"libprintspooler_jni.so",
	"libprocessgroup.so",
	"libprocinfo.so",
	"libprotobuf-cpp-full.so",
	"libprotobuf-cpp-lite.so",
	"libprotoutil.so",
	"libpuresoftkeymasterdevice.so",
	"libqtaguid.so",
	"libradio_metadata.so",
	"libreference-ril.so",
	"libresourcemanagerservice.so",
	"libreverbwrapper.so",
	"libril.so",
	"librilutils.so",
	"librs_jni.so",
	"librtp_jni.so",
	"libschedulerservicehidl.so",
	"libselinux.so",
	"libsensor.so",
	"libsensorservice.so",
	"libsensorservicehidl.so",
	"libsepol.so",
	"libservices.so",
	"libsigchain.so",
	"libsoftkeymasterdevice.so",
	"libsonic.so",
	"libsonivox.so",
	"libsoundpool.so",
	"libsoundtrigger.so",
	"libsoundtriggerservice.so",
	"libsparse.so",
	"libspeexresampler.so",
	"libsqlite.so",
	"libssl.so",
	"libstagefright.so",
	"libstagefright_amrnb_common.so",
	"libstagefright_bufferpool@2.0.so",
	"libstagefright_bufferqueue_helper.so",
	"libstagefright_enc_common.so",
	"libstagefright_flacdec.so",
	"libstagefright_foundation.so",
	"libstagefright_http_support.so",
	"libstagefright_httplive.so",
	"libstagefright_omx.so",
	"libstagefright_omx_utils.so",
	"libstagefright_soft_aacdec.so",
	"libstagefright_soft_aacenc.so",
	"libstagefright_soft_amrdec.so",
	"libstagefright_soft_amrnbenc.so",
	"libstagefright_soft_amrwbenc.so",
	"libstagefright_soft_avcdec.so",
	"libstagefright_soft_avcenc.so",
	"libstagefright_soft_flacdec.so",
	"libstagefright_soft_flacenc.so",
	"libstagefright_soft_g711dec.so",
	"libstagefright_soft_gsmdec.so",
	"libstagefright_soft_hevcdec.so",
	"libstagefright_soft_mp3dec.so",
	"libstagefright_soft_mpeg2dec.so",
	"libstagefright_soft_mpeg4dec.so",
	"libstagefright_soft_mpeg4enc.so",
	"libstagefright_soft_opusdec.so",
	"libstagefright_soft_rawdec.so",
	"libstagefright_soft_vorbisdec.so",
	"libstagefright_soft_vpxdec.so",
	"libstagefright_soft_vpxenc.so",
	"libstagefright_softomx.so",
	"libstagefright_xmlparser.so",
	"libstatslog.so",
	"libstdc++.so",
	"libsurfaceflinger.so",
	"libsuspend.so",
	"libsync.so",
	"libsysutils.so",
	"libtextclassifier.so",
	"libtextclassifier_hash.so",
	"libtinyalsa.so",
	"libtinycompress.so",
	"libtinyxml2.so",
	"libtombstoned_client.so",
	"libui.so",
	"libunwind.so",
	"libunwindstack.so",
	"libusbhost.so",
	"libutils.so",
	"libutilscallstack.so",
	"libvintf.so",
	"libvisualizer.so",
	"libvixl-arm.so",
	"libvixl-arm64.so",
	"libvndksupport.so",
	"libvorbisidec.so",
	"libvulkan.so",
	"libwavextractor.so",
	"libwebrtc_audio_preprocessing.so",
	"libwebviewchromium_loader.so",
	"libwebviewchromium_plat_support.so",
	"libwfds.so",
	"libwifi-service.so",
	"libwifi-system-iface.so",
	"libwifi-system.so",
	"libwifikeystorehal.so",
	"libwilhelm.so",
	"libxml2.so",
	"libyuv.so",
	"libz.so",
	"libziparchive.so",
]

IGNORE_FILENAMES = [
	# Property files
	"build.prop",
	"default.prop",

	# config.fs
	"fs_config_dirs",
	"fs_config_files",
	"group",

	# Licenses
	"NOTICE.xml.gz",
	"NOTICE_GPL.html.gz",
	"NOTICE_GPL.xml.gz",
	"passwd",

	# Recovery patch
	"recovery-from-boot.p",

	# Partition symlinks
	"odm",
	"product",
	"system",
	"system_ext",
	"vendor",
]

IGNORE_EXTENSIONS = [
	# Apps's odex/vdex
	"odex",
	"vdex",
]

IGNORE_FOLDERS = [
	# Hostapd config
	"etc/hostapd",

	# Device init scripts
	"etc/init/hw",

	# Permissions
	"etc/permissions",

	# SELinux
	"etc/selinux",

	# Kernel modules
	"lib/modules",

	# ADSP tests
	"lib/rfsa/adsp/tests",

	# RRO overlays
	"overlay",

	# RFS symlinks
	"rfs",
]

IGNORE_PATHS = [
	# VINTF
	"etc/vintf/compatibility_matrix.xml",
	"etc/vintf/manifest.xml",
]

IGNORE_PATTERNS = [re.compile(pattern) for pattern in [
	# Shell scripts
	r"bin/.*\\.sh",

	# TODO: Find a cleaner way to exclude AOSP interfaces libs,
	# We're currently excluding all AOSP interfaces libs except impl
	r"^(?!lib(64)?/(hw/)?android\\..*\\..*-impl.*.so)lib(64)?/(hw/)?android\\..*\\..*.so",
	# Versioned libprotobuf library
	"lib(64)?/libprotobuf-cpp-(full|lite)-.*.so",
]]

def is_blob_allowed(file: Path) -> bool:
	"""
	Check if the lib is not in the disallowed list.
	"""
	if file.name in IGNORE_BINARIES:
		return False

	if file.name in IGNORE_SHARED_LIBS:
		return False

	if file.name in IGNORE_FILENAMES:
		return False

	if removeprefix(file.suffix, '.') in IGNORE_EXTENSIONS:
		return False

	for folder in [str(folder) for folder in file.parents]:
		if folder in IGNORE_FOLDERS:
			return False

	if str(file) in IGNORE_PATHS:
		return False

	for pattern in IGNORE_PATTERNS:
		if pattern.match(str(file)):
			return False

	return True
