#!/bin/bash
echo "Enabling i2c..."
echo "# Added by arch_post_install.sh" >> /boot/config.txt && echo "dtparam=i2c_arm=on" >> /boot/config.txt
echo "i2c-dev" >> /etc/modules-load.d/raspberrypi.conf
/usr/bin/echo "Syncing pacman, installing packages..."
/usr/bin/sed -i 's/#Color/Color/' /etc/pacman.conf
/usr/bin/pacman-key --init
/usr/bin/pacman-key --populate archlinuxarm
/usr/bin/pacman -Syu
/usr/bin/pacman -S --needed i2c-tools lm_sensors nfs-utils base-devel \
                binutils diffutils libnewt dialog wireless_tools iw crda lshw pkgfile vim git go rxvt-unicode \
                bc gcc make htop bash-completion man which linux-headers dkms \
                usb_modeswitch file screen sudo pip swig