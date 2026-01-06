import metakernel

class ModeMagic(metakernel.Magic):
    modes = {
        "default": "Standard",
        "webapp": "WebApp",
        "texmacs": "TeXmacs"
    }

    def line_mode(self, mode):
        if mode in self.modes:
            self.kernel.mode = mode
            self.kernel.do_execute(f"mode {self.modes[mode]}")
        else:
            raise ValueError(f"expected one of {list(self.modes.keys())}")

def register_magics(kernel):
    kernel.register_magics(ModeMagic)
