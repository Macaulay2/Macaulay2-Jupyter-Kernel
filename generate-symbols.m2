needsPackage "Style"

generateGrammar("m2_kernel/symbols.py", x -> demark(",\n    ", format \ x))
