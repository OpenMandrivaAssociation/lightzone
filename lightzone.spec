%undefine _debugsource_packages

%define oname LightZone
%define beta beta1

Name:		lightzone
Version:	5.0.0
Release:	%{?beta:0.%{beta}.}1
License:	BSD-3-Clause
Summary:	Open-source professional-level digital darkroom software
Url:		https://github.com/ktgw0316/LightZone/
Group:		Graphics
Source0:	https://github.com/ktgw0316/LightZone/archive/%{version}%{?beta:%{beta}}/%{oname}-%{version}%{?beta:%{beta}}.tar.gz
# Get the right commit hash from https://github.com/ktgw0316/LightZone/tree/master/lightcrafts
# FIXME this is broken, bundling prebuilt binaries is a really bad idea
Source1:	https://github.com/ktgw0316/lightzone-dependencies/archive/a402b56d5d39642f4250827e7b29060263d6dddb.tar.gz
Patch0:		LightZone-4.2.5-clang16.patch
BuildRequires:	ant
BuildRequires:	nasm
BuildRequires:  gomp-devel
BuildRequires:	tidy
BuildRequires:	git
BuildRequires:	javahelp2
BuildRequires:  jdk-current
BuildRequires:  java-gui-current
BuildRequires:	java-rpmbuild
BuildRequires:	pkgconfig(x11)
BuildRequires:  pkgconfig(lensfun)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libtiff-4)

Requires:	jre-current
Requires:	java-gui-current
Requires:	%{_lib}lzma5

%description
LightZone is open-source professional-level digital darkroom software for
Windows, Mac OS X, and Linux. Rather than using layers as many other photo
editors do, LightZone lets the user build up a stack of tools which can be
rearranged, turned off and on, and removed from the stack.

It's a non-destructive editor, where any of the tools can be re-adjusted or
modified later — even in a different editing session. A tool stack can be
copied to a batch of photos at one time. LightZone operates in a 16-bit
linear color space with the wide gamut of ProPhoto RGB.

%prep
%autosetup -p1 -n %{oname}-%{version}%{?beta:%{beta}} -a1
if [ %(echo %{version} |cut -d. -f1) -le 4 ]; then
	rmdir lightcrafts/dependencies
	mv lightzone-dependencies-* lightcrafts/dependencies
	# For whatever reason, the insane buildsystem wipes out lib and
	# copies dependencies to its place...
	cp lightcrafts/lib/* lightcrafts/dependencies
else
	mv lightzone-dependencies-*/* lightcrafts/lib/
fi

%build
. %{_sysconfdir}/profile.d/90java.sh

ant -f linux/build.xml jar -Dno-ivy=true -Dno-submodule=true

%install
install -dm 0755 "%buildroot/%{_libexecdir}/%{name}"
cp -pH lightcrafts/products/dcraw_lz "%buildroot/%{_libexecdir}/%{name}"
cp -pH lightcrafts/products/LightZone-forkd "%buildroot/%{_libexecdir}/%{name}"
cp -pH linux/products/*.so "%buildroot/%{_libexecdir}/%{name}"

install -dm 0755 "%buildroot/%{_datadir}/java/%{name}"
cp -pH linux/products/*.jar "%buildroot/%{_datadir}/java/%{name}"

# create icons and shortcuts
install -dm 0755 "%buildroot/%{_datadir}/applications"
install -m 644 linux/products/lightzone.desktop "%buildroot/%{_datadir}/applications/"
cp -pHR linux/icons "%buildroot/%{_datadir}/"

install -dm 755 %{buildroot}/%{_bindir}
install -m 755 linux/products/%{name} %{buildroot}/%{_bindir}

%files
%doc COPYING README.md linux/BUILD-Linux.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%dir %{_datadir}/java/%{name}
%{_datadir}/java/%{name}/*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
