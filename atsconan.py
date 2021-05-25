from conans import ConanFile, AutoToolsBuildEnvironment
import os

class ATSConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "Makefile*"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": False}

    def build(self):
        # build using Make and add the ATSFLAGS variable with all the deps -IATS includes
        atools = AutoToolsBuildEnvironment(self)
        var = atools.vars
        var['ATSFLAGS'] = self.get_ats_includes()
        atools.make(vars=var)

    def package(self):
        # by default, package up the src directory and put the libs in a lib directory
        self.copy("*.hats", dst="src", src="src")
        self.copy("*.dats", dst="src", src="src")
        self.copy("*.sats", dst="src", src="src")
        self.copy("*.cats", dst="src", src="src")
        if self.options.shared:
            self.copy("*.so", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        # default to exporting the src dir as an ats_include
        self.user_info.ats_includes = [ os.path.join(self.package_folder, "src")]

    def get_ats_includes(self):
        """
        Loop through all this package's dependencies and concat a list of ats_includes
        """
        includes = []
        for pkg_name in self.deps_user_info:
            incs = self.deps_user_info[pkg_name].vars.get("ats_includes")
            if not incs:
                continue
            # these are string representations of arrays, so chop off the '[' and ']' and split on commas
            incs = incs[1:-1].split(',')
            # create a list of -IATS ...
            includes.append(" ".join([f"-IATS {i[1:-1]}" for i in incs]))
        return " ".join(includes)