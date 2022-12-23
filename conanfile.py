from conan import ConanFile
from conan.tools.files import replace_in_file
from conan.tools.scm import Git
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout

import os


class MinioCppConan(ConanFile):
    name = "minio-cpp"
    version = "0.1.1"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of MinioCpp here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    generators = ["cmake_find_package"]

    requires = "libcurl/7.86.0", "curlpp/0.8.1", "pugixml/1.13", "nlohmann_json/3.11.2", "openssl/3.0.7", "inih/56"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = Git(self, folder=self.source_folder)
        git.clone('https://github.com/minio/minio-cpp.git', self.source_folder)
        git.checkout(f'tags/v{self.version}')

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "unofficial-curlpp", "curlpp")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "unofficial::curlpp", "curlpp")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "OPENSSL_FOUND", "OpenSSL_FOUND")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "  list(APPEND requiredlibs pugixml)", "  list(APPEND requiredlibs pugixml::pugixml)")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "  list(APPEND requiredlibs inih)", "  list(APPEND requiredlibs inih::inih)")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "ENDIF(PUGIXML_FOUND)", "ENDIF(PUGIXML_FOUND)\nfind_package(inih REQUIRED)\n")
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["miniocpp"]
