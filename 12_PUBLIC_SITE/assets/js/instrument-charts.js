function colorToCss(color) {
  if (typeof color === "number") {
    return "#" + color.toString(16).padStart(6, "0");
  }
  return color || "#f3f4f6";
}

export function createTextSprite(THREE, text, options = {}) {
  const {
    color = "#f3f4f6",
    font = "700 22px Roboto Mono, ui-monospace, Menlo, monospace",
    scale = [0.86, 0.14],
    align = "left",
    background = true,
    stroke = true
  } = options;
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 96;
  const ctx = canvas.getContext("2d");
  const texture = new THREE.CanvasTexture(canvas);
  drawTextSprite(ctx, texture, text, { color, font, align, background, stroke });
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: texture,
    transparent: true,
    depthTest: false,
    depthWrite: false
  }));
  sprite.scale.set(scale[0], scale[1], 1);
  sprite.userData.instrumentText = { ctx, texture, color, font, align, background, stroke };
  return sprite;
}

function drawTextSprite(ctx, texture, text, options) {
  const {
    color,
    font,
    align = "left",
    background = true,
    stroke = true
  } = options;
  const { canvas } = ctx;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.font = font;
  ctx.textAlign = align;
  ctx.textBaseline = "middle";
  if (background) {
    ctx.fillStyle = "rgba(5, 5, 5, 0.68)";
    ctx.fillRect(0, 10, canvas.width, canvas.height - 20);
  }
  if (stroke) {
    ctx.strokeStyle = "rgba(243, 244, 246, 0.18)";
    ctx.strokeRect(0.5, 10.5, canvas.width - 1, canvas.height - 21);
  }
  ctx.fillStyle = colorToCss(color);
  const x = align === "center" ? canvas.width / 2 : (align === "right" ? canvas.width - 22 : 22);
  ctx.fillText(String(text), x, canvas.height / 2 + 1);
  texture.needsUpdate = true;
}

function setTextSpriteText(sprite, text) {
  const state = sprite && sprite.userData && sprite.userData.instrumentText;
  if (!state) return;
  drawTextSprite(state.ctx, state.texture, text, state);
}

function formatTick(value) {
  if (!Number.isFinite(value)) return "--";
  const abs = Math.abs(value);
  if (abs !== 0 && (abs >= 1000 || abs < 0.01)) return value.toExponential(1);
  if (abs >= 100) return value.toFixed(0);
  if (abs >= 10) return value.toFixed(1).replace(/\.0$/, "");
  if (abs >= 1) return value.toFixed(2).replace(/0$/, "").replace(/\.0$/, "");
  return value.toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

export function createStripChart(THREE, options = {}) {
  const {
    origin = new THREE.Vector3(),
    width = 2.2,
    height = 0.52,
    color = 0x2196f3,
    max = 144,
    cursorColor = 0xf3f4f6,
    frameColor = 0x6d7480,
    frameOpacity = 0.38,
    gridOpacity = 0.18,
    traceOpacity = 0.78,
    cursorOpacity = 0.36,
    label = "",
    labelColor = color,
    targetValue = null,
    targetBand = null,
    targetColor = 0xffeb3b,
    currentMarkerColor = color,
    showScale = true,
    scaleColor = "#9ca3af",
    unitLabel = ""
  } = options;
  const group = new THREE.Group();
  const frameMat = new THREE.LineBasicMaterial({
    color: frameColor,
    transparent: true,
    opacity: frameOpacity
  });
  const gridMat = new THREE.LineBasicMaterial({
    color: frameColor,
    transparent: true,
    opacity: gridOpacity
  });
  const frame = new THREE.LineSegments(
    new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(origin.x, origin.y, origin.z),
      new THREE.Vector3(origin.x + width, origin.y, origin.z),
      new THREE.Vector3(origin.x, origin.y + height, origin.z),
      new THREE.Vector3(origin.x + width, origin.y + height, origin.z),
      new THREE.Vector3(origin.x, origin.y, origin.z),
      new THREE.Vector3(origin.x, origin.y + height, origin.z),
      new THREE.Vector3(origin.x + width, origin.y, origin.z),
      new THREE.Vector3(origin.x + width, origin.y + height, origin.z),
      new THREE.Vector3(origin.x, origin.y + height * 0.5, origin.z),
      new THREE.Vector3(origin.x + width, origin.y + height * 0.5, origin.z)
    ]),
    frameMat
  );
  const gridPoints = [];
  for (let i = 1; i < 4; i += 1) {
    const x = origin.x + width * (i / 4);
    gridPoints.push(
      new THREE.Vector3(x, origin.y, origin.z + 0.002),
      new THREE.Vector3(x, origin.y + height, origin.z + 0.002)
    );
    if (i !== 2) {
      const y = origin.y + height * (i / 4);
      gridPoints.push(
        new THREE.Vector3(origin.x, y, origin.z + 0.002),
        new THREE.Vector3(origin.x + width, y, origin.z + 0.002)
      );
    }
  }
  const grid = new THREE.LineSegments(
    new THREE.BufferGeometry().setFromPoints(gridPoints),
    gridMat
  );
  let bandMesh = null;
  if (Array.isArray(targetBand) && targetBand.length === 2) {
    bandMesh = new THREE.Mesh(
      new THREE.PlaneGeometry(1, 1),
      new THREE.MeshBasicMaterial({
        color: targetColor,
        transparent: true,
        opacity: 0.16,
        depthWrite: false,
        side: THREE.DoubleSide
      })
    );
    bandMesh.position.set(origin.x + width / 2, origin.y + height / 2, origin.z + 0.004);
    bandMesh.scale.set(width, height, 1);
  }
  const targetLine = typeof targetValue === "number"
    ? new THREE.Line(
      new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(origin.x, origin.y, origin.z + 0.01),
        new THREE.Vector3(origin.x + width, origin.y, origin.z + 0.01)
      ]),
      new THREE.LineBasicMaterial({
        color: targetColor,
        transparent: true,
        opacity: 0.5
      })
    )
    : null;
  const trace = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(origin.x, origin.y, origin.z + 0.012),
      new THREE.Vector3(origin.x + 0.001, origin.y, origin.z + 0.012)
    ]),
    new THREE.LineBasicMaterial({
      color,
      transparent: true,
      opacity: traceOpacity
    })
  );
  const cursor = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(origin.x, origin.y, origin.z + 0.018),
      new THREE.Vector3(origin.x, origin.y + height, origin.z + 0.018)
    ]),
    new THREE.LineBasicMaterial({
      color: cursorColor,
      transparent: true,
      opacity: cursorOpacity
    })
  );
  const currentMarker = new THREE.Mesh(
    new THREE.CircleGeometry(Math.min(width, height) * 0.055, 24),
    new THREE.MeshBasicMaterial({
      color: currentMarkerColor,
      transparent: true,
      opacity: 0.96,
      depthWrite: false,
      side: THREE.DoubleSide
    })
  );
  currentMarker.position.set(origin.x + width, origin.y, origin.z + 0.026);
  group.add(frame, grid);
  if (bandMesh) group.add(bandMesh);
  if (targetLine) group.add(targetLine);
  group.add(trace, cursor, currentMarker);
  if (label) {
    const labelSprite = createTextSprite(THREE, label, {
      color: labelColor,
      scale: [Math.min(width * 0.58, 1.28), 0.15]
    });
    labelSprite.position.set(origin.x + width * 0.29, origin.y + height + 0.14, origin.z + 0.04);
    group.add(labelSprite);
  }
  const scaleLabels = [];
  if (showScale) {
    [
      { key: "max", y: origin.y + height, text: "1" },
      { key: "mid", y: origin.y + height / 2, text: "0.5" },
      { key: "min", y: origin.y, text: "0" }
    ].forEach((tick) => {
      const sprite = createTextSprite(THREE, tick.text, {
        color: scaleColor,
        font: "700 18px Roboto Mono, ui-monospace, Menlo, monospace",
        scale: [0.24, 0.055],
        align: "right",
        background: false,
        stroke: false
      });
      sprite.position.set(origin.x - 0.08, tick.y, origin.z + 0.038);
      group.add(sprite);
      scaleLabels.push({ ...tick, sprite });
    });
    if (unitLabel) {
      const unitSprite = createTextSprite(THREE, unitLabel, {
        color: scaleColor,
        font: "700 15px Roboto Mono, ui-monospace, Menlo, monospace",
        scale: [0.34, 0.05],
        align: "left",
        background: false,
        stroke: false
      });
      unitSprite.position.set(origin.x + width - 0.08, origin.y - 0.1, origin.z + 0.038);
      group.add(unitSprite);
      scaleLabels.push({ key: "unit", sprite: unitSprite, unit: true });
    }
  }
  return {
    group,
    origin,
    width,
    height,
    max,
    samples: [],
    trace,
    cursor,
    currentMarker,
    targetLine,
    targetBand,
    bandMesh,
    targetValue,
    scaleLabels,
    unitLabel
  };
}

export function clearStripChart(THREE, chart) {
  chart.samples.length = 0;
  chart.trace.geometry.setFromPoints([
    new THREE.Vector3(chart.origin.x, chart.origin.y, chart.origin.z + 0.012),
    new THREE.Vector3(chart.origin.x + 0.001, chart.origin.y, chart.origin.z + 0.012)
  ]);
}

export function updateStripChart(THREE, chart, value, min = 0, max = 1, sampled = false) {
  const span = Math.max(max - min, 1e-9);
  const normalized = Math.max(0, Math.min(1, (value - min) / span));
  if (sampled || chart.samples.length === 0) {
    chart.samples.push(normalized);
    if (chart.samples.length > chart.max) chart.samples.shift();
  }
  const samples = chart.samples.length > 1 ? chart.samples : [normalized, normalized];
  const denom = Math.max(samples.length - 1, 1);
  chart.trace.geometry.setFromPoints(samples.map((sample, index) => new THREE.Vector3(
    chart.origin.x + (index / denom) * chart.width,
    chart.origin.y + sample * chart.height,
    chart.origin.z + 0.012
  )));
  const x = chart.origin.x + chart.width;
  chart.cursor.geometry.setFromPoints([
    new THREE.Vector3(x, chart.origin.y, chart.origin.z + 0.018),
    new THREE.Vector3(x, chart.origin.y + chart.height, chart.origin.z + 0.018)
  ]);
  if (chart.currentMarker) {
    chart.currentMarker.position.set(x, chart.origin.y + normalized * chart.height, chart.origin.z + 0.026);
  }
  if (chart.targetLine && typeof chart.targetValue === "number") {
    const targetN = Math.max(0, Math.min(1, (chart.targetValue - min) / span));
    const y = chart.origin.y + targetN * chart.height;
    chart.targetLine.geometry.setFromPoints([
      new THREE.Vector3(chart.origin.x, y, chart.origin.z + 0.01),
      new THREE.Vector3(chart.origin.x + chart.width, y, chart.origin.z + 0.01)
    ]);
  }
  if (chart.bandMesh && Array.isArray(chart.targetBand) && chart.targetBand.length === 2) {
    const low = Math.max(0, Math.min(1, (Math.min(chart.targetBand[0], chart.targetBand[1]) - min) / span));
    const high = Math.max(0, Math.min(1, (Math.max(chart.targetBand[0], chart.targetBand[1]) - min) / span));
    const bandHeight = Math.max((high - low) * chart.height, chart.height * 0.018);
    chart.bandMesh.position.set(
      chart.origin.x + chart.width / 2,
      chart.origin.y + ((low + high) / 2) * chart.height,
      chart.origin.z + 0.004
    );
    chart.bandMesh.scale.set(chart.width, bandHeight, 1);
    chart.bandMesh.visible = high >= low;
  }
  if (Array.isArray(chart.scaleLabels) && chart.scaleLabels.length) {
    const mid = min + span / 2;
    chart.scaleLabels.forEach((tick) => {
      if (tick.unit) {
        setTextSpriteText(tick.sprite, chart.unitLabel || "");
      } else if (tick.key === "max") {
        setTextSpriteText(tick.sprite, formatTick(max));
      } else if (tick.key === "mid") {
        setTextSpriteText(tick.sprite, formatTick(mid));
      } else if (tick.key === "min") {
        setTextSpriteText(tick.sprite, formatTick(min));
      }
    });
  }
}
