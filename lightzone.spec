%define oname LightZone

Name:		lightzone
Version:	4.1.8
Release:	2
License:	BSD-3-Clause
Summary:	Open-source professional-level digital darkroom software
Url:		http://lightzoneproject.org/
Group:		Graphics
Source0:	https://github.com/ktgw0316/LightZone/archive/%{version}/%{oname}-%{version}.tar.gz
#Source100:	%{name}.rpmlintrc
BuildRequires:	ant
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	nasm
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:  gomp-devel
BuildRequires:	libtool
BuildRequires:	make
BuildRequires:	tidy
BuildRequires:	git
BuildRequires:	javahelp2
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	java-rpmbuild
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libtiff-4)

Requires:	java
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
%setup -qn %{oname}-%{version}

%build
%ant -f linux/build.xml jar

%install
install -dm 0755 "%buildroot/%{_libexecdir}/%{name}"
cp -pH lightcrafts/products/dcraw_lz "%buildroot/%{_libexecdir}/%{name}"
cp -pH lightcrafts/products/LightZone-forkd "%buildroot/%{_libexecdir}/%{name}"
cp -pH linux/products/*.so "%buildroot/%{_libexecdir}/%{name}"

install -dm 0755 "%buildroot/%{_javadir}/%{name}"
cp -pH linux/products/*.jar "%buildroot/%{_javadir}/%{name}"

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
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%define icondir %{_datadir}/icons/hicolor
%dir %{icondir}
%dir %{icondir}/256x256
%dir %{icondir}/256x256/apps
%dir %{icondir}/128x128
%dir %{icondir}/128x128/apps
%dir %{icondir}/64x64
%dir %{icondir}/64x64/apps
%dir %{icondir}/48x48
%dir %{icondir}/48x48/apps
%dir %{icondir}/32x32
%dir %{icondir}/32x32/apps
%dir %{icondir}/16x16
%dir %{icondir}/16x16/apps
%{icondir}/256x256/apps/%{name}.png
%{icondir}/128x128/apps/%{name}.png
%{icondir}/64x64/apps/%{name}.png
%{icondir}/48x48/apps/%{name}.png
%{icondir}/32x32/apps/%{name}.png
%{icondir}/16x16/apps/%{name}.png

