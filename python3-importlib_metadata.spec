#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Read metadata from Python packages
Summary(pl.UTF-8):	Odczyt metadanych z pakietów Pythona
Name:		python3-importlib_metadata
Version:	4.12.0
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/importlib-metadata/
Source0:	https://files.pythonhosted.org/packages/source/i/importlib-metadata/importlib_metadata-%{version}.tar.gz
# Source0-md5:	cfcf29185e13439c76d09c94bc8d81f4
URL:		https://pypi.org/project/importlib-metadata/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:30.3
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
#BuildRequires:	python3-flufl.flake8
%if "%{_ver_lt '%{py3_ver}' '3.9'}" == "1"
BuildRequires:	python3-importlib_resources >= 1.3
%endif
BuildRequires:	python3-packaging
BuildRequires:	python3-pyfakefs
BuildRequires:	python3-pytest >= 6
#BuildRequires:	python3-pytest-black >= 0.3.7
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-enabler >= 1.3
#BuildRequires:	python3-pytest-flake8
#BuildRequires:	python3-pytest-mypy >= 0.9.1
#BuildRequires:	python3-pytest-perf >= 0.9.2
%if "%{_ver_lt '%{py3_ver}' '3.8'}" == "1"
BuildRequires:	python3-typing_extensions >= 3.6.4
%endif
BuildRequires:	python3-zipp >= 0.5
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.749
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-jaraco.packaging >= 9
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
importlib_metadata is a library to access the metadata for a Python
package. New features are merged in later versions of CPython.

%description -l pl.UTF-8
importlib_metadata to biblioteka służąca do dostępu do metadanych
pakietów Pythona. Nowa funkcjonalność jest później włączana do
CPythona.

%package apidocs
Summary:	API documentation for Python importlib_metadata module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona importlib_metadata
Group:		Documentation

%description apidocs
API documentation for Python importlib_metadata module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona importlib_metadata.

%prep
%setup -q -n importlib_metadata-%{version}

# stub for setuptools
cat >setup.py <<EOF
from setuptools import setup
setup()
EOF

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/importlib_metadata
%{py3_sitescriptdir}/importlib_metadata-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
