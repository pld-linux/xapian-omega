%include	/usr/lib/rpm/macros.perl
Summary:	A CGI search frontend and indexers built on Xapian
Summary(pl.UTF-8):	Frontend wyszukiwarki CGI oraz programy indeksujące oparte na Xapianie
Name:		xapian-omega
Version:	1.2.18
Release:	0.1
License:	GPL v2+
Group:		Applications/Databases
Source0:	http://oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7eed3c1e9e6acb703d6587ed9a038265
URL:		http://www.xapian.org/
BuildRequires:	help2man
BuildRequires:	libmagic-devel
BuildRequires:	libstdc++-devel >= 5:3.1
BuildRequires:	pcre-devel
BuildRequires:	perl-base
BuildRequires:	rpm-perlprov
BuildRequires:	xapian-core-devel = %{version}
Requires:	xapian-core-libs = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cgibindir	%{_prefix}/lib/cgi-bin

%description
Omega is a CGI application which uses the Xapian Information Retrieval
library to index and search collections of documents.

%description -l pl.UTF-8
Omega to aplikacja CGI wykorzystująca bibliotekę uzyskiwania
informacji Xapian w celu indeksowania i przeszukiwania zbioru
dokumentów.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdatadir=%{_docdir}/%{name}

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

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO docs/*.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/omega.conf
%attr(755,root,root) %{_bindir}/dbi2omega
%attr(755,root,root) %{_bindir}/omindex
%attr(755,root,root) %{_bindir}/scriptindex
%attr(755,root,root) %{_bindir}/htdig2omega
%attr(755,root,root) %{_bindir}/mbox2omega
%attr(755,root,root) %{cgibindir}/%{name}
%dir %{_libdir}/xapian-omega
%dir %{_libdir}/xapian-omega/bin
%attr(755,root,root) %{_libdir}/xapian-omega/bin/outlookmsg2html
%{_mandir}/man1/omindex.1*
%{_mandir}/man1/scriptindex.1*
%{_datadir}/%{name}
/var/lib/omega
/var/log/omega
