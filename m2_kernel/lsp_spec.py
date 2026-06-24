import shutil

def load(mgr):
    cmd = shutil.which("M2-language-server")
    return {
        "macaulay2": {
            "version": 2,
            "argv": [cmd] if cmd else [],
            "languages": ["macaulay2"],
            "mime_types": ["text/x-macaulay2"],
            "display_name": "Macaulay2",
        }
    }
