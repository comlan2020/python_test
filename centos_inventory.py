import os
import subprocess
import pkg_resources
import datetime

def list_installed_packages():
    # Fetch package information
    cmd = ['rpm', '-qa', '--queryformat', '%{NAME} %{VERSION} %{INSTALLTID:date}\n']
    packages = subprocess.check_output(cmd).decode('utf-8')
    return packages

def list_installed_python_libs():
    dists = pkg_resources.working_set
    package_details = []
    for dist in dists:
        package_info = f"{dist.project_name}=={dist.version}"
        try:
            filepath = os.path.dirname(os.path.dirname(dist.location))
            timestamp = os.path.getctime(filepath)
            install_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            package_info += f", Installed at: {install_date}"
        except Exception as e:
            package_info += ", Couldn't determine installation date."
        package_details.append(package_info)
    return package_details

def main():
    system_packages = list_installed_packages()
    python_packages = list_installed_python_libs()

    print("System Packages:\n")
    print(system_packages)

    print("\nPython Packages:\n")
    for package in python_packages:
        print(package)

if __name__ == "__main__":
    main()
