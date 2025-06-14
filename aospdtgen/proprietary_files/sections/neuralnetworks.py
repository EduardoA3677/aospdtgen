#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from aospdtgen.proprietary_files.section import Section, register_section

class NeuralNetworksSection(Section):
	name = "Neural networks"
	interfaces = [
		"android.hardware.neuralnetworks",
		"vendor.mediatek.hardware.mmagent",
	]
	binaries = [
		"nn_device_test",
		"npu_launcher",
	]
	libraries = [
		"libhexagon_nn_stub",
	]
	patterns = [
		r"lib(64)?/libhta(_.*.)?\.so",
		r"lib(64)?/unnhal.*.\.so",
	]

register_section(NeuralNetworksSection)
