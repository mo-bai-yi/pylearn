/* Turtle Canvas 前端渲染器 — 支持自动缩放和平移 */

let turtleCtx = null;
let turtleAnimId = null;
let turtleX = 250, turtleY = 250;
let turtleAngle = 0;
let turtlePenDown = true;
let turtleColor = '#333333';
let turtleSize = 2;
let turtleVisible = true;
let turtleCommands = [];
let turtleCmdIndex = 0;
let turtleSpeed = 3;

// 所有已绘制的线条
let turtleLines = [];

// 缩放状态（从 localStorage 恢复，跨页面保持）
const _ZOOM_KEY = 'pylearn_turtle_zoom';
let currentScale = parseFloat(localStorage.getItem(_ZOOM_KEY + '_scale')) || 1;
let currentOffsetX = parseFloat(localStorage.getItem(_ZOOM_KEY + '_ox')) || 0;
let currentOffsetY = parseFloat(localStorage.getItem(_ZOOM_KEY + '_oy')) || 0;

const CANVAS_W = 500, CANVAS_H = 500;

// 颜色映射
const TURTLE_COLORS = {
    'red': '#ef4444', 'green': '#22c55e', 'blue': '#3b82f6',
    'yellow': '#eab308', 'purple': '#a855f7', 'orange': '#f97316',
    'pink': '#ec4899', 'brown': '#92400e', 'black': '#000000',
    'white': '#ffffff', 'gray': '#6b7280', 'grey': '#6b7280',
    'cyan': '#06b6d4', 'magenta': '#d946ef',
};

function initTurtleCanvas() {
    const canvas = document.getElementById('turtle-canvas');
    if (!canvas) return;
    canvas.width = CANVAS_W;
    canvas.height = CANVAS_H;
    turtleCtx = canvas.getContext('2d');
    clearTurtleCanvas();
}

function drawGrid(ctx) {
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 1;
    for (let x = 0; x <= CANVAS_W; x += 50) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, CANVAS_H);
        ctx.stroke();
    }
    for (let y = 0; y <= CANVAS_H; y += 50) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(CANVAS_W, y);
        ctx.stroke();
    }
}

/** 执行一次完整重绘：清空 → 变换 → 网格 → 所有线条 → 海龟 */
function fullRedraw() {
    if (!turtleCtx) return;
    const ctx = turtleCtx;

    // 清空
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);

    // 应用缩放变换
    ctx.save();
    ctx.setTransform(
        currentScale, 0, 0, currentScale,
        currentOffsetX, currentOffsetY
    );

    // 网格（受变换影响）
    drawGrid(ctx);

    // 重绘所有已保存的线条
    ctx.lineCap = 'round';
    for (const l of turtleLines) {
        ctx.beginPath();
        ctx.moveTo(l.x1, l.y1);
        ctx.lineTo(l.x2, l.y2);
        ctx.strokeStyle = l.color;
        ctx.lineWidth = l.size;
        ctx.stroke();
    }

    ctx.restore();

    // 海龟在变换之外绘制？不，海龟也应该在变换内
    ctx.save();
    ctx.setTransform(
        currentScale, 0, 0, currentScale,
        currentOffsetX, currentOffsetY
    );
    drawTurtle(ctx);
    ctx.restore();
}

function addLine(x1, y1, x2, y2) {
    turtleLines.push({
        x1, y1, x2, y2,
        color: turtleColor,
        size: turtleSize,
    });
}

function _saveZoomState() {
    try {
        localStorage.setItem(_ZOOM_KEY + '_scale', String(currentScale));
        localStorage.setItem(_ZOOM_KEY + '_ox', String(currentOffsetX));
        localStorage.setItem(_ZOOM_KEY + '_oy', String(currentOffsetY));
    } catch (_) {}
}

function clearTurtleCanvas() {
    if (!turtleCtx) initTurtleCanvas();
    if (!turtleCtx) return;

    if (turtleAnimId) {
        cancelAnimationFrame(turtleAnimId);
        turtleAnimId = null;
    }

    // 重置海龟状态，但保持缩放不变
    turtleX = 250;
    turtleY = 250;
    turtleAngle = 0;
    turtlePenDown = true;
    turtleColor = '#333333';
    turtleSize = 2;
    turtleVisible = true;
    turtleCmdIndex = 0;
    turtleCommands = [];
    turtleLines = [];

    fullRedraw();
}

function drawTurtle(ctx) {
    if (!ctx || !turtleVisible) return;
    const x = turtleX, y = turtleY;
    const angleRad = (90 - turtleAngle) * Math.PI / 180;

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angleRad);

    ctx.beginPath();
    ctx.moveTo(0, -10);
    ctx.lineTo(-7, 7);
    ctx.lineTo(7, 7);
    ctx.closePath();
    ctx.fillStyle = '#22c55e';
    ctx.fill();
    ctx.strokeStyle = '#16a34a';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.restore();
}

/** 模拟执行所有命令，计算边界盒 */
function computeBounds(commands) {
    let x = 250, y = 250, angle = 0;
    let minX = 250, maxX = 250, minY = 250, maxY = 250;

    for (const cmd of commands) {
        const aRad = angle * Math.PI / 180;
        let nx = x, ny = y;

        switch (cmd.cmd) {
            case 'fd':
                nx = x + cmd.args[0] * Math.cos(aRad);
                ny = y - cmd.args[0] * Math.sin(aRad);
                break;
            case 'bk':
                nx = x - cmd.args[0] * Math.cos(aRad);
                ny = y + cmd.args[0] * Math.sin(aRad);
                break;
            case 'rt':
                angle = (angle - (cmd.args[0] || 0) + 360) % 360;
                continue;
            case 'lt':
                angle = (angle + (cmd.args[0] || 0) + 360) % 360;
                continue;
            case 'goto': {
                const tx = cmd.args[0] !== undefined ? cmd.args[0] : nx;
                const ty = cmd.args[1] !== undefined ? cmd.args[1] : ny;
                nx = tx; ny = ty;
                break;
            }
            case 'circle': {
                const r = cmd.args[0] || 50;
                minX = Math.min(minX, x - r);
                maxX = Math.max(maxX, x + r);
                minY = Math.min(minY, y - r);
                maxY = Math.max(maxY, y + r);
                continue;
            }
            case 'home':
                nx = 250; ny = 250; angle = 0;
                continue;
            case 'seth':
                angle = (cmd.args[0] || 0) % 360;
                continue;
            default:
                continue;
        }

        x = nx; y = ny;
        minX = Math.min(minX, x);
        maxX = Math.max(maxX, x);
        minY = Math.min(minY, y);
        maxY = Math.max(maxY, y);
    }

    return { minX, maxX, minY, maxY, w: maxX - minX, h: maxY - minY };
}

/** 计算自动适配的缩放和平移 */
function calcAutoFit(commands) {
    if (!commands || commands.length === 0) return { scale: 1, ox: 0, oy: 0 };

    const bounds = computeBounds(commands);
    const contentW = bounds.w || 1;
    const contentH = bounds.h || 1;
    const padding = 40;

    // 计算最小缩放
    const scaleX = (CANVAS_W - padding * 2) / contentW;
    const scaleY = (CANVAS_H - padding * 2) / contentH;
    let scale = Math.min(scaleX, scaleY);
    scale = Math.min(scale, 3); // 最大3倍
    scale = Math.max(scale, 0.1); // 最小0.1倍

    // 居中
    const centerX = (bounds.minX + bounds.maxX) / 2;
    const centerY = (bounds.minY + bounds.maxY) / 2;
    const ox = CANVAS_W / 2 - centerX * scale;
    const oy = CANVAS_H / 2 - centerY * scale;

    return { scale, ox, oy };
}

function applyTurtleCommand(cmd, args) {
    if (!turtleCtx) return false;

    const ctx = turtleCtx;
    const angleRad = turtleAngle * Math.PI / 180;

    switch (cmd) {
        case 'fd': {
            const dist = args[0] || 0;
            const nx = turtleX + dist * Math.cos(angleRad);
            const ny = turtleY - dist * Math.sin(angleRad);
            if (turtlePenDown) addLine(turtleX, turtleY, nx, ny);
            turtleX = nx;
            turtleY = ny;
            break;
        }
        case 'bk': {
            const dist = args[0] || 0;
            const nx = turtleX - dist * Math.cos(angleRad);
            const ny = turtleY + dist * Math.sin(angleRad);
            if (turtlePenDown) addLine(turtleX, turtleY, nx, ny);
            turtleX = nx;
            turtleY = ny;
            break;
        }
        case 'rt':
            turtleAngle = (turtleAngle - (args[0] || 0) + 360) % 360;
            break;
        case 'lt':
            turtleAngle = (turtleAngle + (args[0] || 0) + 360) % 360;
            break;
        case 'pu':
            turtlePenDown = false;
            break;
        case 'pd':
            turtlePenDown = true;
            break;
        case 'pensize':
            turtleSize = args[0] || 2;
            break;
        case 'pencolor': {
            const col = args[0] || '#333';
            turtleColor = TURTLE_COLORS[col] || col;
            break;
        }
        case 'circle': {
            const r = args[0] || 50;
            if (turtlePenDown) {
                // 近似为多条直线
                const segments = 36;
                for (let i = 0; i < segments; i++) {
                    const a1 = (i / segments) * Math.PI * 2;
                    const a2 = ((i + 1) / segments) * Math.PI * 2;
                    const x1 = turtleX + r * Math.sin(a1);
                    const y1 = turtleY - r * Math.cos(a1);
                    const x2 = turtleX + r * Math.sin(a2);
                    const y2 = turtleY - r * Math.cos(a2);
                    addLine(x1, y1, x2, y2);
                }
            }
            break;
        }
        case 'goto': {
            const tx = args[0] !== undefined ? args[0] : turtleX;
            const ty = args[1] !== undefined ? args[1] : turtleY;
            if (turtlePenDown) addLine(turtleX, turtleY, tx, ty);
            turtleX = tx;
            turtleY = ty;
            break;
        }
        case 'home':
            turtleX = 250; turtleY = 250; turtleAngle = 0;
            break;
        case 'clear':
            clearTurtleCanvas();
            return true;
        case 'ht':
            turtleVisible = false;
            break;
        case 'st':
            turtleVisible = true;
            break;
    }

    return true;
}

function renderTurtleCommands(commands, speed) {
    clearTurtleCanvas();
    turtleCommands = commands || [];
    turtleCmdIndex = 0;
    turtleSpeed = speed || 3;

    if (turtleAnimId) {
        cancelAnimationFrame(turtleAnimId);
        turtleAnimId = null;
    }

    if (turtleCommands.length === 0) return;

    // 更新缩放标签
    updateZoomLabel();

    // 速度映射
    const delay = Math.max(30, 380 - turtleSpeed * 35);
    let lastTime = 0;

    function animate(timestamp) {
        if (lastTime === 0) lastTime = timestamp;
        const elapsed = timestamp - lastTime;

        if (elapsed >= delay && turtleCmdIndex < turtleCommands.length) {
            const cmd = turtleCommands[turtleCmdIndex];
            applyTurtleCommand(cmd.cmd, cmd.args);
            fullRedraw();
            turtleCmdIndex++;
            lastTime = timestamp;
        }

        if (turtleCmdIndex < turtleCommands.length) {
            turtleAnimId = requestAnimationFrame(animate);
        }
    }

    turtleAnimId = requestAnimationFrame(animate);
}

/* ===== 缩放控制（以画布中心为锚点） ===== */
function zoomAtCenter(factor) {
    const cx = CANVAS_W / 2;
    const cy = CANVAS_H / 2;
    // 保持中心点对应的世界坐标不变
    currentOffsetX = cx * (1 - factor) + factor * currentOffsetX;
    currentOffsetY = cy * (1 - factor) + factor * currentOffsetY;
    currentScale *= factor;
}

function zoomIn() {
    if (!turtleCtx) return;
    zoomAtCenter(1.3);
    updateZoomLabel();
    _saveZoomState();
    fullRedraw();
}

function zoomOut() {
    if (!turtleCtx) return;
    zoomAtCenter(1 / 1.3);
    updateZoomLabel();
    _saveZoomState();
    fullRedraw();
}

function zoomReset() {
    if (!turtleCtx) return;
    currentScale = 1;
    currentOffsetX = 0;
    currentOffsetY = 0;
    updateZoomLabel();
    _saveZoomState();
    fullRedraw();
}

function zoomAutoFit() {
    if (!turtleCtx || turtleCommands.length === 0) return;
    const fit = calcAutoFit(turtleCommands);
    currentScale = fit.scale;
    currentOffsetX = fit.ox;
    currentOffsetY = fit.oy;
    updateZoomLabel();
    _saveZoomState();
    fullRedraw();
}

function updateZoomLabel() {
    const el = document.getElementById('zoom-label');
    if (el) el.textContent = Math.round(currentScale * 100) + '%';
}

document.addEventListener('DOMContentLoaded', function() {
    initTurtleCanvas();
});
