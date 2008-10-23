Summary:	A CGI search frontend and indexers built on Xapian
Name:		xapian-omega
Version:	1.0.4
Release:	0.1
License:	GPL
Group:		Applications/Databases
URL:		http://www.xapian.org/
Source0:	http://www.oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-gcc43.patch
# Source0-md5:	f4c84cc69cad731677a430c4e3e9a16f
BuildRequires:	xapian-core-devel = %{version}
Requires:	xapian-core-libs = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cgibindir	%{_prefix}/lib/cgi-bin

%description
Omega is a CGI application which uses the Xapian Information Retrieval
library to index and search collections of documents.

%prep
%setup -q
%patch

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT docdatadir=%{_docdir}/%{name}/

# CGI application
install -d $RPM_BUILD_ROOT%{cgibindir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/xapian-omega/bin/omega $RPM_BUILD_ROOT%{cgibindir}/%{name}

# Create the data directory
install -d $RPM_BUILD_ROOT/var/lib/omega/data
install -d $RPM_BUILD_ROOT/var/lib/omega/cdb
install -d $RPM_BUILD_ROOT/var/log/omega

# Default templates
install -d $RPM_BUILD_ROOT/var/lib/omega
cp -a templates $RPM_BUILD_ROOT/var/lib/omega/templates

# Configuration file
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a omega.conf $RPM_BUILD_ROOT%{_sysconfdir}/omega.conf

# Move the scripts to the right place
mv $RPM_BUILD_ROOT%{_datadir}/omega $RPM_BUILD_ROOT%{_datadir}/%{name}

# Images
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
cp -a images $RPM_BUILD_ROOT%{_datadir}/%{name}/icons

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%doc docs/*.txt
%config(noreplace) %{_sysconfdir}/omega.conf
%attr(755,root,root) %{_bindir}/dbi2omega
%attr(755,root,root) %{_bindir}/omindex
%attr(755,root,root) %{_bindir}/scriptindex
%attr(755,root,root) %{_bindir}/htdig2omega
%attr(755,root,root) %{_bindir}/mbox2omega
%attr(755,root,root) %{cgibindir}/%{name}
%{_mandir}/man1/omindex.1*
%{_mandir}/man1/scriptindex.1*
%{_datadir}/%{name}
/var/lib/omega
/var/log/omega
