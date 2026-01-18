import metakernel

class ModeMagic(metakernel.Magic):
    modes = {
        "standard": "Standard",
        "webapp": "WebApp",
        "texmacs": "TeXmacs"
    }

    def line_mode(self, mode):
        """
        %mode MODE - switch top level mode

        Possible modes:
           webapp (html + mathjax) (default)
           texmacs (html + mathml)
           standard (plain text)
        """

        mode = mode.lower()
        if mode in self.modes:
            self.kernel.mode = mode
            self.kernel.do_execute_direct(
                f"changeJupyterMode {self.modes[mode]}")
        else:
            raise ValueError(f"expected one of {list(self.modes.keys())}")

def register_magics(kernel):
    kernel.register_magics(ModeMagic)
