from aospdtgen.proprietary_files.section import Section, register_section

class WifiSection(Section):
	name = "Wi-Fi"
	interfaces = [
		"android.hardware.wifi",
		"vendor.mediatek.hardware.wifi.hostapd",
		"vendor.mediatek.hardware.wifi.supplicant",
		"vendor.qti.hardware.wifi.hostapd",
		"vendor.qti.hardware.wifi.keystore",
		"vendor.qti.hardware.wifi.supplicant",
		"vendor.qti.hardware.wifi.wifilearner",
	]
	binaries = [
		"hostapd",
		"wpa_supplicant",
	]

class WifiConfigsSection(Section):
	name = "Wi-Fi configs"
	folders = [
		"etc/wifi",
	]

class WifiFirmwareSection(Section):
	name = "Wi-Fi firmware"
	folders = [
		"firmware/wigig",
		"firmware/wlan",
	]

register_section(WifiSection)
register_section(WifiConfigsSection)
register_section(WifiFirmwareSection)
