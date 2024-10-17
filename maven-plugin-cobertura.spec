Name:       maven-plugin-cobertura
Version:    2.4
Release:    4
Summary:    Plugin providing the features of Cobertura within Maven

Group:      Development/Java
License:    ASL 2.0 and GPLv2 and GPLv2+
URL:        https://mojo.codehaus.org/cobertura-maven-plugin/
Source0:    http://repo2.maven.org/maven2/org/codehaus/mojo/cobertura-maven-plugin/2.4/cobertura-maven-plugin-%{version}-source-release.zip
# Fix compile with our doxia.
Patch0:     maven-plugin-cobertura-2.3-SiteRenderer.patch
BuildArch:  noarch

BuildRequires:  maven2
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  maven-plugin-cobertura
BuildRequires:  gnu.getopt >= 0:1.0.13
BuildRequires:  cobertura
BuildRequires:  mojo-parent

Requires:       maven2
Requires:       cobertura
Requires:       mojo-parent
Requires(post): jpackage-utils
Requires(postun):  jpackage-utils

%description
This plugin provides the features of Cobertura within the Maven 2 environment.
The report generated by this plugin is the result of executing the Cobertura
tool against your compiled classes to help you determine how well the unit
testing efforts have been, and can then be used to identify which parts
of your Java program are lacking test coverage.

%package	javadoc
Summary:    Javadoc for %{name}
Group:      Development/Java
Requires:   %{name} = %{version}-%{release}
Requires:   jpackage-utils

%description	javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n cobertura-maven-plugin-%{version}
%patch0 -p1

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp -Dmaven.test.skip=true -Dmaven.repo.local=$MAVEN_REPO_LOCAL package javadoc:javadoc


%install
rm -rf $RPM_BUILD_ROOT

# jar
ln -sf $(build-classpath gnu.getopt)
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 target/cobertura-maven-plugin-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/maven-plugin-cobertura.jar

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -p -m 644 pom.xml \
  $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP-maven-plugin-cobertura.pom
%add_to_maven_depmap org.codehaus.mojo cobertura-maven-plugin %{version} JPP maven-plugin-cobertura

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%{_mavenpomdir}/JPP-%{name}*.pom
%config(noreplace) %{_mavendepmapfragdir}
%{_javadir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}


