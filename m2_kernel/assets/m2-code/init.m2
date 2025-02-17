saveStandardPrint = Thing#{Standard,Print}
saveTeXmacsPrint  = Thing#{TeXmacs, Print}
saveWebAppPrint   = Thing#{WebApp,  Print}

sentinelStandardPrint = x -> ( << "--VAL\n"; saveStandardPrint(x); << "--CLS\n"; )
sentinelTeXmacsPrint  = x -> ( << "--VAL\n"; saveTeXmacsPrint(x);  << "--CLS\n"; )
sentinelWebAppPrint   = x -> ( << "--VAL\n"; saveWebAppPrint(x);   << "--CLS\n"; )

Thing#{Standard,Print} = sentinelStandardPrint

noop = (trigger) -> (lineNumber -= 1;)

mode = (newmode) -> (
    Thing#{Standard, Print} = (
	if      newmode === Standard then sentinelStandardPrint
	else if newmode === TeXmacs  then sentinelTeXmacsPrint
	else if newmode === WebApp   then sentinelWebAppPrint
    );
    noop(mode);
)
