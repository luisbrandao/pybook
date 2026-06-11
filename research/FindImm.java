//Find functions whose instructions use any of the given scalar immediates.
//@category EBoN
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.scalar.Scalar;
import ghidra.program.model.lang.OperandType;
import java.util.HashSet;
import java.util.HashMap;
import java.util.Map;

public class FindImm extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        HashSet<Long> targets = new HashSet<>();
        for (String a : args) targets.add(Long.parseLong(a.replaceFirst("(?i)^0x", ""), 16));
        Map<String,Integer> hits = new HashMap<>();
        InstructionIterator it = currentProgram.getListing().getInstructions(true);
        while (it.hasNext()) {
            Instruction ins = it.next();
            for (int op = 0; op < ins.getNumOperands(); op++) {
                Object[] objs = ins.getOpObjects(op);
                for (Object o : objs) {
                    if (o instanceof Scalar) {
                        long v = ((Scalar)o).getUnsignedValue();
                        if (targets.contains(v)) {
                            Function f = getFunctionContaining(ins.getAddress());
                            String key = f != null ? f.getName()+" @ "+f.getEntryPoint() : "(none) @ "+ins.getAddress();
                            hits.merge(key, 1, Integer::sum);
                        }
                    }
                }
            }
        }
        for (Map.Entry<String,Integer> e : hits.entrySet())
            println("HIT " + e.getValue() + "x  " + e.getKey());
    }
}
