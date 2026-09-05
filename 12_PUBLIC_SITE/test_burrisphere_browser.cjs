/* Bounded local QA. NODE_PATH may point to an existing Playwright installation.
 * Does not install packages, contact a model, modify site content, or deploy.
 */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const BASE = process.env.BURRISPHERE_QA_URL || 'http://127.0.0.1:8781';
if (!['127.0.0.1','localhost'].includes(new URL(BASE).hostname)) throw Error('Local preview only');
const OUT = path.join(__dirname, 'output/playwright/burrisphere-20260905');
fs.mkdirSync(OUT, {recursive:true});
const results = [], errors = [], external = [];

(async () => {
  const browser = await chromium.launch({headless:true});
  try {
    async function context(options = {}) {
      const ctx = await browser.newContext(options);
      await ctx.route('**/*', route => {
        const url = new URL(route.request().url());
        if (['127.0.0.1','localhost'].includes(url.hostname)) return route.continue();
        external.push(url.origin); return route.abort();
      });
      const page = await ctx.newPage();
      page.on('pageerror', e => errors.push(e.message));
      await page.goto(BASE+'/burrisphere/instrument/', {waitUntil:'networkidle'});
      return {ctx,page};
    }
    for (const [width,height] of [[1440,1000],[1024,768],[768,1024],[390,844],[320,568],[844,390]]) {
      const {ctx,page} = await context({viewport:{width,height}});
      await page.waitForFunction(()=>document.querySelector('#burrisphere-canvas').dataset.camera);
      assert.equal(await page.locator('#geometry-controls').isDisabled(),false);
      const overflow = await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth);
      assert.equal(overflow, false, `overflow ${width}x${height}`);
      for (const id of ['phi','nu','product','balance','theta','azimuth']) {
        assert.ok(await page.locator('#'+id+'-value').isVisible(), `${id} hidden`);
      }
      assert.ok(await page.locator('.bi-nav a[href="/exit/"]').isVisible());
      assert.ok(await page.locator('#live-legend').isVisible());
      assert.match(await page.locator('#legend-move').textContent(),/Kṛṣṇa.*Giving-A/);
      const legendSpace = await page.evaluate(()=>{
        const legend=document.querySelector('.bi-thesis').getBoundingClientRect();
        const hint=document.querySelector('.bi-drag-hint').getBoundingClientRect();
        return hint.top-legend.bottom;
      });
      assert.ok(legendSpace>=45,`legend covers chart ${width}x${height}: ${legendSpace}`);
      const before = await page.locator('#burrisphere-canvas').getAttribute('data-theta-degrees');
      await page.locator('#kali_take_phi summary').focus();
      await page.keyboard.press('Enter');
      assert.ok(await page.locator('#kali_take_phi').evaluate(el=>el.open));
      assert.equal(await page.locator('#burrisphere-canvas').getAttribute('data-theta-degrees'),before);
      if (width<=700) {
        const visual = await page.locator('#sphere-viewport').boundingBox();
        assert.ok(visual.y>=59 && visual.y+visual.height<=height, 'mobile sphere lost during rule reading');
      }
      const shortTargets = await page.locator('.bi-actions button, .bi-equation summary, .bi-titan-links a').evaluateAll(elements=>elements.filter(e=>e.getBoundingClientRect().height<48).map(e=>e.textContent));
      assert.deepEqual(shortTargets,[]);
      await page.locator('.bi-workbench').evaluate(el=>el.scrollTop=0);
      await page.evaluate(()=>window.scrollTo(0,0));
      await page.screenshot({path:path.join(OUT,`${width}x${height}.png`)});
      results.push({viewport:[width,height], overflow:false, geometry:'started', allReadouts:true, keyboardRule:true});
      await ctx.close();
    }
    const {ctx,page} = await context({viewport:{width:1440,height:1000}});
    await page.waitForFunction(()=>document.querySelector('#burrisphere-canvas').dataset.camera);
    const canvas = page.locator('#burrisphere-canvas');
    async function slider(id,value,event='input') {
      await page.locator('#'+id).evaluate((el,{value,event})=>{el.value=String(value);el.dispatchEvent(new Event(event,{bubbles:true}));},{value,event});
    }
    const legend=page.locator('#live-legend');
    for (const [bearing,operator,alias] of [[-45,'kali_take_phi','Kali'],[45,'kali_take_v','Kālī'],[135,'krishna_give_v','Kṛṣṇa'],[225,'arjuna_give_phi','Arjuna']]) {
      await slider('axial-rotation',bearing);
      assert.equal(await legend.getAttribute('data-operator'),operator);
      assert.ok((await page.locator('#legend-move').textContent()).includes(alias));
      assert.equal(await legend.getAttribute('data-target'),'','bearing invented Titan approach');
      assert.match(await page.locator('#phase-signature').textContent(),/[ΦV]/);
    }
    await slider('axial-rotation',90);
    assert.equal(await legend.getAttribute('data-seam'),'true');
    await slider('axial-rotation',91);
    assert.equal(await legend.getAttribute('data-seam'),'false','seam retained within same sector');
    for (const [before,after,target] of [[20,30,'equator'],[100,110,'north'],[160,150,'equator'],[80,70,'south']]) {
      await slider('polar-angle',before); await slider('polar-angle',after);
      assert.equal(await legend.getAttribute('data-target'),target);
      assert.equal(await legend.getAttribute('data-motion'),'moving');
      await slider('polar-angle',after,'change');
      assert.equal(await legend.getAttribute('data-motion'),'still');
      assert.equal(await legend.getAttribute('data-target'),'');
    }
    for (const pole of [0,180]) {
      await slider('polar-angle',pole);
      assert.equal(await legend.getAttribute('data-operator'),'');
      assert.match(await page.locator('#legend-move').textContent(),/pole boundary/);
    }
    await page.locator('#centre-button').click();
    assert.match(await page.locator('#legend-direction').textContent(),/Reset.*Viṣṇu/);
    await page.locator('#overlay-toggle').click();
    assert.equal(await legend.getAttribute('data-motion'),'hidden');
    assert.equal(await legend.getAttribute('data-operator'),'');
    await page.locator('#overlay-toggle').click();
    await page.locator('#bearing-button').click();
    await page.evaluate(() => {
      document.querySelector('#kali_take_phi summary').click();
      document.querySelector('#kali_take_v summary').click();
    });
    await page.waitForTimeout(100);
    assert.deepEqual(await page.locator('.bi-equation[open]').evaluateAll(es=>es.map(e=>e.id)),['kali_take_v'], 'latest rule selection lost to queued toggle');
    // Exercise real native keyboard input; rotation may not alter radial quantities.
    await page.locator('#polar-angle').focus();
    await page.keyboard.press('ArrowRight');
    await page.waitForFunction(()=>document.querySelector('#theta-value').textContent==='90.1°');
    const radial = await page.locator('#phi-value').textContent();
    await page.locator('#axial-rotation').focus();
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#phi-value').textContent(), radial);
    const box = await canvas.boundingBox();
    const operatorBeforeOrbit = await legend.getAttribute('data-operator');
    const thetaBeforeOrbit = await canvas.getAttribute('data-theta-degrees');
    await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
    await page.mouse.down(); await page.mouse.move(box.x+box.width/2+75,box.y+box.height/2+40,{steps:8});
    assert.equal(await legend.getAttribute('data-motion'),'camera');
    assert.equal(await legend.getAttribute('data-target'),'');
    await page.mouse.up();
    assert.equal(await canvas.getAttribute('data-theta-degrees'),thetaBeforeOrbit);
    assert.equal(await legend.getAttribute('data-operator'),operatorBeforeOrbit);
    await page.waitForFunction(() => {
      const canvas = document.querySelector('#burrisphere-canvas');
      const state = canvas.dataset.camera;
      window.__biStable = window.__biLastCamera === state ? (window.__biStable || 0)+1 : 0;
      window.__biLastCamera = state;
      return window.__biStable > 4;
    }, null, {polling:150,timeout:15000});
    const camera = await canvas.getAttribute('data-camera');
    await page.setViewportSize({width:1280,height:900});
    await page.waitForTimeout(300);
    assert.equal(await canvas.getAttribute('data-camera'),camera,'resize changed orbit');
    const count = await canvas.getAttribute('data-render-count');
    await page.waitForTimeout(400);
    assert.equal(await canvas.getAttribute('data-render-count'),count,'idle keeps rendering');
    await page.locator('#fullscreen-button').click();
    await page.waitForTimeout(300);
    const fullscreen = await page.evaluate(()=>Boolean(document.fullscreenElement));
    if (fullscreen) {
      await page.locator('#fullscreen-button').click();
      await page.waitForTimeout(300);
      assert.equal(await page.evaluate(()=>Boolean(document.fullscreenElement)),false);
      assert.equal(await page.evaluate(()=>document.activeElement.id),'fullscreen-button');
    } else {
      assert.match(await page.locator('#runtime-status').textContent(),/unavailable or declined/);
    }
    // Explicit denial path leaves the window and native inspector usable.
    await page.evaluate(()=>{document.documentElement.requestFullscreen=()=>Promise.reject(new Error('QA denied'));});
    await page.locator('#fullscreen-button').click();
    await page.waitForFunction(()=>document.querySelector('#runtime-status').textContent.includes('unavailable or declined'));
    await page.locator('#motion-toggle').click();
    await page.waitForTimeout(200);
    assert.equal(await legend.getAttribute('data-target'),'equator');
    await page.locator('#motion-toggle').click();
    assert.equal(await legend.getAttribute('data-motion'),'paused');
    assert.equal(await legend.getAttribute('data-target'),'');
    await page.locator('#motion-toggle').click();
    await page.locator('#polar-angle').focus(); await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#motion-toggle').getAttribute('aria-pressed'),'false');
    // Let the real 12-second itinerary cross the equator and finish once.
    await page.locator('#motion-toggle').click();
    await page.waitForFunction(()=>Number(document.querySelector('#burrisphere-canvas').dataset.thetaDegrees)>105,null,{timeout:15000});
    assert.equal(await legend.getAttribute('data-target'),'north');
    await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
    await page.mouse.down(); await page.mouse.move(box.x+box.width/2+10,box.y+box.height/2+10);
    assert.equal(await legend.getAttribute('data-motion'),'moving','camera masked concurrent itinerary');
    await page.mouse.up();
    await page.screenshot({path:path.join(OUT,'legend-moving.png')});
    await page.waitForFunction(()=>document.querySelector('#motion-toggle').textContent.includes('Replay'),null,{timeout:15000});
    assert.equal(await legend.getAttribute('data-motion'),'still');
    assert.equal(await legend.getAttribute('data-target'),'');
    assert.equal(await legend.getAttribute('data-operator'),'','completed pole retained move');
    await page.locator('#motion-toggle').click();
    await page.waitForTimeout(200);
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.waitForFunction(()=>document.querySelector('#motion-toggle').disabled);
    assert.equal(await legend.getAttribute('data-motion'),'still');
    assert.equal(await legend.getAttribute('data-target'),'');
    await page.emulateMedia({reducedMotion:'no-preference'});
    // Actual context loss, not a simulated success status.
    await canvas.evaluate(el=>el.getContext('webgl2').getExtension('WEBGL_lose_context').loseContext());
    await page.waitForFunction(()=>document.body.dataset.webgl==='lost');
    assert.ok(await page.locator('#webgl-fallback').isVisible());
    assert.ok(await page.locator('.bi-nav a[href="/exit/"]').isVisible());
    await page.locator('#vishnu_preserve summary').click();
    assert.ok(await page.locator('#vishnu_preserve').evaluate(el=>el.open));
    await page.screenshot({path:path.join(OUT,'context-lost.png')});
    results.push({liveMoveAliases:4,titanDirections:4,seamsAndPoles:true,noCameraMove:true,pauseClearsDirection:true,completeClearsDirection:true,reducedMotionClearsDirection:true,concurrentCameraAndItinerary:true,independentCoordinates:true, latestRuleSelection:true, resizePreservesCamera:true, idleRenders:false, fullscreen, denialFallback:true, contextLoss:true});
    await ctx.close();

    for (const mode of ['no-js','reduced']) {
      const {ctx,page} = await context({viewport:{width:320,height:568},javaScriptEnabled:mode!=='no-js',reducedMotion:mode==='reduced'?'reduce':'no-preference'});
      await page.locator('#brahma_create summary').focus(); await page.keyboard.press('Enter');
      assert.ok(await page.locator('#brahma_create').evaluate(el=>el.open));
      if (mode==='reduced') assert.ok(await page.locator('#motion-toggle').isDisabled());
      else assert.ok(await page.locator('#polar-angle').isDisabled());
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
      await page.screenshot({path:path.join(OUT,`${mode}.png`)});
      results.push({mode, staticRules:true,overflow:false});
      await ctx.close();
    }
    assert.deepEqual(errors,[],'page errors');
    assert.deepEqual(external,[],'external resource requests');
    const report={status:'PASS',runtime:require('playwright/package.json').version,results,errors,external};
    fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify(report,null,2));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
