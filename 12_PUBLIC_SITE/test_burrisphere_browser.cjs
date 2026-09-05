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
    await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
    await page.mouse.down(); await page.mouse.move(box.x+box.width/2+75,box.y+box.height/2+40,{steps:8}); await page.mouse.up();
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
    await page.locator('#polar-angle').focus(); await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#motion-toggle').getAttribute('aria-pressed'),'false');
    // Actual context loss, not a simulated success status.
    await canvas.evaluate(el=>el.getContext('webgl2').getExtension('WEBGL_lose_context').loseContext());
    await page.waitForFunction(()=>document.body.dataset.webgl==='lost');
    assert.ok(await page.locator('#webgl-fallback').isVisible());
    assert.ok(await page.locator('.bi-nav a[href="/exit/"]').isVisible());
    await page.locator('#vishnu_preserve summary').click();
    assert.ok(await page.locator('#vishnu_preserve').evaluate(el=>el.open));
    await page.screenshot({path:path.join(OUT,'context-lost.png')});
    results.push({independentCoordinates:true, latestRuleSelection:true, resizePreservesCamera:true, idleRenders:false, fullscreen, denialFallback:true, contextLoss:true});
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
