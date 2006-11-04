%define		_rel	0.1
Summary:	Aethera - Email and PIM application
Name:		aethera
Version:	1.2.1
Release:	050331.%{_rel}
License:	GPL
Group:		X11/Applications
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	f3efd064b5e9884bd7adf49bf763e213
URL:		http://www.thekompany.com/projects/aethera/
#BuildRequires:	korelib
BuildRequires:	qt-devel
#Requires: thekompany-support
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aethera is a pim application, i.e. it handles all kinds of personal
information: email, contacts, notes, tasks, todos, journals.

%prep
%setup -q

%build
# Use the new libraries in building process
export LD_LIBRARY_PATH=$dir/lib:$LD_LIBRARY_PATH
dir=$(pwd)

# Compile tkcBase
cd tkcbase
echo > defines.pri
echo "TKCBASE_LIB="$dir/lib >> defines.pri
echo "TKCBASE_INCLUDE="$dir/tkcbase >> defines.pri
echo "CONFIG += release thread" >> defines.pri
./qmake.sh
%{__make}
./qmake.sh
%{__make}

# Compile tkcSSL
cd ../tkcssl
echo > defines.pri
echo "TKCSSL_LIB="$dir/lib >> defines.pri
echo "TKCSSL_INCLUDE="$dir/include/tkcssl >> defines.pri
echo "INCLUDEPATH += "$dir/include/tkcbase >> defines.pri
echo "DEPENDPATH += "$dir/include/tkcbase >> defines.pri
echo "CONFIG += release thread" >> defines.pri
./qmake.sh
%{__make}
./qmake.sh
%{__make}

# Compile webdav
cd ../webdav
echo > defines.pri
echo "WEBDAV_LIB="$dir/lib/ >> defines.pri
echo "WEBDAV_INCLUDE="$dir/include/tkcbase >> defines.pri
echo "CONFIG += release thread" >> defines.pri
./qmake.sh
%{__make}
./qmake.sh
%{__make}

# Compile Aethera
cd ../aethera
echo > defines.pri
echo "AETHERA_DIR="$dir/lib/theKompany/Aethera >> defines.pri
echo "AETHERA_BIN="$dir/bin >> defines.pri
echo "AETHERA_LIB="$dir/lib/ >> defines.pri
echo "AETHERA_INCLUDE="$dir/include/aethera/ >> defines.pri
echo "AETHERA_INCLUDES="$dir/include/aethera/ >> defines.pri
echo "TINO_LIB="$dir/lib/lib >> defines.pri
echo "TINO_INCLUDE="$dir/include/tino >> defines.pri
echo "INCLUDEPATH += "$dir/include >> defines.pri
echo "INCLUDEPATH += "$dir/include/tkcbase >> defines.pri
echo "DEPENDPATH += "$dir/include/tkcbase >> defines.pri
echo "INCLUDEPATH += "$dir/include/tkcssl >> defines.pri
echo "DEPENDPATH += "$dir/include/tkcssl >> defines.pri

echo "CONFIG += qt warn_on release thread" >> defines.pri

./qmake.sh
%{__make}
./qmake.sh
%{__make}

# Compile KOrganizer plugin
cd ../koplugin

echo > defines.pri
echo "AETHERA_DIR="$dir/lib >> defines.pri

echo "INCLUDEPATH += "$dir/include >> defines.pri
echo "INCLUDEPATH += "$dir/include/tkcbase >> defines.pri
echo "DEPENDPATH += "$dir/include/tkcbase >> defines.pri
echo "INCLUDEPATH += "$dir/include/tkcssl >> defines.pri
echo "DEPENDPATH += "$dir/include/tkcssl >> defines.pri
echo "INCLUDEPATH += "$dir/include/aethera >> defines.pri
echo "DEPENDPATH += "$dir/include/aethera >> defines.pri
echo "INCLUDEPATH += "$dir/include/aethera/libs/plugins/kommailplugin >> defines.pri
echo "DEPENDPATH += "$dir/include/aethera/libs/plugins/kommailplugin >> defines.pri
echo "INCLUDEPATH += "$dir/include/aethera/libs/plugins/komcontactsplugin >> defines.pri
echo "DEPENDPATH += "$dir/include/aethera/libs/plugins/komcontactsplugin >> defines.pri
echo "INCLUDEPATH += "$dir/include/tino >> defines.pri
echo "DEPENDPATH += "$dir/include/tino >> defines.pri

echo "CONFIG += qt warn_on release thread" >> defines.pri
echo "DEFINES += AETHERA_KOLAB" >> defines.pri

./qmake.sh
%{__make}
./qmake.sh
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C tkcbase install
%{__make} -C tkcssl install
%{__make} -C webdav install
%{__make} -C aethera install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
