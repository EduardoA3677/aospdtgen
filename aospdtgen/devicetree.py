#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from aospdtgen.lib.libprop import BuildProp
from aospdtgen.proprietary_files.proprietary_files_list import ProprietaryFilesList
from aospdtgen.templates import render_template
from aospdtgen.utils.boot_configuration import BootConfiguration
from aospdtgen.utils.device_info import DeviceInfo
from aospdtgen.utils.fstab import Fstab
from aospdtgen.utils.ignored_props import IGNORED_PROPS
from aospdtgen.utils.partition import PartitionModel
from aospdtgen.utils.partitions import Partitions
from aospdtgen.utils.reorder import reorder_key
from datetime import datetime
from pathlib import Path
from shutil import rmtree

class DeviceTree:
	"""Class representing an Android device tree."""
	def __init__(self, path: Path):
		"""Given a path to a dumpyara dump path, generate a device tree by parsing it."""
		self.path = path

		self.current_year = str(datetime.now().year)

		# All files
		self.all_files_txt = self.path / "all_files.txt"
		self.all_files = [file for file in self.all_files_txt.open().read().splitlines()
		                  if (self.path / file).is_file()]
		self.all_files = list(dict.fromkeys(self.all_files))
		self.all_files.sort(key=reorder_key)
		self.all_files = [self.path / file for file in self.all_files]

		self.partitions = Partitions(self.path)

		self.system = self.partitions.get_partition(PartitionModel.SYSTEM)
		self.vendor = self.partitions.get_partition(PartitionModel.VENDOR)

		# Associate files with partitions
		for partition in self.partitions.get_all_partitions():
			partition.fill_files(self.all_files)

		# Parse build prop and device info
		self.build_prop = BuildProp()
		for partition in self.partitions.get_all_partitions():
			self.build_prop.import_props(partition.build_prop)
		self.device_info = DeviceInfo(self.build_prop)

		# Parse fstab
		fstab = None
		for file in [file for file in self.vendor.files if file.relative_to(self.vendor.real_path).is_relative_to("etc") and file.name.startswith("fstab.")]:
			if file.is_file():
				fstab = file
				break
		self.fstab = Fstab(fstab)

		# Let the partitions know their fstab entries if any
		for partition in self.partitions.get_all_partitions():
			partition.fill_fstab_entry(self.fstab)

		# Get a list of A/B partitions
		self.ab_partitions: list[PartitionModel] = []
		if self.device_info.device_is_ab:
			for fstab_entry in self.fstab.get_slotselect_partitions():
				partition_model = PartitionModel.from_mount_point(fstab_entry.mount_point)
				if partition_model is None:
					continue

				self.ab_partitions.append(partition_model)

		# Extract boot image
		self.boot_configuration = BootConfiguration(self.path / "boot.img",
		                                            self.path / "dtbo.img",
		                                            self.path / "recovery.img",
		                                            self.path / "vendor_boot.img")

		# Get list of rootdir files
		self.rootdir_bin_files = [file for file in self.vendor.files
		                          if file.relative_to(self.vendor.real_path).is_relative_to("bin")
		                          and file.suffix == ".sh"]
		self.rootdir_etc_files = [file for file in self.vendor.files
		                          if file.relative_to(self.vendor.real_path).is_relative_to("etc/init/hw")]
		
		recovery_resources_location = (self.boot_configuration.recovery_aik_manager.ramdisk_path
		                               if self.boot_configuration.recovery_aik_manager
		                               else self.boot_configuration.boot_aik_manager.ramdisk_path)
		self.rootdir_recovery_etc_files = [file for file in recovery_resources_location.iterdir()
		                                   if file.relative_to(recovery_resources_location).is_relative_to(".")
		                                   and file.suffix == ".rc"]

		# Generate proprietary files list
		self.proprietary_files_list = ProprietaryFilesList(self.partitions.get_all_partitions())

	def dump_to_folder(self, folder: Path):
		"""Dump all makefiles, blueprint and prebuilts to a folder."""
		if folder.is_dir():
			rmtree(folder)
		folder.mkdir(parents=True)

		# Makefiles/blueprints
		self._render_template(folder, "Android.bp", comment_prefix="//")
		self._render_template(folder, "Android.mk")
		self._render_template(folder, "AndroidProducts.mk")
		self._render_template(folder, "BoardConfig.mk")
		self._render_template(folder, "device.mk")
		self._render_template(folder, "extract-files.sh")
		self._render_template(folder, "lineage_device.mk", out_file=f"lineage_{self.device_info.codename}.mk")
		self._render_template(folder, "README.md")
		self._render_template(folder, "setup-makefiles.sh")

		# Proprietary files list
		(folder / "proprietary-files.txt").write_text(
				self.proprietary_files_list.get_formatted_list(self.device_info.build_description))

		# Dump build props
		for partition in self.partitions.get_all_partitions():
			if not partition.build_prop:
				continue

			(folder / f"{partition.model.name}.prop").write_text(partition.build_prop.get_readable_list(IGNORED_PROPS))

		# Dump boot image prebuilt files
		prebuilts_path = folder / "prebuilts"
		prebuilts_path.mkdir()

		self.boot_configuration.copy_files_to_folder(prebuilts_path)

		# Dump rootdir
		rootdir_path = folder / "rootdir"
		rootdir_path.mkdir()

		self._render_template(rootdir_path, "rootdir_Android.bp", "Android.bp", comment_prefix="//")
		self._render_template(rootdir_path, "rootdir_Android.mk", "Android.mk")

		# rootdir/bin
		rootdir_bin_path = rootdir_path / "bin"
		rootdir_bin_path.mkdir()

		for file in self.rootdir_bin_files:
			(rootdir_bin_path / file.name).write_bytes(file.read_bytes())

		# rootdir/etc
		rootdir_etc_path = rootdir_path / "etc"
		rootdir_etc_path.mkdir()

		for file in self.rootdir_etc_files + self.rootdir_recovery_etc_files:
			(rootdir_etc_path / file.name).write_bytes(file.read_bytes())

		(rootdir_etc_path / self.fstab.fstab.name).write_bytes(self.fstab.fstab.read_bytes())

		# Manifest
		(folder / "manifest.xml").write_text(str(self.vendor.manifest))

	def cleanup(self) -> None:
		"""
		Cleanup all the temporary files.

		After you call this, you should throw away this object and never use it anymore.
		"""
		self.boot_configuration.cleanup()

	def _render_template(self, *args, comment_prefix: str = "#", **kwargs):
		return render_template(*args,
		                       ab_partitions=self.ab_partitions,
		                       boot_configuration=self.boot_configuration,
		                       comment_prefix=comment_prefix,
		                       current_year=self.current_year,
		                       device_info=self.device_info,
		                       fstab=self.fstab,
		                       rootdir_bin_files=self.rootdir_bin_files,
		                       rootdir_etc_files=self.rootdir_etc_files,
		                       rootdir_recovery_etc_files=self.rootdir_recovery_etc_files,
		                       partitions=self.partitions,
		                       **kwargs)
