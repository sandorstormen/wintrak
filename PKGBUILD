# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# The following guidelines are specific to BZR, GIT, HG and SVN packages.
# Other VCS sources are not natively supported by makepkg yet.

# Maintainer: Sandor Berglund <sandor.berglund@gmail.com>
pkgname=wintrak-git # '-bzr', '-git', '-hg' or '-svn'
pkgver=r14.ea7a604
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
md5sums=('SKIP')

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

prepare() {
	cd "${pkgname%-git}"
	git submodule init
	git -c protocol.file.allow=always submodule update
}

build() {
	cd "${pkgname%-git}/gui"
	
	yarn install
	yarn add --dev @electron-forge/cli
	npx electron-forge import

	yarn make
}

# check() {
# 	cd wintrak
# 	# make -k check
# }

package() {
	cd "${pkgname%-git}"
	# cd "$srcdir"
	install -dm755 "$pkgdir/usr/lib/wintrak"
	install -dm755 "./backend/wintrak" "$pkgdir/usr/lib/wintrak"
	install -m644 "./backend/wintrak.service" "$pkgdir/etc/systemd/user"
}
