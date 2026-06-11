//Decompile the functions containing the given hex addresses and write each to /tmp/ebon_<addr>.c
//@category EBoN
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import java.io.FileWriter;
import java.io.PrintWriter;

public class DecompFuncs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            println("usage: DecompFuncs.java <hexaddr> [hexaddr ...]");
            return;
        }
        DecompInterface ifc = new DecompInterface();
        ifc.openProgram(currentProgram);
        try {
            for (String a : args) {
                Address addr = toAddr(Long.parseLong(a.replaceFirst("(?i)^0x", ""), 16));
                Function f = getFunctionContaining(addr);
                if (f == null) {
                    println("NO FUNCTION at " + a);
                    continue;
                }
                DecompileResults res = ifc.decompileFunction(f, 180, monitor);
                String out = "/tmp/ebon_" + f.getEntryPoint() + ".c";
                try (PrintWriter pw = new PrintWriter(new FileWriter(out))) {
                    if (res.decompileCompleted()) {
                        pw.println("// " + f.getName() + " @ " + f.getEntryPoint());
                        pw.println(res.getDecompiledFunction().getC());
                        println("WROTE " + out);
                    }
                    else {
                        pw.println("// decompile FAILED: " + res.getErrorMessage());
                        println("FAILED " + a + ": " + res.getErrorMessage());
                    }
                }
            }
        }
        finally {
            ifc.dispose();
        }
    }
}
