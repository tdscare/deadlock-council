using System.Reflection;
using System.Text;
using DeadworksManaged.Api;

namespace SandboxTester;

public partial class SandboxTester
{
	[Command("sbx_dump", Description = "Dump public members of an Api type to sbx_logs\\api_<Type>.txt")]
	public void CmdDump(Caller caller, string typeName) => Run(caller, "sbx_dump", typeName, () =>
	{
		var asm = typeof(CBaseEntity).Assembly;
		var t = asm.GetTypes().FirstOrDefault(x => x.Name.Equals(typeName, StringComparison.OrdinalIgnoreCase));
		if (t == null) { foreach (var a in AppDomain.CurrentDomain.GetAssemblies()) { t = a.GetTypes().FirstOrDefault(x => x.Name.Equals(typeName, StringComparison.OrdinalIgnoreCase)); if (t != null) break; } }
		if (t == null) { Reply(caller, "type not found"); return; }
		var sb = new StringBuilder();
		sb.AppendLine($"{t.FullName} : {t.BaseType?.FullName}");
		foreach (var m in t.GetMembers(BindingFlags.Public | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly))
		{
			if (m is MethodInfo mi && mi.IsSpecialName) continue;
			if (m is PropertyInfo pi) sb.AppendLine($"P {pi.PropertyType.Name} {pi.Name} {(pi.CanRead ? "get" : "")}{(pi.CanWrite ? " set" : "")}");
			else if (m is MethodInfo mm) sb.AppendLine($"M {mm.ReturnType.Name} {mm.Name}({string.Join(", ", mm.GetParameters().Select(p => p.ParameterType.Name + " " + p.Name))})");
			else if (m is FieldInfo fi) sb.AppendLine($"F {fi.FieldType.Name} {fi.Name}");
		}
		var b = t.BaseType;
		while (b != null && b != typeof(object)) { sb.AppendLine("base " + b.FullName); b = b.BaseType; }
		File.WriteAllText(Path.Combine(_dir, "api_" + t.Name + ".txt"), sb.ToString());
		Reply(caller, "dumped " + t.FullName);
	});
}
