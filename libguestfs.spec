# If you have trouble building locally ('make local') try adding
#   %libguestfs_buildnet 1
# to your ~/.rpmmacros file.

# Enable to build using a network repo
# Default is disabled
%if %{defined libguestfs_buildnet}
%global buildnet %{libguestfs_buildnet}
%else
%global buildnet 0
%endif 

# Enable to make the appliance use virtio_blk
# Default is enabled
%if %{defined libguestfs_virtio}
%global with_virtio %{libguestfs_virtio}
%else
%global with_virtio 1
%endif 

# Mirror and updates repositories to use if building with network repo
%if %{defined libguestfs_mirror}
%global mirror %{libguestfs_mirror}
%else
%global mirror http://download.fedora.redhat.com/pub/fedora/linux/development/%{_arch}/os/
%endif
%if %{defined libguestfs_updates}
%global updates %{libguestfs_updates}
%else
%global updates none
%endif

# Enable to run tests during check
# Default is enabled
%if %{defined libguestfs_runtests}
%global runtests %{libguestfs_runtests}
%else
%global runtests 1
%endif

Summary:       Access and modify virtual machine disk images
Name:          libguestfs
Epoch:         1
Version:       1.2.7
Release:       1.24%{?dist}
License:       LGPLv2+
Group:         Development/Libraries
URL:           http://libguestfs.org/
Source0:       http://libguestfs.org/download/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
ExclusiveArch: x86_64

# Disable FUSE tests, not supported in Koji at the moment.
Patch0:        libguestfs-1.0.79-no-fuse-test.patch

# Backport the new API aug_clear from upstream development branch.
Patch1:        libguestfs-1.2.5-aug-clear-full.patch

# Backport supermin unification patch from upstream.
Patch2:        libguestfs-1.2.7-unify-supermin.patch

# Backport ignore utempter binaries patch from upstream.
Patch3:        libguestfs-1.2.7-ignore-utempter-binaries.patch

# Backport guestfish 'help' command error status from stable 1.2 branch.
# RHBZ#598771
Patch4:        libguestfs-1.2.7-guestfish-help-error-status.patch

# Don't fail if -m and --listen flags both given to guestfish (RHBZ#609990).
Patch5:        libguestfs-1.2.7-guestfish-dont-fail-if-m-and-listen-flags.patch

# Fix guestfs_add_cdrom in RHEL 6 (RHBZ#598807).
Patch6:        libguestfs-1.2.7-fix-add-cdrom-in-RHEL-6.patch

# In guestfs_mkfs_b, map block size to cluster size for VFAT and NTFS.
# RHBZ#600148
Patch7:        libguestfs-1.2.7-mkfs-b-map-block-size-to-cluster-size.patch

# Mount operations on unclean filesystems fail when drives are added
# readonly (RHBZ#617165).
Patch8:        libguestfs-1.2.7-revert-readonly-option.patch

# Backport upstream patch to use augeas's lens for modules.conf
Patch9:        libguestfs-1.2.7-use_augeas_modules_conf_lens.patch

# Backport upstream patch to use link-local addresses for host<->guest
Patch10:        libguestfs-1.2.7-link_local_addresses.patch

# Backport new API is_lv from upstream development branch.
Patch11:        libguestfs-1.2.7-is-lv-full.patch


# Basic build requirements:
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/bin/pod2text
BuildRequires: febootstrap >= 2.7
BuildRequires: hivex-devel >= 1.2.2
BuildRequires: augeas-devel >= 0.5.0
BuildRequires: readline-devel
BuildRequires: genisoimage
BuildRequires: libxml2-devel
BuildRequires: createrepo
BuildRequires: glibc-static
BuildRequires: libselinux-devel
BuildRequires: fuse-devel

# RHBZ#612309, and see note below.
BuildRequires: qemu-kvm >= 2:0.12.1.0
BuildRequires: qemu-kvm < 2:0.12.2.0

# This is only needed for RHEL 5 because readline-devel doesn't
# properly depend on it, but doesn't do any harm on other platforms:
BuildRequires: ncurses-devel

# Build requirements for the appliance (see 'make.sh.in' in the source):
BuildRequires: kernel, bash, coreutils, lvm2, util-linux-ng
BuildRequires: MAKEDEV, net-tools, augeas-libs, file
BuildRequires: module-init-tools, procps, strace, iputils
BuildRequires: e2fsprogs
BuildRequires: dosfstools, lsof, scrub, libselinux
BuildRequires: parted, btrfs-progs, gfs2-utils
BuildRequires: vim-minimal
BuildRequires: binutils
%ifarch %{ix86} x86_64
BuildRequires: grub
%endif
# Not available in RHEL-6:
#BuildRequires: hfsplus-tools, nilfs-utils, reiserfs-utils
#BuildRequires: jfsutils, gfs-utils
#BuildRequires: zerofree
#BuildRequires: ntfs-3g, ntfsprogs
# xfsprogs is a layered product (RHBZ#630986).
#BuildRequires: xfsprogs

# Must match the above set of BuildRequires exactly!
Requires:      kernel, bash, coreutils, lvm2, util-linux-ng
Requires:      MAKEDEV, net-tools, augeas-libs, file
Requires:      module-init-tools, procps, strace, iputils
Requires:      e2fsprogs
Requires:      dosfstools, lsof, scrub, libselinux
Requires:      parted, btrfs-progs, gfs2-utils
Requires:      vim-minimal
Requires:      binutils
%ifarch %{ix86} x86_64
Requires:      grub
%endif
# Not available in RHEL-6:
#Requires:      hfsplus-tools, nilfs-utils, reiserfs-utils
#Requires:      jfsutils, gfs-utils
#Requires:      zerofree
#Requires:      ntfs-3g, ntfsprogs
# xfsprogs is a layered product (RHBZ#630986).
#Requires:      xfsprogs

# These are only required if you want to build the bindings for
# different languages:
BuildRequires: ocaml
BuildRequires: ocaml-findlib-devel
BuildRequires: ocaml-xml-light-devel
BuildRequires: perl-devel
BuildRequires: perl-Test-Simple
BuildRequires: perl-Test-Pod
BuildRequires: perl-Test-Pod-Coverage
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-XML-Writer
BuildRequires: perl-libintl
BuildRequires: python-devel
BuildRequires: ruby-devel
BuildRequires: rubygem-rake
BuildRequires: java >= 1.5.0
BuildRequires: jpackage-utils
BuildRequires: java-devel

# For libguestfs-tools:
BuildRequires: perl-Sys-Virt

Requires:      febootstrap >= 2.7

# If we rebase qemu in RHEL 6.1, don't allow this RPM to be mixed with
# qemu-kvm RPMs from 6.1 (RHBZ#612309).
Requires:      qemu-kvm >= 2:0.12.1.0
Requires:      qemu-kvm < 2:0.12.2.0

# For libguestfs-test-tool.
Requires:      genisoimage

# Provide our own custom requires for the supermin appliance.
Source1:       libguestfs-find-requires.sh
%global _use_internal_dependency_generator 0
%global __find_provides %{_rpmconfigdir}/find-provides
%global __find_requires %{SOURCE1} %{_rpmconfigdir}/find-requires


%description
Libguestfs is a library for accessing and modifying guest disk images.
Amongst the things this is good for: making batch configuration
changes to guests, getting disk used/free statistics (see also:
virt-df), migrating between virtualization systems (see also:
virt-p2v), performing partial backups, performing partial guest
clones, cloning guests and changing registry/UUID/hostname info, and
much else besides.

Libguestfs uses Linux kernel and qemu code, and can access any type of
guest filesystem that Linux and qemu can, including but not limited
to: ext2/3/4, btrfs, FAT and NTFS, LVM, many different disk partition
schemes, qcow, qcow2, vmdk.

Libguestfs provides ways to enumerate guest storage (eg. partitions,
LVs, what filesystem is in each LV, etc.).  It can also run commands
in the context of the guest.

Libguestfs is a library that can be linked with C and C++ management
programs.

See also the 'guestfish' package for shell scripting and command line
access, and '%{name}-mount' for mounting guest filesystems on the
host using FUSE.

For Perl bindings, see 'perl-libguestfs'.

For OCaml bindings, see 'ocaml-libguestfs-devel'.

For Python bindings, see 'python-libguestfs'.

For Ruby bindings, see 'ruby-libguestfs'.

For Java bindings, see 'libguestfs-java-devel'.


%package devel
Summary:       Development tools and libraries for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%package -n guestfish
Summary:       Shell for accessing and modifying virtual machine disk images
Group:         Development/Tools
License:       GPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      /usr/bin/pod2text
Requires:      virt-inspector


%description -n guestfish
Guestfish is the Filesystem Interactive SHell, for accessing and
modifying virtual machine disk images from the command line and shell
scripts.


%package mount
Summary:       Mount guest filesystems on the host using FUSE and libguestfs
Group:         Development/Tools
License:       GPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      virt-inspector


%description mount
The guestmount command lets you mount guest filesystems on the
host using FUSE and %{name}.


%package tools
Summary:       System administration tools for virtual machines
Group:         Development/Tools
License:       GPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      guestfish
Requires:      perl-Sys-Virt
Requires:      perl-XML-Writer
Requires:      hivex >= 1.2.1

# Obsolete and replace earlier packages.
Provides:      virt-cat = %{epoch}:%{version}-%{release}
Obsoletes:     virt-cat < %{epoch}:%{version}-%{release}
Provides:      virt-df = %{epoch}:%{version}-%{release}
Obsoletes:     virt-df < %{epoch}:%{version}-%{release}
Provides:      virt-inspector = %{epoch}:%{version}-%{release}
Obsoletes:     virt-inspector < %{epoch}:%{version}-%{release}

# RHBZ#514309
Provides:      virt-df2 = %{epoch}:%{version}-%{release}
Obsoletes:     virt-df2 < %{epoch}:%{version}-%{release}

# These were never packages:
Provides:      virt-edit = %{epoch}:%{version}-%{release}
Provides:      virt-rescue = %{epoch}:%{version}-%{release}


%description tools
This package contains miscellaneous system administrator command line
tools for virtual machines.

Virt-cat is a command line tool to display the contents of a file in a
virtual machine.

Virt-df is a command line tool to display free space on virtual
machine filesystems.  Unlike other tools, it doesn’t just display the
amount of space allocated to a virtual machine, but can look inside
the virtual machine to see how much space is really being used.  It is
like the df(1) command, but for virtual machines, except that it also
works for Windows virtual machines.

Virt-edit is a command line tool to edit the contents of a file in a
virtual machine.

Virt-inspector examines a virtual machine and tries to determine the
version of the OS, the kernel version, what drivers are installed,
whether the virtual machine is fully virtualized (FV) or
para-virtualized (PV), what applications are installed and more.

Virt-list-filesystems can be used to list out the filesystems in a
virtual machine image (for shell scripts etc).

Virt-list-partitions can be used to list out the partitions in a
virtual machine image.

Virt-ls is a command line tool to list out files in a virtual machine.

Virt-rescue provides a rescue shell for making interactive,
unstructured fixes to virtual machines.

Virt-resize can resize existing virtual machine disk images.

Virt-tar is an archive, backup and upload tool for virtual machines.

Virt-win-reg lets you look inside the Windows Registry for
Windows virtual machines.


%package -n ocaml-%{name}
Summary:       OCaml bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:       OCaml bindings for %{name}
Group:         Development/Libraries
Requires:      ocaml-%{name} = %{epoch}:%{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.


%package -n perl-%{name}
Summary:       Perl bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# RHBZ#523547
Requires:      perl-XML-XPath


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%package -n python-%{name}
Summary:       Python bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%package -n ruby-%{name}
Summary:       Ruby bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      ruby(abi) = 1.8
Provides:      ruby(guestfs) = %{version}

%{!?ruby_sitelib: %define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%package java
Summary:       Java bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      java >= 1.5.0
Requires:      jpackage-utils

%description java
%{name}-java contains Java bindings for %{name}.

If you want to develop software in Java which uses %{name}, then
you will also need %{name}-java-devel.


%package java-devel
Summary:       Java development package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-java = %{epoch}:%{version}-%{release}

%description java-devel
%{name}-java-devel contains the tools for developing Java software
using %{name}.

See also %{name}-javadoc.


%package javadoc
Summary:       Java documentation for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-java = %{epoch}:%{version}-%{release}
Requires:      jpackage-utils

%description javadoc
%{name}-javadoc contains the Java documentation for %{name}.


%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
rm -f appliance/make.sh

mkdir -p daemon/m4


%build
%if %{buildnet}
%define extra --with-mirror=%{mirror} --with-repo=rhel-6 --with-updates=%{updates}
%else
# Build a local repository containing the packages used to
# install the current buildroot (assuming we are being built
# with mock or Koji).  Then tell febootstrap to reference this
# local repository when building the appliance.
mkdir repo
find /var/cache/yum -type f -name '*.rpm' -print0 | xargs -0 cp -t repo
createrepo repo
%define extra --with-mirror=file://$(pwd)/repo --with-repo=rhel-6 --with-updates=none
%endif

./configure \
  --prefix=%{_prefix} --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --with-qemu="qemu-kvm qemu-system-%{_build_arch} qemu" \
  --enable-debug-command \
  --enable-supermin \
%if %{with_virtio}
  --with-drive-if=virtio \
%endif
  %{extra}

# This ensures that /usr/sbin/chroot is on the path.  Not needed
# except for RHEL 5, it shouldn't do any harm on other platforms.
export PATH=/usr/sbin:$PATH

# 'INSTALLDIRS' ensures that perl libs are installed in the vendor dir
# not the site dir.
make INSTALLDIRS=vendor %{?_smp_mflags}

# Useful for debugging appliance problems.
echo "==== files in initramfs ===="
find initramfs -type f
echo "==== hostfiles ===="
ls -l appliance/supermin.d/hostfiles
cat appliance/supermin.d/hostfiles
echo "============"


%check
# Enable debugging - very useful if a test does fail, although
# it produces masses of output in the build.log.
export LIBGUESTFS_DEBUG=1

# Uncomment one of these, depending on whether you want to
# do a very long and thorough test ('make check') or just
# a quick test to see if things generally work.

# Tracking test issues:
# BZ       archs        branch reason
# 494075   ppc, ppc64          openbios bug causes "invalid/unsupported opcode"
# 504273   ppc, ppc64          "no opcode defined"
# 505109   ppc, ppc64          "Boot failure! No secondary bootloader specified"
# 502058   i386, x86-64 F-11   need to boot with noapic (WORKAROUND ENABLED)
# 502074   i386         all    commands segfault randomly
# 503236   i386         F-12   cryptomgr_test at doublefault_fn
# 507066   all          F-12   sequence of chroot calls (FIXED)
# 513249   all          F-12   guestfwd broken in qemu (FIXED)
# 516022   all          F-12   virtio-net gives "Network is unreachable" errors
#                                 (FIXED)
# 516096   ?            F-11   race condition in swapoff/blockdev --rereadpt
# 516543   ?            F-12   qemu-kvm segfaults when run inside a VM (FIXED)
# 548121   all          F-13   udevsettle command is broken (WORKAROUND)
# 553689   all          F-13   missing SeaBIOS (FIXED)
# 563103   all          F-13   glibc incorrect emulation of preadv/pwritev
#                                 (WORKAROUND using LD_PRELOAD)
# 567567   32-bit       all    guestfish xstrtol test failure on 32-bit (FIXED)
# 575734   all          F-14   microsecond resolution for blkid cache
#                                 (FIXED upstream but still broken in F-14)

# Workaround #563103
cat > rhbz563103.c <<'EOF'
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
ssize_t preadv (int fd,...) { errno = ENOSYS; return -1; }
ssize_t preadv64 (int fd,...) { errno = ENOSYS; return -1; }
ssize_t pwritev (int fd,...) { errno = ENOSYS; return -1; }
ssize_t pwritev64 (int fd,...) { errno = ENOSYS; return -1; }
EOF
gcc -fPIC -c rhbz563103.c
gcc -shared -Wl,-soname,rhbz563103.so.1 rhbz563103.o -o rhbz563103.so
LD_PRELOAD=$(pwd)/rhbz563103.so
export LD_PRELOAD

# Workaround #575734 in F-14
export SKIP_TEST_MKE2JOURNAL_U=1
export SKIP_TEST_MKE2JOURNAL_L=1

# Unknown why this fails - could be also #575734.
export SKIP_TEST_SWAPON_LABEL=1

# Workaround buggy getlogin_r.c test in gnulib (no BZ number).
# Error is: test-getlogin_r.c:55: assertion failed
make -C daemon/tests check ||:
rm daemon/tests/test-getlogin_r
touch daemon/tests/test-getlogin_r
chmod +x daemon/tests/test-getlogin_r

%if %{runtests}
make check
%endif


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Delete the ordinary appliance, leaving just the supermin appliance.
rm $RPM_BUILD_ROOT%{_libdir}/guestfs/vmlinuz.*
rm $RPM_BUILD_ROOT%{_libdir}/guestfs/initramfs.*

# Delete static libraries, libtool files.
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs.a
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs.la

# Clean up the examples/ directory which will get installed in %doc.
# Note we can't delete the original examples/Makefile because that
# will be needed by the check section later in the RPM build.
cp -a examples ex
pushd ex
make clean
rm Makefile*
rm -rf .deps .libs
popd

# Same for ocaml/examples.
cp -a ocaml/examples ocaml/ex
pushd ocaml/ex
make clean
rm Makefile*
popd

find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete
find $RPM_BUILD_ROOT -name 'bindtests.pl' -delete

rm $RPM_BUILD_ROOT%{python_sitearch}/libguestfsmod.a
rm $RPM_BUILD_ROOT%{python_sitearch}/libguestfsmod.la

if [ "$RPM_BUILD_ROOT%{python_sitearch}" != "$RPM_BUILD_ROOT%{python_sitelib}" ]; then
   mkdir -p $RPM_BUILD_ROOT%{python_sitelib}
   mv $RPM_BUILD_ROOT%{python_sitearch}/guestfs.py* \
     $RPM_BUILD_ROOT%{python_sitelib}/
fi

# Install ruby bindings by hand.
mkdir -p $RPM_BUILD_ROOT%{ruby_sitelib}
mkdir -p $RPM_BUILD_ROOT%{ruby_sitearch}
install -p -m0644 ruby/lib/guestfs.rb $RPM_BUILD_ROOT%{ruby_sitelib}
install -p -m0755 ruby/ext/guestfs/_guestfs.so $RPM_BUILD_ROOT%{ruby_sitearch}

# Remove static-linked Java bindings.
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs_jni.a
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs_jni.la

# Move installed documentation back to the source directory so
# we can install it using a %%doc rule.
mv $RPM_BUILD_ROOT%{_docdir}/libguestfs installed-docs

# Find locale files.
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/libguestfs-test-tool
%{_libdir}/guestfs/
%{_libdir}/libguestfs.so.*
%{_libexecdir}/libguestfs-test-tool-helper
%{_mandir}/man1/libguestfs-test-tool.1*


%files devel
%defattr(-,root,root,-)
%doc ChangeLog HACKING TODO README ex html/guestfs.3.html html/pod.css
%doc installed-docs/*
%{_libdir}/libguestfs.so
%{_mandir}/man3/guestfs.3*
%{_mandir}/man3/libguestfs.3*
%{_includedir}/guestfs.h
%{_includedir}/guestfs-actions.h
%{_includedir}/guestfs-structs.h
%{_libdir}/pkgconfig/libguestfs.pc


%files -n guestfish
%defattr(-,root,root,-)
%doc html/guestfish.1.html html/pod.css recipes/
%{_bindir}/guestfish
%{_mandir}/man1/guestfish.1*


%files mount
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/guestmount
%{_mandir}/man1/guestmount.1*


%files tools
%defattr(-,root,root,-)
%{_bindir}/virt-cat
%{_mandir}/man1/virt-cat.1*
%{_bindir}/virt-df
%{_mandir}/man1/virt-df.1*
%{_bindir}/virt-edit
%{_mandir}/man1/virt-edit.1*
%{_bindir}/virt-inspector
%{_mandir}/man1/virt-inspector.1*
%{_bindir}/virt-list-filesystems
%{_mandir}/man1/virt-list-filesystems.1*
%{_bindir}/virt-list-partitions
%{_mandir}/man1/virt-list-partitions.1*
%{_bindir}/virt-ls
%{_mandir}/man1/virt-ls.1*
%{_bindir}/virt-rescue
%{_mandir}/man1/virt-rescue.1*
%{_bindir}/virt-resize
%{_mandir}/man1/virt-resize.1*
%{_bindir}/virt-tar
%{_mandir}/man1/virt-tar.1*
%{_bindir}/virt-win-reg
%{_mandir}/man1/virt-win-reg.1*


%files -n ocaml-%{name}
%defattr(-,root,root,-)
%doc README
%{_libdir}/ocaml/guestfs
%exclude %{_libdir}/ocaml/guestfs/*.a
%exclude %{_libdir}/ocaml/guestfs/*.cmxa
%exclude %{_libdir}/ocaml/guestfs/*.cmx
%exclude %{_libdir}/ocaml/guestfs/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files -n ocaml-%{name}-devel
%defattr(-,root,root,-)
%doc ocaml/ex
%{_libdir}/ocaml/guestfs/*.a
%{_libdir}/ocaml/guestfs/*.cmxa
%{_libdir}/ocaml/guestfs/*.cmx
%{_libdir}/ocaml/guestfs/*.mli


%files -n perl-%{name}
%defattr(-,root,root,-)
%doc perl/examples
%{perl_vendorarch}/*
%{_mandir}/man3/Sys::Guestfs.3pm*
%{_mandir}/man3/Sys::Guestfs::Lib.3pm*


%files -n python-%{name}
%defattr(-,root,root,-)
%doc README
%{python_sitearch}/*
%{python_sitelib}/*.py
%{python_sitelib}/*.pyc
%{python_sitelib}/*.pyo


%files -n ruby-%{name}
%defattr(-,root,root,-)
%doc README
%{ruby_sitelib}/guestfs.rb
%{ruby_sitearch}/_guestfs.so


%files java
%defattr(-,root,root,-)
%doc README
%{_libdir}/libguestfs_jni*.so.*
%{_datadir}/java/*.jar


%files java-devel
%defattr(-,root,root,-)
%doc README
%{_libdir}/libguestfs_jni*.so


%files javadoc
%defattr(-,root,root,-)
%doc README
%{_datadir}/javadoc/%{name}-java-%{version}


%changelog
* Tue Sep  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.24
- Remove runtime requires xfsprogs and /lib64/libhandle.so.1 (RHBZ#630986).
  Note that we have removed support completely from the appliance.  Even
  installing xfsprogs separately will not provide support in this
  build of libguestfs.

* Wed Aug  4 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.23
- Backport new API is_lv from upstream development branch (RHBZ#619826).

* Fri Jul 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.22
- Include generated code in patch for RHBZ#617165.

* Mon Jul 26 2010 Matthew Booth <mbooth@redhat.com> - 1:1.2.7-1.21
- Rely on upstream augeas lens for modules.conf (RHBZ#616753)
- Use link-local addresses for host<->guest communication (RHBZ#613562)

* Fri Jul 23 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.20
- Mount operations on unclean filesystems fail when drives are added
  readonly (RHBZ#617165).

* Tue Jul 20 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.18
- Missing Requires binutils (RHBZ#616438).

* Mon Jul 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.17
- Fix libguestfs-find-requires.sh for new location of hostfiles (RHBZ#615870).

* Thu Jul  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.16
- Don't allow this RPM to be mixed with qemu-kvm RPM from 6.1 (RHBZ#612309).

* Wed Jul  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.11
- For RHBZ#600148:
  * In guestfs_mkfs_b, map block size to cluster size for VFAT and NTFS
  * Remove power-of-2 test from API tests.  Not supported by backported
    code.

* Wed Jul  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.9
- Fix 'add-cdrom' command in RHEL 6 (RHBZ#598807).

* Wed Jul  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.8
- Don't fail if both -m and --listen flags given to guestfish (RHBZ#609990).

* Wed Jul  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.7
- Don't add extra chars after dist tag (RHBZ#604552).

* Wed Jul  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.el6.6
- Backport guestfish help command error status patch from stable branch
  (RHBZ#598771).

* Tue May 18 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1.el6.5
- Backport ignore utempter patch from upstream.
- Work around buggy getlogin_r test in gnulib.
- Explicitly depend on e2fsprogs (no longer pulled in implicitly).

* Mon May 17 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.7-1
- Pull in latest release of upstream stable branch.
- Remove NTFS support from this package.
- Backport supermin unification patch from upstream development branch.

* Wed Apr 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.5-1.el6.5
- Branch from Fedora 13 and compile for RHEL-6.
- Include NTFS support in the appliance for V2V and other virtualization
  operations on Windows guests.
- Backport aug_clear API from upstream development branch.

* Tue Apr 20 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.3-1
- New upstream stable branch version 1.2.3.
- Fixes: 582548, 583554, 582948, 582901, 582929, 582899, 582953,
  578407.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.2-1
- New upstream stable branch version 1.2.2.
- Fixes RHBZ#580016.
- Fixes several important bugs in virt-resize.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.2.1-1
- New upstream stable branch version 1.2.1.
- Includes the new tools virt-list-partitions, virt-resize, and
  updated virt-rescue and virt-win-reg (with regedit support).
- Reenable tests.
- Fixes bugs: 580650, 579155, 580246, 579664, 578123, 509597,
  505329, 576876, 576688, 576689, 569757, 567567, 570181.

* Fri Mar 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-2.4
- Backport upstream patch to remove dependency on /lib/libntfs-3g.so.N.
- The above depends on the bash quoting patch, so apply that first.

* Mon Mar 08 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-2.3
- Rebuild against latest plymouth in F-13 updates-testing.

* Mon Mar 08 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-2.2
- Bump and rebuild.

* Fri Mar 05 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-2.1
- Bump and rebuild.

* Wed Mar 03 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-2
- Bump and rebuild.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-1
- New upstream version 1.0.85.
- Remove hivex, now a separate upstream project and package.
- Remove supermin quoting patch, now upstream.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-6
- Fix quoting in supermin-split script (RHBZ#566511).
- Don't include bogus './builddir' entries in supermin hostfiles
  (RHBZ#566512).

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-4
- Don't include generator.ml in rpm.  It's 400K and almost no one will need it.
- Add comments to spec file about how repo building works.
- Whitespace changes in the spec file.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-3
- Bump and rebuild.

* Tue Feb 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-2
- Bump and rebuild.

* Fri Feb 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-1
- New upstream version 1.0.84.

* Fri Feb 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.83-8
- Bump and rebuild.

* Thu Feb 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-7
- Disable tests.  These fail in Koji (on RHEL 5 kernel) because of a
  bug in preadv/pwritev emulation in glibc (RHBZ#563103).

* Tue Feb  9 2010 Matthew Booth <mbooth@redhat.com> - 1.0.83-6
- Change buildnonet to buildnet
- Allow buildnet, mirror, updates, virtio and runtests to be configured by user
  macros.

* Mon Feb  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-5
- libguestfs-tools should require perl-XML-Writer (RHBZ#562858).

* Mon Feb  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-4
- Use virtio for block device access (RHBZ#509383 is fixed).

* Fri Feb  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-3
- Rebuild: possible timing-related build problem in Koji.

* Fri Feb  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-2
- New upstream release 1.0.83.
- This release fixes:
  Add Marathi translations (RHBZ#561671).
  Polish translations (RHBZ#502533).
  Add Gujarti translations (Sweta Kothari) (RHBZ#560918).
  Update Oriya translations (thanks Manoj Kumar Giri) (RHBZ#559498).
  Set locale in C programs so l10n works (RHBZ#559962).
  Add Tamil translation (RHBZ#559877) (thanks to I.Felix)
  Update Punjabi translation (RHBZ#559480) (thanks Jaswinder Singh)
- There are significant fixes to hive file handling.
- Add hivexsh and manual page.
- Remove two patches, now upstream.

* Sun Jan 31 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.82-7
- Bump and rebuild.

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-6
- Backport a better fix for RHBZ557655 test from upstream.
- Backport fix for unreadable yum.log from upstream.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-3
- Backport RHBZ557655 test fix from upstream.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-1
- New upstream version 1.0.82.  This includes the two patches
  we were carrying, so those are now removed.
- This release fixes:
  RHBZ#559498 (Oriya translation).
  RHBZ#559480 (Punjabi translation).
  RHBZ#558593 (Should prevent corruption by multilib).
  RHBZ#559237 (Telugu translation).
  RHBZ#557655 (Use xstrtol/xstrtoll to parse integers in guestfish).
  RHBZ#557195 (Missing crc kernel modules for recent Linux).
- In addition this contains numerous fixes to the hivex library
  for parsing Windows Registry files, making hivex* and virt-win-reg
  more robust.
- New API call 'filesize'.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-8
- Backport special handling of libgcc_s.so.
- Backport unreadable files patch from RHEL 6 / upstream.

* Fri Jan 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-5
- Require febootstrap >= 2.6 (RHBZ#557262).

* Thu Jan 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-4
- Rebuild for unannounced soname bump (libntfs-3g.so).

* Fri Jan 15 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-3
- Rebuild for unannounced soname bump (libplybootsplash.so).

* Thu Jan 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-2
- Rebuild for broken dependency (iptables soname bump).

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-1
- New upstream version 1.0.81.
- Remove two upstream patches.
- virt-inspector: Make RPM application data more specific (RHBZ#552718).

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-14
- Reenable tests because RHBZ#553689 is fixed.

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-13
- Rebuild because of libparted soname bump (1.9 -> 2.1).

* Fri Jan  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-12
- qemu in Rawhide is totally broken (RHBZ#553689).  Disable tests.

* Thu Jan  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-11
- Remove gfs-utils (deprecated and removed from Fedora 13 by the
  upstream Cluster Suite developers).
- Include patch to fix regression in qemu -serial stdio option.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-10
- Remove some debugging statements which were left in the requires
  script by accident.

* Mon Dec 21 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-9
- Generate additional requires for supermin (RHBZ#547496).

* Fri Dec 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-3
- Work around udevsettle command problem (RHBZ#548121).
- Enable tests.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-2
- Disable tests because of RHBZ#548121.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-1
- New upstream release 1.0.80.
- New Polish translations (RHBZ#502533).
- Give a meaningful error if no usable kernels are found (RHBZ#539746).
- New tool: virt-list-filesystems

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:1.0.79-3
- rebuild against perl 5.10.1

* Wed Nov 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.79-2
- New upstream release 1.0.79.
- Adds FUSE test script and multiple fixes for FUSE (RHBZ#538069).
- Fix virt-df in Xen (RHBZ#538041).
- Improve speed of supermin appliance.
- Disable FUSE-related tests because Koji doesn't currently allow them.
  fuse: device not found, try 'modprobe fuse' first

* Tue Nov 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.78-2
- New upstream release 1.0.78.
- Many more filesystem types supported by this release - add them
  as dependencies.

* Tue Nov  3 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.77-1
- New upstream release 1.0.77.
- Support for mounting guest in host using FUSE (guestmount command).
- hivex*(1) man pages should be in main package, not -devel, since
  they are user commands.
- libguestfs-tools: Fix "self-obsoletion" issue raised by rpmlint.
- perl: Remove bogus script Sys/bindtests.pl.

* Thu Oct 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.75-2
- New upstream release 1.0.75.
- New library: libhivex.
- New tools: virt-win-reg, hivexml, hivexget.
- Don't require chntpw.
- Add BR libxml2-devel, accidentally omitted before.

* Tue Oct 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.74-1
- New upstream release 1.0.74.
- New API call: guestfs_find0.
- New tools: virt-ls, virt-tar.

* Wed Oct 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.73-1
- New upstream release 1.0.73.
- OCaml library now depends on xml-light.
- Deal with installed documentation.

* Tue Sep 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.72-2
- Force rebuild.

* Wed Sep 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.72-1
- New upstream release 1.0.72.
- New tools: virt-edit, virt-rescue.
- Combine virt-cat, virt-df, virt-edit, virt-inspector and virt-rescue
  into a single package called libguestfs-tools.

* Tue Sep 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.71-2
- New upstream release 1.0.71.

* Fri Sep 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.70-2
- Perl bindings require perl-XML-XPath (fixed RHBZ#523547).

* Tue Sep 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.70-1
- New upstream release 1.0.70.
- Fixes build problem related to old version of GNU gettext.

* Tue Sep 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.69-1
- New upstream release 1.0.69.
- Reenable the tests (because RHBZ#516543 is supposed to be fixed).
- New main loop code should fix RHBZ#501888, RHBZ#504418.
- Add waitpid along guestfs_close path (fixes RHBZ#518747).

* Wed Aug 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.68-2
- New upstream release 1.0.68.
- BR genisoimage.

* Thu Aug 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.67-2
- New upstream release 1.0.67.

* Fri Aug  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.66-5
- Set network interface to ne2k_pci (workaround for RHBZ#516022).
- Rerun autoconf because patch touches configure script.

* Thu Aug  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.66-1
- New upstream release 1.0.66.

* Wed Jul 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.65-1
- New upstream release 1.0.65.
- Add Obsoletes for virt-df2 (RHBZ#514309).
- Disable tests because of ongoing TCG problems with newest qemu in Rawhide.

* Thu Jul 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.64-3
- RHBZ#513249 bug in qemu is now fixed, so try to rebuild and run tests.
- However RHBZ#503236 still prevents us from testing on i386.

* Thu Jul 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.64-1
- New upstream release 1.0.64.
- New tool 'libguestfs-test-tool'.

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.61-1
- New upstream release 1.0.61.
- New tool / subpackage 'virt-cat'.
- New BR perl-libintl.

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-2
- Fix runtime Requires so they use epoch correctly.

* Tue Jul 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-1
- New upstream release 1.0.60.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.58-2
- New upstream release 1.0.58.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.57-1
- New upstream release 1.0.57.
- New tool virt-df (obsoletes existing package with this name).
- RHBZ#507066 may be fixed, so reenable tests.

* Tue Jul  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.56-2
- New upstream release 1.0.56.
- Don't rerun generator.

* Thu Jul  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.55-1
- New upstream release 1.0.55.
- New manual page libguestfs(3).

* Mon Jun 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.54-2
- New upstream release 1.0.54.
- +BR perl-XML-Writer.

* Wed Jun 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.53-1
- New upstream release 1.0.53.
- Disable all tests (because of RHBZ#507066).

* Wed Jun 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.52-1
- New upstream release 1.0.52.

* Mon Jun 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.51-1
- New upstream release 1.0.51.
- Removed patches which are now upstream.

* Sat Jun 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.49-5
- Remove workaround for RHBZ#507007, since bug is now fixed.
- Pull in upstream patch to fix pclose checking
  (testing as possible fix for RHBZ#507066).
- Pull in upstream patch to check waitpid return values
  (testing as possible fix for RHBZ#507066).

* Fri Jun 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.49-2
- New upstream release 1.0.49.
- Add workaround for RHBZ#507007.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-2
- Accidentally omitted the supermin image from previous version.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-1
- New upstream release 1.0.48.
- Should fix all the brokenness from 1.0.47.
- Requires febootstrap >= 2.3.

* Mon Jun 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.47-2
- New upstream release 1.0.47.
- Enable experimental supermin appliance build.
- Fix path to appliance.

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.45-2
- New upstream release 1.0.45.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-2
- Disable ppc/ppc64 tests again because of RHBZ#505109.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-1
- New upstream version 1.0.44.
- Try enabling tests on ppc & ppc64 since it looks like the bug(s?)
  in qemu which might have caused them to fail have been fixed.

* Tue Jun  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.43-1
- New upstream version 1.0.43.
- New upstream URL.
- Requires chntpw program.

* Sat Jun  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.42-1
- New upstream version 1.0.42.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.41-1
- New upstream version 1.0.41.
- Fixes a number of regressions in RHBZ#503169.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.40-1
- New upstream version 1.0.40.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.39-1
- New upstream version 1.0.39.
- Fixes:
  . libguestfs /dev is too sparse for kernel installation/upgrade (RHBZ#503169)
  . OCaml bindings build failure (RHBZ#502309)

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-2
- Disable tests on ix86 because of RHBZ#503236.

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-1
- New upstream version 1.0.38.

* Fri May 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.37-1
- New upstream version 1.0.37.
- Fixes:
  . "mkdir-p" should not throw errors on preexisting directories (RHBZ#503133)
  . cramfs and squashfs modules should be available in libguestfs appliances
      (RHBZ#503135)

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.36-2
- New upstream version 1.0.36.
- Rerun the generator in prep section.

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.35-1
- New upstream version 1.0.35.
- Fixes multiple bugs in bindings parameters (RHBZ#501892).

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.34-1
- New upstream version 1.0.34.

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.33-1
- New upstream version 1.0.33.
- --with-java-home option is no longer required.
- Upstream contains potential fixes for:
    501878 built-in commands like 'alloc' and 'help' don't autocomplete
    501883 javadoc messed up in libguestfs java documentation
    501885 Doesn't detect missing Java, --with-java-home=no should not be needed
    502533 Polish translation of libguestfs
    n/a    Allow more ext filesystem kmods (Charles Duffy)

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.32-2
- New upstream version 1.0.32.
- Use %%find_lang macro.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.31-1
- Rebuild for OCaml 3.11.1.
- New upstream version 1.0.31.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.30-1
- New upstream version 1.0.30.  Now includes test-bootbootboot.sh script.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.29-3
- New upstream version 1.0.29 (fixes RHBZ#502007 RHBZ#502018).
- This should allow us to enable tests for i386 and x86-64.
- Added test-bootbootboot.sh script which was missed from 1.0.29 tarball.
- Pass kernel noapic flag to workaround RHBZ#502058.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.28-1
- New upstream version 1.0.28.  Nothing has visibly changed, but
  the source has been gettextized and we want to check that doesn't
  break anything.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.27-3
- Change requirement from qemu -> qemu-kvm (RHBZ#501761).

* Tue May 19 2009 Richard Jones <rjones@redhat.com> - 1.0.27-2
- New upstream version 1.0.27.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-6
- Experimentally try to reenable ppc and ppc64 builds.
- Note BZ numbers which are causing tests to fail.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-1
- New upstream version 1.0.26.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.25-4
- New upstream version 1.0.25.
- Enable debugging when running the tests.
- Disable tests - don't work correctly in Koji.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.24-1
- New upstream version 1.0.24.
- BRs glibc-static for the new command tests.
- Enable tests.

* Mon May 11 2009 Richard Jones <rjones@redhat.com> - 1.0.23-2
- New upstream version 1.0.23.
- Don't try to use updates during build.

* Fri May  8 2009 Richard Jones <rjones@redhat.com> - 1.0.21-3
- New upstream version 1.0.21.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.20-2
- New upstream version 1.0.20.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.19-1
- New upstream version 1.0.19.

* Tue Apr 28 2009 Richard Jones <rjones@redhat.com> - 1.0.15-1
- New upstream version 1.0.15.

* Fri Apr 24 2009 Richard Jones <rjones@redhat.com> - 1.0.12-1
- New upstream version 1.0.12.

* Wed Apr 22 2009 Richard Jones <rjones@redhat.com> - 1.0.6-1
- New upstream version 1.0.6.

* Mon Apr 20 2009 Richard Jones <rjones@redhat.com> - 1.0.2-1
- New upstream version 1.0.2.

* Thu Apr 16 2009 Richard Jones <rjones@redhat.com> - 0.9.9-12
- Multiple fixes to get it to scratch build in Koji.

* Sat Apr  4 2009 Richard Jones <rjones@redhat.com> - 0.9.9-1
- Initial build.
