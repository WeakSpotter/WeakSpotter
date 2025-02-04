import enum
from dataclasses import dataclass


@dataclass
class LicenseInfo:
    name: str
    url: str
    # See https://www.gnu.org/licenses/license-list.html
    gpl_compatible: bool


class License(enum.Enum):
    GPLv3 = LicenseInfo(
        name="GNU General Public License v3",
        url="https://opensource.org/license/gpl-3-0",
        gpl_compatible=True,
    )

    GPLv2 = LicenseInfo(
        name="GNU General Public License v2",
        url="https://opensource.org/licenses/GPL-2.0",
        gpl_compatible=True,
    )

    BSD = LicenseInfo(
        name="BSD 3-Clause License",
        url="https://opensource.org/licenses/BSD-3-Clause",
        gpl_compatible=True,
    )

    MIT = LicenseInfo(
        name="MIT License",
        url="https://opensource.org/licenses/MIT",
        gpl_compatible=True,
    )

    Apachev2 = LicenseInfo(
        name="Apache License 2.0",
        url="https://opensource.org/licenses/Apache-2.0",
        gpl_compatible=True,
    )

    MPLv2 = LicenseInfo(
        name="Mozilla Public License",
        url="https://opensource.org/licenses/MPL-2.0",
        gpl_compatible=True,
    )

    NSPL = LicenseInfo(
        name="Nmap Public Source License",
        url="https://nmap.org/npsl/",
        gpl_compatible=True,
    )

    Empty = LicenseInfo(
        name="See LICENSE.md for the license",
        url="https://github.com/WeakSpotter/WeakSpotter/blob/main/LICENSE.md",
        gpl_compatible=True,
    )

    WPScan = LicenseInfo(
        name="WPScan License",
        url="https://wpscan.com/",
        gpl_compatible=False,
    )
