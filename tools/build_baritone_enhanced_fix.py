from pathlib import Path

root = Path('baritone-enhanced')

auto = root / 'src/main/java/baritone/command/defaults/AutoCommand.java'
s = auto.read_text()
s = s.replace(
    '    public Stream<String> tabComplete(String label, IArgConsumer args) {\n',
    '    public Stream<String> tabComplete(String label, IArgConsumer args) throws CommandException {\n',
    1
)
auto.write_text(s)

renderer = root / 'src/main/java/baritone/utils/PathRenderer.java'
s = renderer.read_text()
anchor = '    private static void drawGoal(PoseStack stack, IPlayerContext ctx, Goal goal, Color color) {\n'
replacement = '''    public static void drawGoal(PoseStack stack, IPlayerContext ctx, Goal goal, float partialTicks, Color color) {\n        drawGoal(stack, ctx, goal, color);\n    }\n\n    private static void drawGoal(PoseStack stack, IPlayerContext ctx, Goal goal, Color color) {\n'''
if anchor not in s:
    raise SystemExit('PathRenderer drawGoal anchor missing')
s = s.replace(anchor, replacement, 1)
renderer.write_text(s)

print('Compatibility fixes applied.')
