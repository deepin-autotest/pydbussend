import os
import sys


def install_depends():
    python_path = sys.executable
    site_packages_path = os.path.join(
        os.path.dirname(os.path.dirname(python_path)),
        'lib',
        f'python{sys.version_info.major}.{sys.version_info.minor}',
        'site-packages'
    )
    for p in [
        "python3-dbus",
    ]:
        wheel_name = p.split("-")[-1].upper()
        if not os.path.exists(os.path.join(site_packages_path, wheel_name)):
            os.system(f"apt download {p} > /dev/null 2>&1")
            os.system(f"dpkg -x {p}*.deb {p}")
            os.system(f"cp -r {p}/usr/lib/python3/dist-packages/* {site_packages_path}/")
            os.system(f"rm -rf {p}*")


if __name__ == '__main__':
    install_depends()
