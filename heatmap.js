// heatmap.js  (원본 index.html과 동일한 컬러/렌더링 방식)

const COLOR_STOPS = [
    { v: 0.0,  rgb: [3, 0, 0] },
    { v: 0.2,  rgb: [30, 5, 2] },
    { v: 0.4,  rgb: [110, 30, 10] },
    { v: 0.6,  rgb: [190, 70, 20] },
    { v: 0.8,  rgb: [240, 135, 50] },
    { v: 1.0,  rgb: [255, 232, 185] }
  ];
  
  function brightnessToColor(value) {
    const v = Math.max(0, Math.min(1, Math.pow(value, 0.6)));

    let lower = COLOR_STOPS[0];
    let upper = COLOR_STOPS[COLOR_STOPS.length - 1];
  
    for (let i = 0; i < COLOR_STOPS.length - 1; i++) {
      const a = COLOR_STOPS[i];
      const b = COLOR_STOPS[i + 1];
      if (v >= a.v && v <= b.v) {
        lower = a;
        upper = b;
        break;
      }
    }
  
    const t = (v - lower.v) / (upper.v - lower.v || 1);
    const r = Math.round(lower.rgb[0] + (upper.rgb[0] - lower.rgb[0]) * t);
    const g = Math.round(lower.rgb[1] + (upper.rgb[1] - lower.rgb[1]) * t);
    const b = Math.round(lower.rgb[2] + (upper.rgb[2] - lower.rgb[2]) * t);
  
    return `rgb(${r}, ${g}, ${b})`;
  }
  
  function drawHeatmap(canvas, cityData) {
    const dates = cityData.dates;
    const times = cityData.times;
    const values = cityData.values;
  
    const rows = dates.length;
    const cols = times.length;
    if (!rows || !cols) return;
  
    const dpr = window.devicePixelRatio || 1;
  
    const displayWidth  = canvas.clientWidth  || canvas.width  || 800;
    const displayHeight = canvas.clientHeight || canvas.height || 400;
  
    canvas.width  = displayWidth * dpr;
    canvas.height = displayHeight * dpr;
  
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  
    const cellW = displayWidth / cols;
    const cellH = displayHeight / rows;
  
    for (let r = 0; r < rows; r++) {
      const row = values[r];
      for (let c = 0; c < cols; c++) {
        const v = row[c] ?? 0;
        ctx.fillStyle = brightnessToColor(v);
        ctx.fillRect(c * cellW, r * cellH, cellW + 0.5, cellH + 0.5);
      }
    }
  }
  window.HEATMAP_COLOR_STOPS = COLOR_STOPS;
  