//Print functions referencing each given hex data address.
//@category EBoN
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceManager;
import ghidra.program.model.listing.Function;

public class FindRefs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        ReferenceManager rm = currentProgram.getReferenceManager();
        for (String a : args) {
            Address addr = toAddr(Long.parseLong(a.replaceFirst("(?i)^0x", ""), 16));
            println("=== refs to " + a + " ===");
            for (Reference r : rm.getReferencesTo(addr)) {
                Address from = r.getFromAddress();
                Function f = getFunctionContaining(from);
                println("  " + from + (f != null ? "  in " + f.getName() + " @ " + f.getEntryPoint() : "  (no func)"));
            }
        }
    }
}
