import sys

current_version = sys.version_info

def version_comparation(version_to_compare, operation_to_compare="<="):
    code = """ current_version {0} version_compare""".format(operation_to_compare)

    return eval(code, {"current_version": current_version, "version_compare": version_to_compare})


if __name__ == "__main__":
    print(sys.version_info)