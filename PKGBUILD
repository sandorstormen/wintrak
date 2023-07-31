# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# The following guidelines are specific to BZR, GIT, HG and SVN packages.
# Other VCS sources are not natively supported by makepkg yet.

# Maintainer: Sandor Berglund <sandor.berglund@gmail.com>
pkgname=wintrak-git # '-bzr', '-git', '-hg' or '-svn'
pkgver="0.0.1"
pkgrel=1
_desc="The real time tracker"
pkgdesc="The real time tracker"
arch=('any')
url="git+https://github.com/sandorstormen/wintrak.git"
license=('GPL')
groups=()
depends=("python" "python-xlib")
makedepends=('git')
provides=("${pkgname%-git}")
conflicts=("${pkgname%-git}")
# replaces=()
# backup=()
# options=()
# install=
source=('git+https://github.com/sandorstormen/wintrak.git')
noextract=()
md5sums=('5f4fcfdec864255d8d9662900e0fa4c9' '1f4f72c6544f68045faa4b2238005a0d')

# Please refer to the 'USING VCS SOURCES' section of the PKGBUILD man page for
# a description of each element in the source array.

pkgver() {
	cd "$srcdir/${pkgname%-git}"

# The examples below are not absolute and need to be adapted to each repo. The
# primary goal is to generate version numbers that will increase according to
# pacman's version comparisons with later commits to the repo. The format
# VERSION='VER_NUM.rREV_NUM.HASH', or a relevant subset in case VER_NUM or HASH
# are not available, is recommended.

# Git, tags available
	printf "%s" "$(git describe --long | sed 's/\([^-]*-\)g/r\1/;s/-/./g')"

# Git, no tags available
	printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

# prepare() {
# 	cd "$srcdir/${pkgname%-VCS}"
# 	patch -p1 -i "$srcdir/${pkgname%-VCS}.patch"
# }

build() {
	cd "$srcdir/${pkgname%-VCS}"
	# ./autogen.sh
	# ./configure --prefix=/usr
	make
}

check() {
	cd "$srcdir/${pkgname%-VCS}"
	make -k check
}

package() {
	cd "$srcdir/${pkgname%-VCS}"
	make DESTDIR="$pkgdir/" install
}