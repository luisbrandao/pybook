# Decompile specific functions to C (Ghidra headless post-script, Jython).
# @category Analysis
# Usage: ... -postScript DecompFuncs.py 0x41b6e1 0x429f74 ...
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

args = getScriptArgs()
targets = [int(a, 16) for a in args] if args else [0x41b6e1]

di = DecompInterface()
di.openProgram(currentProgram)
fm = currentProgram.getFunctionManager()
space = currentProgram.getAddressFactory().getDefaultAddressSpace()
mon = ConsoleTaskMonitor()

for a in targets:
    addr = space.getAddress(a)
    fn = fm.getFunctionContaining(addr)
    if fn is None:
        print("=== no function at 0x%x ===" % a)
        continue
    res = di.decompileFunction(fn, 180, mon)
    print("\n//================ %s @ %s (entry %s) ================"
          % (fn.getName(), addr, fn.getEntryPoint()))
    if res and res.decompileCompleted():
        print(res.getDecompiledFunction().getC())
    else:
        print("// decompile failed: %s" % (res.getErrorMessage() if res else "no result"))
