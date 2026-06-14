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
    align = "left"
  } = options;
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 96;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.font = font;
  ctx.textAlign = align;
  ctx.textBaseline = "middle";
  ctx.fillStyle = "rgba(5, 5, 5, 0.68)";
  ctx.fillRect(0, 10, canvas.width, canvas.height - 20);
  ctx.strokeStyle = "rgba(243, 244, 246, 0.18)";
  ctx.strokeRect(0.5, 10.5, canvas.width - 1, canvas.height - 21);
  ctx.fillStyle = colorToCss(color);
  ctx.fillText(text, align === "center" ? canvas.width / 2 : 22, canvas.height / 2 + 1);
  const texture = new THREE.CanvasTexture(canvas);
  texture.needsUpdate = true;
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: texture,
    transparent: true,
    depthWrite: false
  }));
  sprite.scale.set(scale[0], scale[1], 1);
  return sprite;
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
    frameOpacity = 0.25,
    traceOpacity = 0.57,
    cursorOpacity = 0.26,
    label = "",
    labelColor = color
  } = options;
  const group = new THREE.Group();
  const frameMat = new THREE.LineBasicMaterial({
    color: frameColor,
    transparent: true,
    opacity: frameOpacity
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
  group.add(frame, trace, cursor);
  if (label) {
    const labelSprite = createTextSprite(THREE, label, {
      color: labelColor,
      scale: [Math.min(width * 0.58, 1.28), 0.15]
    });
    labelSprite.position.set(origin.x + width * 0.29, origin.y + height + 0.14, origin.z + 0.04);
    group.add(labelSprite);
  }
  return { group, origin, width, height, max, samples: [], trace, cursor };
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
}
