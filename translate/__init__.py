import argostranslate.package
import argostranslate.translate


def init(from_code: str, to_code: str):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    ))
    argostranslate.package.install_from_path(package_to_install.download())

def translate(text: str, from_code: str, to_code: str):
    return argostranslate.translate.translate(text, from_code, to_code)
