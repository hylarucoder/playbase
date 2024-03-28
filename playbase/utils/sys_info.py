import os


def get_current_os():
    name = os.name
    if "posix" in name:
        return "Mac OS"
    elif "linux" in name:
        return "Linux"
    else:
        return "Windows"
