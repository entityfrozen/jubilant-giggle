from pathlib import Path
import re

root = Path('baritone-enhanced')

def replace(path, old, new, count=-1):
    p = root / path
    s = p.read_text()
    if old not in s:
        raise SystemExit(f'Missing expected text in {path}: {old[:120]!r}')
    p.write_text(s.replace(old, new, count))

replace('gradle.properties', 'mod_version=1.9.5', 'mod_version=1.9.5-enhanced.1')
replace('gradle.properties', 'archives_base_name=baritone', 'archives_base_name=baritone-enhanced')
replace('fabric/src/main/resources/fabric.mod.json', '"name": "Baritone"', '"name": "Baritone Enhanced"')
replace('fabric/src/main/resources/fabric.mod.json', '"description": "Google Maps for Blockgame"', '"description": "Baritone with smoother movement, clean visuals, continuous mining, auto-eat, and combat automation"')
replace('fabric/src/main/resources/fabric.mod.json', '"minecraft": ">=1.21.11"', '"minecraft": ">=1.21.11 <1.22"')

settings = root / 'src/api/java/baritone/api/Settings.java'
s = settings.read_text()
reps = {
    'public final Setting<Boolean> allowInventory = new Setting<>(false);': 'public final Setting<Boolean> allowInventory = new Setting<>(true);',
    'public final Setting<Double> randomLooking113 = new Setting<>(2d);': 'public final Setting<Double> randomLooking113 = new Setting<>(0d);',
    'public final Setting<Integer> blockBreakSpeed = new Setting<>(6);': 'public final Setting<Integer> blockBreakSpeed = new Setting<>(1);',
    'public final Setting<Double> randomLooking = new Setting<>(0.01d);': 'public final Setting<Double> randomLooking = new Setting<>(0d);',
    'public final Setting<Boolean> renderPathAsLine = new Setting<>(false);': 'public final Setting<Boolean> renderPathAsLine = new Setting<>(true);',
    'public final Setting<Boolean> renderGoalAnimated = new Setting<>(true);': 'public final Setting<Boolean> renderGoalAnimated = new Setting<>(false);',
    'public final Setting<Boolean> renderSelectionBoxes = new Setting<>(true);': 'public final Setting<Boolean> renderSelectionBoxes = new Setting<>(false);',
    'public final Setting<Boolean> renderGoalIgnoreDepth = new Setting<>(true);': 'public final Setting<Boolean> renderGoalIgnoreDepth = new Setting<>(false);',
    'public final Setting<Boolean> renderSelectionBoxesIgnoreDepth = new Setting<>(true);': 'public final Setting<Boolean> renderSelectionBoxesIgnoreDepth = new Setting<>(false);',
    'public final Setting<Boolean> renderPathIgnoreDepth = new Setting<>(true);': 'public final Setting<Boolean> renderPathIgnoreDepth = new Setting<>(false);',
    'public final Setting<Float> pathRenderLineWidthPixels = new Setting<>(5F);': 'public final Setting<Float> pathRenderLineWidthPixels = new Setting<>(1.75F);',
    'public final Setting<Float> goalRenderLineWidthPixels = new Setting<>(3F);': 'public final Setting<Float> goalRenderLineWidthPixels = new Setting<>(1.75F);',
    'public final Setting<Boolean> fadePath = new Setting<>(false);': 'public final Setting<Boolean> fadePath = new Setting<>(true);',
    'public final Setting<Boolean> freeLook = new Setting<>(true);': 'public final Setting<Boolean> freeLook = new Setting<>(false);',
    'public final Setting<Boolean> smoothLook = new Setting<>(false);': 'public final Setting<Boolean> smoothLook = new Setting<>(true);',
    'public final Setting<Integer> smoothLookTicks = new Setting<>(5);': 'public final Setting<Integer> smoothLookTicks = new Setting<>(3);',
    'public final Setting<Color> colorCurrentPath = new Setting<>(Color.RED);': 'public final Setting<Color> colorCurrentPath = new Setting<>(new Color(139, 111, 232));',
    'public final Setting<Color> colorNextPath = new Setting<>(Color.MAGENTA);': 'public final Setting<Color> colorNextPath = new Setting<>(new Color(191, 168, 255));',
    'public final Setting<Color> colorBestPathSoFar = new Setting<>(Color.BLUE);': 'public final Setting<Color> colorBestPathSoFar = new Setting<>(new Color(116, 166, 255));',
    'public final Setting<Color> colorMostRecentConsidered = new Setting<>(Color.CYAN);': 'public final Setting<Color> colorMostRecentConsidered = new Setting<>(new Color(151, 226, 255));',
    'public final Setting<Color> colorGoalBox = new Setting<>(Color.GREEN);': 'public final Setting<Color> colorGoalBox = new Setting<>(new Color(255, 157, 202));',
}
for a, b in reps.items():
    if a not in s:
        raise SystemExit(f'Missing Settings replacement: {a}')
    s = s.replace(a, b)

anchor = '    public final Setting<Integer> smoothLookTicks = new Setting<>(3);\n'
extra = '''    public final Setting<Integer> smoothLookTicks = new Setting<>(3);\n\n    public final Setting<Boolean> continuousMining = new Setting<>(true);\n    public final Setting<Boolean> enhancedVisuals = new Setting<>(true);\n    public final Setting<Boolean> enhancedPathGlow = new Setting<>(true);\n    public final Setting<Boolean> enhancedPathMarkers = new Setting<>(true);\n    public final Setting<Float> enhancedRotationEase = new Setting<>(0.42F);\n    public final Setting<Float> enhancedMaxYawStep = new Setting<>(13.0F);\n    public final Setting<Float> enhancedMaxPitchStep = new Setting<>(10.0F);\n    public final Setting<Boolean> smoothMovementInput = new Setting<>(true);\n    public final Setting<Float> movementInputEase = new Setting<>(0.82F);\n    public final Setting<Boolean> autoEat = new Setting<>(true);\n    public final Setting<Integer> autoEatHunger = new Setting<>(14);\n    public final Setting<Integer> autoEatStopHunger = new Setting<>(19);\n    public final Setting<Boolean> autoFight = new Setting<>(false);\n    public final Setting<Boolean> autoFightMobs = new Setting<>(true);\n    public final Setting<Boolean> autoFightPlayers = new Setting<>(false);\n    public final Setting<Boolean> autoFightChase = new Setting<>(true);\n    public final Setting<Boolean> autoFightAutoWeapon = new Setting<>(true);\n    public final Setting<Double> autoFightSearchRange = new Setting<>(12.0D);\n    public final Setting<Double> autoFightAttackRange = new Setting<>(3.15D);\n'''
if anchor not in s:
    raise SystemExit('smoothLookTicks anchor missing')
s = s.replace(anchor, extra, 1)
settings.write_text(s)

look = root / 'src/main/java/baritone/behavior/LookBehavior.java'
s = look.read_text()
old = '''                    } else if (ctx.player().isFallFlying() ? Baritone.settings().elytraSmoothLook.value : Baritone.settings().smoothLook.value) {\n                        ctx.player().setYRot((float) this.smoothYawBuffer.stream().mapToDouble(d -> d).average().orElse(this.prevRotation.getYaw()));\n                        if (ctx.player().isFallFlying()) {\n                            ctx.player().setXRot((float) this.smoothPitchBuffer.stream().mapToDouble(d -> d).average().orElse(this.prevRotation.getPitch()));\n                        }\n                    }'''
new = '''                    } else if (ctx.player().isFallFlying() ? Baritone.settings().elytraSmoothLook.value : Baritone.settings().smoothLook.value) {\n                        final Settings settings = Baritone.settings();\n                        ctx.player().setYRot(smoothAxis(this.prevRotation.getYaw(), this.target.rotation.getYaw(), settings.enhancedMaxYawStep.value, settings.enhancedRotationEase.value, true));\n                        ctx.player().setXRot(smoothAxis(this.prevRotation.getPitch(), this.target.rotation.getPitch(), settings.enhancedMaxPitchStep.value, settings.enhancedRotationEase.value, false));\n                    }'''
if old not in s:
    raise SystemExit('LookBehavior smoothing block missing')
s = s.replace(old, new, 1)
pig = '    public void pig() {\n'
helper = '''    private static float smoothAxis(float current, float target, float maxStep, float ease, boolean wrap) {\n        float delta = wrap ? wrapDegrees(target - current) : target - current;\n        if (Math.abs(delta) < 0.025F) {\n            return wrap ? wrapDegrees(target) : clampPitch(target);\n        }\n        float safeEase = Math.max(0.05F, Math.min(1.0F, ease));\n        float safeMax = Math.max(0.25F, maxStep);\n        float step = Math.max(-safeMax, Math.min(safeMax, delta * safeEase));\n        if (Math.abs(step) < 0.10F) {\n            step = Math.copySign(Math.min(Math.abs(delta), 0.10F), delta);\n        }\n        float result = current + step;\n        return wrap ? wrapDegrees(result) : clampPitch(result);\n    }\n\n    private static float wrapDegrees(float value) {\n        value %= 360.0F;\n        if (value >= 180.0F) value -= 360.0F;\n        if (value < -180.0F) value += 360.0F;\n        return value;\n    }\n\n    private static float clampPitch(float value) {\n        return Math.max(-90.0F, Math.min(90.0F, value));\n    }\n\n    public void pig() {\n'''
if pig not in s:
    raise SystemExit('LookBehavior pig anchor missing')
s = s.replace(pig, helper, 1)
look.write_text(s)

movement = root / 'src/main/java/baritone/utils/PlayerMovementInput.java'
s = movement.read_text()
s = s.replace('package baritone.utils;\n\n', 'package baritone.utils;\n\nimport baritone.Baritone;\n')
s = s.replace('    private final InputOverrideHandler handler;\n', '    private final InputOverrideHandler handler;\n    private float smoothX;\n    private float smoothY;\n')
old = '''        this.moveVector = new Vec2(\n                toAxis(this.keyPresses.left(), this.keyPresses.right()),\n                toAxis(this.keyPresses.forward(), this.keyPresses.backward())\n        );'''
new = '''        float targetX = toAxis(this.keyPresses.left(), this.keyPresses.right());\n        float targetY = toAxis(this.keyPresses.forward(), this.keyPresses.backward());\n        if (Baritone.settings().smoothMovementInput.value) {\n            float ease = Math.max(0.1F, Math.min(1.0F, Baritone.settings().movementInputEase.value));\n            smoothX = approach(smoothX, targetX, ease);\n            smoothY = approach(smoothY, targetY, ease);\n        } else {\n            smoothX = targetX;\n            smoothY = targetY;\n        }\n        this.moveVector = new Vec2(smoothX, smoothY);'''
if old not in s:
    raise SystemExit('PlayerMovementInput vector block missing')
s = s.replace(old, new, 1)
anchor = '    private static float toAxis(boolean positive, boolean negative) {\n'
helper = '''    private static float approach(float current, float target, float ease) {\n        float value = current + (target - current) * ease;\n        if (Math.abs(target - value) < 0.02F) return target;\n        return value;\n    }\n\n    private static float toAxis(boolean positive, boolean negative) {\n'''
s = s.replace(anchor, helper, 1)
movement.write_text(s)

break_helper = root / 'src/main/java/baritone/utils/BlockBreakHelper.java'
s = break_helper.read_text()
old = '                    breakDelayTimer = BaritoneAPI.getSettings().blockBreakSpeed.value - BASE_BREAK_DELAY;'
new = '                    breakDelayTimer = BaritoneAPI.getSettings().continuousMining.value ? 0 : Math.max(0, BaritoneAPI.getSettings().blockBreakSpeed.value - BASE_BREAK_DELAY);'
if old not in s:
    raise SystemExit('BlockBreakHelper delay anchor missing')
s = s.replace(old, new, 1)
break_helper.write_text(s)

renderer = r'''/*
 * This file is part of Baritone and is distributed under LGPL-3.0-or-later.
 */
package baritone.utils;

import baritone.api.BaritoneAPI;
import baritone.api.event.events.RenderEvent;
import baritone.api.pathing.goals.*;
import baritone.api.utils.BetterBlockPos;
import baritone.api.utils.IPlayerContext;
import baritone.api.utils.interfaces.IGoalRenderPos;
import baritone.behavior.PathingBehavior;
import baritone.pathing.path.PathExecutor;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.dimension.DimensionType;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

import java.awt.*;
import java.util.Collection;
import java.util.List;

public final class PathRenderer implements IRenderer {
    private PathRenderer() {}

    public static double posX() { return renderManager.renderPosX(); }
    public static double posY() { return renderManager.renderPosY(); }
    public static double posZ() { return renderManager.renderPosZ(); }

    public static void render(RenderEvent event, PathingBehavior behavior) {
        final IPlayerContext ctx = behavior.ctx;
        if (ctx.world() == null) return;
        if (ctx.minecraft().screen instanceof GuiClick) {
            ((GuiClick) ctx.minecraft().screen).onRender(event.getModelViewStack(), event.getProjectionMatrix());
        }
        final DimensionType mine = ctx.world().dimensionType();
        final IPlayerContext primary = BaritoneAPI.getProvider().getPrimaryBaritone().getPlayerContext();
        if (primary.world() == null || mine != primary.world().dimensionType()) return;

        PoseStack stack = event.getModelViewStack();
        Goal goal = behavior.getGoal();
        if (goal != null && settings.renderGoal.value) {
            drawGoal(stack, ctx, goal, settings.colorGoalBox.value);
        }
        if (!settings.renderPath.value) return;

        PathExecutor current = behavior.getCurrent();
        PathExecutor next = behavior.getNext();
        if (current != null && current.getPath() != null) {
            int begin = Math.max(current.getPosition() - 1, 0);
            drawPath(stack, current.getPath().positions(), begin, settings.colorCurrentPath.value, 1.0F);
        }
        if (next != null && next.getPath() != null) {
            drawPath(stack, next.getPath().positions(), 0, settings.colorNextPath.value, 0.62F);
        }
        if (current != null && settings.renderSelectionBoxes.value) {
            drawManySelectionBoxes(stack, ctx.player(), current.toBreak(), settings.colorBlocksToBreak.value);
            drawManySelectionBoxes(stack, ctx.player(), current.toPlace(), settings.colorBlocksToPlace.value);
            drawManySelectionBoxes(stack, ctx.player(), current.toWalkInto(), settings.colorBlocksToWalkInto.value);
        }
    }

    public static void drawPath(PoseStack stack, List<BetterBlockPos> positions, int startIndex, Color color, boolean fadeOut, int fadeStart, int fadeEnd) {
        drawPath(stack, positions, startIndex, color, 1.0F);
    }

    public static void drawPath(PoseStack stack, List<BetterBlockPos> positions, int startIndex, Color color, boolean fadeOut, int fadeStart, int fadeEnd, double offset) {
        drawPath(stack, positions, startIndex, color, 1.0F);
    }

    private static void drawPath(PoseStack stack, List<BetterBlockPos> positions, int startIndex, Color color, float intensity) {
        if (positions == null || positions.size() < 2 || startIndex >= positions.size() - 1) return;
        if (!settings.enhancedVisuals.value) {
            drawLayer(stack, positions, startIndex, color, settings.pathRenderLineWidthPixels.value, 0.72F * intensity, false);
            return;
        }
        if (settings.enhancedPathGlow.value) {
            drawLayer(stack, positions, startIndex, color, settings.pathRenderLineWidthPixels.value * 3.2F, 0.10F * intensity, false);
        }
        drawLayer(stack, positions, startIndex, color, settings.pathRenderLineWidthPixels.value, 0.92F * intensity, true);
    }

    private static void drawLayer(PoseStack stack, List<BetterBlockPos> positions, int startIndex, Color color, float width, float baseAlpha, boolean markers) {
        IRenderer.startLines(color, baseAlpha, width, settings.renderPathIgnoreDepth.value);
        int fadeStart = startIndex + 18;
        int fadeEnd = startIndex + 72;
        int end = Math.min(positions.size() - 1, fadeEnd + 1);
        for (int i = startIndex; i < end; i++) {
            BetterBlockPos a = positions.get(i);
            BetterBlockPos b = positions.get(i + 1);
            float alpha = baseAlpha;
            if (settings.fadePath.value && i > fadeStart) {
                float t = Math.min(1.0F, (float)(i - fadeStart) / Math.max(1.0F, (float)(fadeEnd - fadeStart)));
                t = t * t * (3.0F - 2.0F * t);
                alpha = Math.max(0.02F, baseAlpha * (1.0F - t));
            }
            IRenderer.glColor(color, alpha);
            emitRouteSegment(stack, a, b);
            if (markers && settings.enhancedPathMarkers.value && (i - startIndex) % 8 == 0) {
                emitMarker(stack, a, 0.12D);
            }
        }
        IRenderer.endLines(settings.renderPathIgnoreDepth.value);
    }

    private static void emitRouteSegment(PoseStack stack, BetterBlockPos a, BetterBlockPos b) {
        double ax = a.x + 0.5D - posX();
        double ay = a.y + 0.12D - posY();
        double az = a.z + 0.5D - posZ();
        double bx = b.x + 0.5D - posX();
        double by = b.y + 0.12D - posY();
        double bz = b.z + 0.5D - posZ();
        IRenderer.emitLine(stack, ax, ay, az, bx, by, bz);
    }

    private static void emitMarker(PoseStack stack, BetterBlockPos p, double size) {
        double x = p.x + 0.5D - posX();
        double y = p.y + 0.13D - posY();
        double z = p.z + 0.5D - posZ();
        IRenderer.emitLine(stack, x - size, y, z, x + size, y, z);
        IRenderer.emitLine(stack, x, y, z - size, x, y, z + size);
    }

    private static void drawGoal(PoseStack stack, IPlayerContext ctx, Goal goal, Color color) {
        if (goal instanceof GoalComposite composite) {
            for (Goal child : composite.goals()) drawGoal(stack, ctx, child, color);
            return;
        }
        if (goal instanceof GoalInverted inverted) {
            drawGoal(stack, ctx, inverted.origin, settings.colorInvertedGoalBox.value);
            return;
        }
        if (goal instanceof IGoalRenderPos renderPos) {
            drawGoalDiamond(stack, renderPos.getGoalPos(), color);
            return;
        }
        if (goal instanceof GoalXZ xz) {
            drawGoalDiamond(stack, new BlockPos(xz.getX(), ctx.playerFeet().getY(), xz.getZ()), color);
            return;
        }
        if (goal instanceof GoalYLevel yLevel) {
            drawYLevel(stack, ctx, yLevel.level, color);
        }
    }

    private static void drawGoalDiamond(PoseStack stack, BlockPos p, Color color) {
        float width = settings.goalRenderLineWidthPixels.value;
        IRenderer.startLines(color, 0.16F, width * 3.0F, settings.renderGoalIgnoreDepth.value);
        emitDiamond(stack, p, 0.52D, 1.08D);
        IRenderer.endLines(settings.renderGoalIgnoreDepth.value);
        IRenderer.startLines(color, 0.94F, width, settings.renderGoalIgnoreDepth.value);
        emitDiamond(stack, p, 0.52D, 1.08D);
        IRenderer.endLines(settings.renderGoalIgnoreDepth.value);
    }

    private static void emitDiamond(PoseStack stack, BlockPos p, double r, double yOff) {
        double x = p.getX() + 0.5D - posX();
        double y = p.getY() + yOff - posY();
        double z = p.getZ() + 0.5D - posZ();
        IRenderer.emitLine(stack, x + r, y, z, x, y, z + r);
        IRenderer.emitLine(stack, x, y, z + r, x - r, y, z);
        IRenderer.emitLine(stack, x - r, y, z, x, y, z - r);
        IRenderer.emitLine(stack, x, y, z - r, x + r, y, z);
        IRenderer.emitLine(stack, x, y - 0.55D, z, x, y + 0.55D, z);
        double top = y + 0.55D;
        IRenderer.emitLine(stack, x - r * 0.45D, top, z, x, top, z + r * 0.45D);
        IRenderer.emitLine(stack, x, top, z + r * 0.45D, x + r * 0.45D, top, z);
    }

    private static void drawYLevel(PoseStack stack, IPlayerContext ctx, int level, Color color) {
        double x = ctx.player().getX() - posX();
        double y = level + 0.05D - posY();
        double z = ctx.player().getZ() - posZ();
        double r = 2.25D;
        IRenderer.startLines(color, 0.82F, settings.goalRenderLineWidthPixels.value, settings.renderGoalIgnoreDepth.value);
        IRenderer.emitLine(stack, x-r, y, z-r, x+r, y, z-r);
        IRenderer.emitLine(stack, x+r, y, z-r, x+r, y, z+r);
        IRenderer.emitLine(stack, x+r, y, z+r, x-r, y, z+r);
        IRenderer.emitLine(stack, x-r, y, z+r, x-r, y, z-r);
        IRenderer.endLines(settings.renderGoalIgnoreDepth.value);
    }

    public static void drawManySelectionBoxes(PoseStack stack, Entity player, Collection<BlockPos> positions, Color color) {
        if (positions == null || positions.isEmpty()) return;
        IRenderer.startLines(color, 0.62F, Math.max(1.0F, settings.pathRenderLineWidthPixels.value), settings.renderSelectionBoxesIgnoreDepth.value);
        BlockStateInterface bsi = new BlockStateInterface(BaritoneAPI.getProvider().getPrimaryBaritone().getPlayerContext());
        positions.forEach(pos -> {
            BlockState state = bsi.get0(pos);
            VoxelShape shape = state.getShape(player.level(), pos);
            AABB box = (shape.isEmpty() ? Shapes.block().bounds() : shape.bounds()).move(pos);
            IRenderer.emitAABB(stack, box, .002D);
        });
        IRenderer.endLines(settings.renderSelectionBoxesIgnoreDepth.value);
    }
}
'''
(root / 'src/main/java/baritone/utils/PathRenderer.java').write_text(renderer)

automation = r'''/*
 * Baritone Enhanced automation behavior. LGPL-3.0-or-later.
 */
package baritone.behavior;

import baritone.Baritone;
import baritone.api.Settings;
import baritone.api.event.events.TickEvent;
import baritone.api.pathing.goals.GoalNear;
import baritone.api.utils.Rotation;
import baritone.api.utils.RotationUtils;
import net.minecraft.core.component.DataComponents;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.AABB;

import java.util.Comparator;
import java.util.List;

public final class EnhancedAutomationBehavior extends Behavior {
    private boolean autoEating;
    private int previousSlot = -1;
    private LivingEntity combatTarget;
    private int targetRefresh;
    private int chaseRefresh;
    private boolean combatOwnsGoal;

    public EnhancedAutomationBehavior(Baritone baritone) {
        super(baritone);
    }

    @Override
    public void onTick(TickEvent event) {
        if (event.getType() != TickEvent.Type.IN || ctx.player() == null || ctx.world() == null) return;
        if (handleAutoEat()) return;
        handleAutoFight();
    }

    private boolean handleAutoEat() {
        Settings settings = Baritone.settings();
        if (!settings.autoEat.value) {
            stopEating();
            return false;
        }
        int food = ctx.player().getFoodData().getFoodLevel();
        if (!autoEating && food > settings.autoEatHunger.value) return false;
        if (autoEating && food >= settings.autoEatStopHunger.value) {
            stopEating();
            return false;
        }
        if (!autoEating) {
            previousSlot = ctx.player().getInventory().getSelectedSlot();
            if (!selectFood()) {
                previousSlot = -1;
                return false;
            }
            autoEating = true;
        }
        if (!isFood(ctx.player().getMainHandItem()) && !isFood(ctx.player().getOffhandItem())) {
            if (!selectFood()) {
                stopEating();
                return false;
            }
        }
        InteractionHand hand = isFood(ctx.player().getMainHandItem()) ? InteractionHand.MAIN_HAND : InteractionHand.OFF_HAND;
        ctx.minecraft().options.keyUse.setDown(true);
        if (!ctx.player().isUsingItem()) {
            ctx.playerController().processRightClick(ctx.player(), ctx.world(), hand);
        }
        return true;
    }

    private boolean selectFood() {
        return baritone.getInventoryBehavior().throwaway(true, this::isFood, Baritone.settings().allowInventory.value);
    }

    private boolean isFood(ItemStack stack) {
        if (stack == null || stack.isEmpty() || stack.get(DataComponents.FOOD) == null) return false;
        return !stack.is(Items.ROTTEN_FLESH)
                && !stack.is(Items.SPIDER_EYE)
                && !stack.is(Items.POISONOUS_POTATO)
                && !stack.is(Items.PUFFERFISH)
                && !stack.is(Items.GOLDEN_APPLE)
                && !stack.is(Items.ENCHANTED_GOLDEN_APPLE)
                && !stack.is(Items.CHORUS_FRUIT);
    }

    private void stopEating() {
        if (!autoEating) return;
        ctx.minecraft().options.keyUse.setDown(false);
        if (previousSlot >= 0 && previousSlot < 9) {
            ctx.player().getInventory().setSelectedSlot(previousSlot);
        }
        previousSlot = -1;
        autoEating = false;
    }

    private void handleAutoFight() {
        Settings settings = Baritone.settings();
        if (!settings.autoFight.value) {
            clearCombat();
            return;
        }
        if (targetRefresh-- <= 0 || !validTarget(combatTarget)) {
            combatTarget = findTarget();
            targetRefresh = 5;
        }
        if (combatTarget == null) {
            releaseCombatGoal();
            return;
        }
        if (settings.autoFightAutoWeapon.value) selectWeapon();

        double attackRange = Math.max(2.0D, settings.autoFightAttackRange.value);
        double distanceSq = ctx.player().distanceToSqr(combatTarget);
        if (distanceSq > attackRange * attackRange) {
            if (settings.autoFightChase.value && chaseRefresh-- <= 0) {
                baritone.getCustomGoalProcess().setGoal(new GoalNear(combatTarget.blockPosition(), 2));
                baritone.getCustomGoalProcess().path();
                combatOwnsGoal = true;
                chaseRefresh = 8;
            }
            return;
        }
        releaseCombatGoal();
        Rotation targetRotation = RotationUtils.calcRotationFromVec3d(
                ctx.player().getEyePosition(1.0F),
                combatTarget.getEyePosition(1.0F),
                ctx.playerRotations()
        );
        baritone.getLookBehavior().updateTarget(targetRotation, false);
        if (ctx.player().hasLineOfSight(combatTarget) && ctx.player().getAttackStrengthScale(0.0F) >= 0.92F) {
            ctx.minecraft().gameMode.attack(ctx.player(), combatTarget);
            ctx.player().swing(InteractionHand.MAIN_HAND);
        }
    }

    private LivingEntity findTarget() {
        Settings settings = Baritone.settings();
        double range = Math.max(2.0D, settings.autoFightSearchRange.value);
        AABB box = ctx.player().getBoundingBox().inflate(range);
        List<LivingEntity> targets = ctx.world().getEntitiesOfClass(LivingEntity.class, box, this::validTarget);
        return targets.stream().min(Comparator.comparingDouble(ctx.player()::distanceToSqr)).orElse(null);
    }

    private boolean validTarget(LivingEntity entity) {
        if (entity == null || entity == ctx.player() || !entity.isAlive()) return false;
        Settings settings = Baritone.settings();
        if (entity instanceof Player player) {
            return settings.autoFightPlayers.value && !player.isSpectator();
        }
        return settings.autoFightMobs.value && entity instanceof Monster;
    }

    private void selectWeapon() {
        ItemStack held = ctx.player().getMainHandItem();
        if (held.is(ItemTags.SWORDS) || held.is(ItemTags.AXES)) return;
        for (int i = 0; i < 9; i++) {
            if (ctx.player().getInventory().getItem(i).is(ItemTags.SWORDS)) {
                ctx.player().getInventory().setSelectedSlot(i);
                return;
            }
        }
        for (int i = 0; i < 9; i++) {
            if (ctx.player().getInventory().getItem(i).is(ItemTags.AXES)) {
                ctx.player().getInventory().setSelectedSlot(i);
                return;
            }
        }
    }

    private void releaseCombatGoal() {
        if (combatOwnsGoal) {
            baritone.getCustomGoalProcess().onLostControl();
            combatOwnsGoal = false;
        }
    }

    private void clearCombat() {
        combatTarget = null;
        targetRefresh = 0;
        chaseRefresh = 0;
        releaseCombatGoal();
    }
}
'''
(root / 'src/main/java/baritone/behavior/EnhancedAutomationBehavior.java').write_text(automation)

baritone_file = root / 'src/main/java/baritone/Baritone.java'
s = baritone_file.read_text()
old = '            this.inputOverrideHandler = this.registerBehavior(InputOverrideHandler::new);\n            this.registerBehavior(WaypointBehavior::new);'
new = '            this.inputOverrideHandler = this.registerBehavior(InputOverrideHandler::new);\n            this.registerBehavior(EnhancedAutomationBehavior::new);\n            this.registerBehavior(WaypointBehavior::new);'
if old not in s:
    raise SystemExit('Baritone behavior registration anchor missing')
s = s.replace(old, new, 1)
baritone_file.write_text(s)

auto_cmd = r'''/*
 * Baritone Enhanced commands. LGPL-3.0-or-later.
 */
package baritone.command.defaults;

import baritone.Baritone;
import baritone.api.IBaritone;
import baritone.api.Settings;
import baritone.api.Settings.Setting;
import baritone.api.command.Command;
import baritone.api.command.argument.IArgConsumer;
import baritone.api.command.exception.CommandException;

import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.stream.Stream;

public final class AutoCommand extends Command {
    public AutoCommand(IBaritone baritone) {
        super(baritone, "auto", "enhanced", "plus");
    }

    @Override
    public void execute(String label, IArgConsumer args) throws CommandException {
        args.requireMax(3);
        if (!args.hasAny()) {
            status();
            return;
        }
        String section = args.getString().toLowerCase(Locale.ROOT);
        switch (section) {
            case "status" -> status();
            case "eat" -> setBool("Auto Eat", Baritone.settings().autoEat, args);
            case "visuals", "visual" -> setBool("Enhanced Visuals", Baritone.settings().enhancedVisuals, args);
            case "mining", "mine" -> setBool("Continuous Mining", Baritone.settings().continuousMining, args);
            case "smooth", "smoothing" -> smooth(args);
            case "fight", "combat" -> fight(args);
            case "preset", "defaults" -> preset();
            default -> logDirect("Unknown module: " + section + ". Try #auto status");
        }
    }

    private void fight(IArgConsumer args) throws CommandException {
        if (!args.hasAny()) {
            Baritone.settings().autoFight.value = !Baritone.settings().autoFight.value;
            logState("Auto Fight", Baritone.settings().autoFight.value);
            return;
        }
        String sub = args.peekString().toLowerCase(Locale.ROOT);
        if (sub.equals("players") || sub.equals("mobs") || sub.equals("chase")) {
            args.getString();
            Setting<Boolean> setting = sub.equals("players") ? Baritone.settings().autoFightPlayers : sub.equals("mobs") ? Baritone.settings().autoFightMobs : Baritone.settings().autoFightChase;
            setBool("Fight " + sub, setting, args);
            return;
        }
        setBool("Auto Fight", Baritone.settings().autoFight, args);
    }

    private void smooth(IArgConsumer args) throws CommandException {
        boolean next = args.hasAny() ? parseBool(args.getString(), Baritone.settings().smoothLook.value) : !Baritone.settings().smoothLook.value;
        Baritone.settings().smoothLook.value = next;
        Baritone.settings().smoothMovementInput.value = next;
        logState("Smooth Movement", next);
    }

    private void setBool(String name, Setting<Boolean> setting, IArgConsumer args) throws CommandException {
        boolean next = args.hasAny() ? parseBool(args.getString(), setting.value) : !setting.value;
        setting.value = next;
        logState(name, next);
    }

    private boolean parseBool(String raw, boolean current) {
        return switch (raw.toLowerCase(Locale.ROOT)) {
            case "on", "true", "yes", "1", "enable", "enabled" -> true;
            case "off", "false", "no", "0", "disable", "disabled" -> false;
            case "toggle" -> !current;
            default -> current;
        };
    }

    private void preset() {
        Settings s = Baritone.settings();
        s.allowInventory.value = true;
        s.autoTool.value = true;
        s.continuousMining.value = true;
        s.blockBreakSpeed.value = 1;
        s.randomLooking.value = 0D;
        s.randomLooking113.value = 0D;
        s.smoothLook.value = true;
        s.smoothMovementInput.value = true;
        s.enhancedVisuals.value = true;
        s.enhancedPathGlow.value = true;
        s.enhancedPathMarkers.value = true;
        s.renderPath.value = true;
        s.renderPathAsLine.value = true;
        s.fadePath.value = true;
        s.renderSelectionBoxes.value = false;
        s.renderGoalAnimated.value = false;
        s.autoEat.value = true;
        logDirect("Baritone Enhanced preset applied.");
    }

    private void status() {
        Settings s = Baritone.settings();
        logDirect("Baritone Enhanced • 1.21.11");
        logDirect("Mining: " + state(s.continuousMining.value) + "  |  Auto Eat: " + state(s.autoEat.value));
        logDirect("Auto Fight: " + state(s.autoFight.value) + "  |  Players: " + state(s.autoFightPlayers.value));
        logDirect("Smooth: " + state(s.smoothLook.value) + "  |  Visuals: " + state(s.enhancedVisuals.value));
        logDirect("Use #auto <eat|fight|smooth|visuals|mining|preset> [on|off]");
    }

    private void logState(String name, boolean value) {
        logDirect(name + ": " + state(value));
    }

    private String state(boolean value) { return value ? "ON" : "OFF"; }

    @Override
    public Stream<String> tabComplete(String label, IArgConsumer args) {
        if (args.hasExactlyOne()) {
            String p = args.peekString().toLowerCase(Locale.ROOT);
            return Stream.of("status", "eat", "fight", "smooth", "visuals", "mining", "preset").filter(x -> x.startsWith(p));
        }
        return Stream.empty();
    }

    @Override
    public String getShortDesc() { return "Control Baritone Enhanced automation modules"; }

    @Override
    public List<String> getLongDesc() {
        return Arrays.asList(
                "Controls the extra Baritone Enhanced modules.",
                "#auto eat [on|off]",
                "#auto fight [on|off]",
                "#auto fight players [on|off]",
                "#auto fight mobs [on|off]",
                "#auto smooth [on|off]",
                "#auto visuals [on|off]",
                "#auto mining [on|off]",
                "#auto preset"
        );
    }
}
'''
(root / 'src/main/java/baritone/command/defaults/AutoCommand.java').write_text(auto_cmd)

defaults = root / 'src/main/java/baritone/command/defaults/DefaultCommands.java'
s = defaults.read_text()
anchor = '                new HelpCommand(baritone),\n'
insert = '''                new HelpCommand(baritone),\n                new AutoCommand(baritone),\n                new CommandAlias(baritone, Arrays.asList("automine", "dig"), "Mine blocks automatically", "mine"),\n                new CommandAlias(baritone, "go", "Go to coordinates or a goal", "goto"),\n                new CommandAlias(baritone, "halt", "Stop all Baritone activity", "cancel"),\n                new CommandAlias(baritone, "fight", "Toggle/configure auto fight", "auto fight"),\n                new CommandAlias(baritone, "eat", "Toggle/configure auto eat", "auto eat"),\n                new CommandAlias(baritone, "visuals", "Toggle the clean renderer", "auto visuals"),\n                new CommandAlias(baritone, "smooth", "Toggle movement/rotation smoothing", "auto smooth"),\n                new CommandAlias(baritone, "status", "Show Baritone Enhanced status", "auto status"),\n'''
if anchor not in s:
    raise SystemExit('DefaultCommands help anchor missing')
s = s.replace(anchor, insert, 1)
defaults.write_text(s)

help_src = r'''/*
 * Baritone Enhanced help. LGPL-3.0-or-later.
 */
package baritone.command.defaults;

import baritone.api.IBaritone;
import baritone.api.command.Command;
import baritone.api.command.ICommand;
import baritone.api.command.argument.IArgConsumer;
import baritone.api.command.exception.CommandException;
import baritone.api.command.exception.CommandNotFoundException;
import baritone.api.command.helpers.TabCompleteHelper;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

public final class HelpCommand extends Command {
    public HelpCommand(IBaritone baritone) {
        super(baritone, "help", "?");
    }

    @Override
    public void execute(String label, IArgConsumer args) throws CommandException {
        args.requireMax(1);
        if (!args.hasAny()) {
            logDirect("Baritone Enhanced • 1.21.11");
            logDirect("MOVE   #go <x> <y> <z>   •   #come   •   #follow");
            logDirect("MINE   #automine <block>   •   #tunnel   •   #farm");
            logDirect("AUTO   #fight   •   #eat   •   #status");
            logDirect("LOOK   #visuals   •   #smooth");
            logDirect("STOP   #halt");
            logDirect("Use #help <command> for details or #help all for everything.");
            return;
        }
        String name = args.getString().toLowerCase();
        if (name.equals("all")) {
            logDirect("All Baritone Enhanced commands:");
            this.baritone.getCommandManager().getRegistry().descendingStream()
                    .filter(command -> !command.hiddenFromHelp())
                    .forEach(command -> logDirect("#" + command.getNames().get(0) + " - " + command.getShortDesc()));
            return;
        }
        ICommand command = this.baritone.getCommandManager().getCommand(name);
        if (command == null) throw new CommandNotFoundException(name);
        logDirect(String.join(" / ", command.getNames()) + " - " + command.getShortDesc());
        command.getLongDesc().forEach(this::logDirect);
    }

    @Override
    public Stream<String> tabComplete(String label, IArgConsumer args) throws CommandException {
        if (args.hasExactlyOne()) {
            return Stream.concat(Stream.of("all"), new TabCompleteHelper().addCommands(this.baritone.getCommandManager()).filterPrefix(args.getString()).stream());
        }
        return Stream.empty();
    }

    @Override
    public String getShortDesc() { return "Show the clean Baritone Enhanced command guide"; }

    @Override
    public List<String> getLongDesc() {
        return Arrays.asList("#help", "#help <command>", "#help all");
    }
}
'''
(root / 'src/main/java/baritone/command/defaults/HelpCommand.java').write_text(help_src)

version = root / 'src/main/java/baritone/command/defaults/VersionCommand.java'
s = version.read_text()
s = s.replace('logDirect(String.format("You are running Baritone v%s", version));', 'logDirect(String.format("Baritone Enhanced v%s • Minecraft 1.21.11", version));')
version.write_text(s)

(root / 'BARITONE_ENHANCED_COMMANDS.txt').write_text('''Baritone Enhanced 1.21.11\n\nCore\n#go <x> <y> <z>\n#automine <block>\n#tunnel\n#farm\n#halt\n\nAutomation\n#eat [on|off]\n#fight [on|off]\n#fight mobs [on|off]\n#fight players [on|off]\n#visuals [on|off]\n#smooth [on|off]\n#auto mining [on|off]\n#status\n#auto preset\n\nPlayer combat is OFF by default. Hostile mob combat is enabled as a target type, but the auto-fight module itself is OFF by default.\n''')
print('Baritone Enhanced source patches applied.')
