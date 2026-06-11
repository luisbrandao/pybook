//Force-create a function at each given address (clearing any overlap) and decompile it.
//@category EBoN
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.symbol.SourceType;
import ghidra.app.cmd.function.CreateFunctionCmd;
import java.io.FileWriter;
import java.io.PrintWriter;

public class DecompAt extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        FunctionManager fm = currentProgram.getFunctionManager();
        for (String a : args) {
            Address addr = toAddr(Long.parseLong(a.replaceFirst("(?i)^0x", ""), 16));
            Function f = fm.getFunctionContaining(addr);
            if (f != null && !f.getEntryPoint().equals(addr)) {
                println("Clearing merged function " + f.getEntryPoint() + " to expose " + a);
                fm.removeFunction(f.getEntryPoint());
            }
            f = fm.getFunctionAt(addr);
            if (f == null) {
                CreateFunctionCmd cmd = new CreateFunctionCmd(addr);
                cmd.applyTo(currentProgram, monitor);
                f = fm.getFunctionAt(addr);
            }
            if (f == null) { println("FAILED to create function at " + a); continue; }

            DecompInterface ifc = new DecompInterface();
            ifc.openProgram(currentProgram);
            DecompileResults res = ifc.decompileFunction(f, 180, monitor);
            String out = "/tmp/ebonW_" + f.getEntryPoint() + ".c";
            try (PrintWriter pw = new PrintWriter(new FileWriter(out))) {
                if (res.decompileCompleted()) {
                    pw.println("// " + f.getName() + " @ " + f.getEntryPoint());
                    pw.println(res.getDecompiledFunction().getC());
                    println("WROTE " + out);
                } else {
                    pw.println("// FAILED: " + res.getErrorMessage());
                    println("FAILED " + a + ": " + res.getErrorMessage());
                }
            }
            ifc.dispose();
        }
    }
}
