# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import itertools
import os

WINDOW_T = "Recovery SD Card Uploader Tool"
WINDOW_W = 1280 
WINDOW_H = 720

UNITS = ("B", "KiB", "MiB", "GiB")

SOFTWARE = "Software"
OS_YOCTO = "yocto"
OS_DEBIAN = "debian"
OS_B2QT = "b2qt"

MX8_SOM_DT_8M       = "DART-MX8M"
MX8_SOM_DT_8M_MINI  = "DART-MX8M-MINI"
MX8_SOM_DT_8M_PLUS  = "DART-MX8M-PLUS"

YAML_CHANGELOG_MX8_SOM_DT_8M       = "dart-mx8m-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8_SOM_DT_8M_MINI  = "dart-mx8m-mini-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8_SOM_DT_8M_PLUS  = "dart-mx8m-plus-recovery-sd-changelog.yml"

MX8_SOM_DARTS = [MX8_SOM_DT_8M, MX8_SOM_DT_8M_MINI, MX8_SOM_DT_8M_PLUS]

MX8_SOM_VS_8        = "VAR-SOM-MX8"
MX8_SOM_VS_8X       = "VAR-SOM-MX8X"
MX8_SOM_VS_8M_NANO  = "VAR-SOM-MX8M-NANO"

YAML_CHANGELOG_MX8_SOM_VS_8        = "var-som-mx8-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8_SOM_VS_8X       = "var-som-mx8x-recovery-sd-changelog.yml"
YAML_CHANGELOG_MX8_SOM_VS_8M_NANO  = "var-som-mx8m-nano-recovery-sd-changelog.yml"

MX8_SOM_VARS = [MX8_SOM_VS_8, MX8_SOM_VS_8X, MX8_SOM_VS_8M_NANO]

MX8_YAML_CHANGELOG_FILES = {
         MX8_SOM_DT_8M : YAML_CHANGELOG_MX8_SOM_DT_8M,
         MX8_SOM_DT_8M_MINI : YAML_CHANGELOG_MX8_SOM_DT_8M_MINI,
         MX8_SOM_DT_8M_PLUS : YAML_CHANGELOG_MX8_SOM_DT_8M_PLUS,
         MX8_SOM_VS_8 : YAML_CHANGELOG_MX8_SOM_VS_8,
         MX8_SOM_VS_8X : YAML_CHANGELOG_MX8_SOM_VS_8X,
         MX8_SOM_VS_8M_NANO : YAML_CHANGELOG_MX8_SOM_VS_8M_NANO}

VAR_SYSTEM_ON_MODULES = list(itertools.chain(MX8_SOM_DARTS, MX8_SOM_VARS))

VAR_OS = ["yocto", "debian", "b2qt"]
