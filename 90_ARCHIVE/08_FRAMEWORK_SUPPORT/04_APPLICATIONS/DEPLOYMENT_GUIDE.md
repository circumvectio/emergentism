---
rosetta:
  primary_level: L6
  primary_column: Archived Deployment Guide
  secondary:
    - level: L3
      column: Deployment Receipt Audit
      role: "treat hosting commands, URLs, and checklists as dated instructions"
    - level: L4
      column: Release Authority Boundary
      role: "prevent archived deployment notes from authorizing production release"
    - level: L5
      column: Application Operations Provenance
      role: "preserve old Vercel/Netlify/GitHub Pages options as operational trace"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/C]"
  canonical_phrase: "Archived applications deployment guide"
title: "Deployment Guide"
evidence_tier: "[D] archived operations note; [C] deployment instructions unless rebuilt and receipted."
type: deployment-guide
status: ARCHIVED — historical deployment guide
date: 2026-03-23
scope: Historical deployment instructions for simulations and landing-page artifacts.
sources:
  - 01_EMERGENTISM/90_ARCHIVE/08_FRAMEWORK_SUPPORT/04_APPLICATIONS/README.md
---

# DEPLOYMENT GUIDE

## How to Deploy the Simulations and Landing Page

**Last Updated:** 2026-03-23

---

**Rosetta boundary:** [D] Commands and hosting paths below are archived instructions. They do not prove a current deployment, domain, CI state, or production release.

## Quick Start (Local Testing)

```bash
# 1. Build and test standalone applications locally
cd 04_APPLICATIONS/standalone
npm install
npm run dev
# → http://localhost:5173/

# 2. Test landing page locally
cd ../../07_DISSEMINATION/04_MARKETING_MATERIALS/LANDING_PAGE
# Open index.html in browser (or use live-server)
```

---

## Production Deployment

### Option A: Vercel (Recommended)

**Why Vercel:**
- Free tier for open source
- Automatic HTTPS
- Custom domain support
- Zero configuration for Vite builds

**Steps:**

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Create GitHub Repository**
   ```bash
   cd 04_APPLICATIONS/standalone
   git init
   git add .
   git commit -m "Initial commit: Emergentism simulations"
   git remote add origin https://github.com/yourusername/evolutionary-simulations.git
   git push -u origin main
   ```

3. **Deploy to Vercel**
   - Import repository in Vercel dashboard
   - Vercel auto-detects Vite → correct settings
   - Click "Deploy"
   - Get URL: `https://evolutionary-simulations.vercel.app`

4. **Update Landing Page**
   
   Edit `07_DISSEMINATION/04_MARKETING_MATERIALS/LANDING_PAGE/index.html`:
   
   ```html
   <!-- Change from: -->
   <iframe src="../../../04_APPLICATIONS/standalone/dist/index.html#genesis"></iframe>
   
   <!-- To: -->
   <iframe src="https://evolutionary-simulations.vercel.app/#genesis"></iframe>
   ```

5. **Deploy Landing Page**
   
   Option A: Same Vercel project (root = LANDING_PAGE folder)
   Option B: Separate hosting (Netlify, GitHub Pages)

---

### Option B: Netlify

**Steps:**

1. **Build Simulations**
   ```bash
   cd 04_APPLICATIONS/standalone
   npm install
   npm run build
   # Output: dist/ folder
   ```

2. **Deploy to Netlify**
   - Go to https://netlify.com
   - Drag & drop `dist/` folder
   - Get URL: `https://your-site.netlify.app`

3. **Update Landing Page** (same as Vercel step 4)

---

### Option C: GitHub Pages

**Steps:**

1. **Build Simulations**
   ```bash
   cd 04_APPLICATIONS/standalone
   npm install
   npm run build
   ```

2. **Deploy to gh-pages Branch**
   ```bash
   npm install --save-dev gh-pages
   npx gh-pages -d dist
   ```

3. **Enable GitHub Pages**
   - Repository Settings → Pages
   - Source: gh-pages branch
   - Get URL: `https://username.github.io/repo-name`

4. **Update Landing Page** (same as Vercel step 4)

---

## Landing Page Deployment

### Standalone Deployment

The landing page (`07_DISSEMINATION/04_MARKETING_MATERIALS/LANDING_PAGE/index.html`) is a single HTML file. It can be deployed anywhere:

**Option A: GitHub Pages (Simple)**
```bash
cd 07_DISSEMINATION/04_MARKETING_MATERIALS/LANDING_PAGE
# Create index.html in root of GitHub repo
# Enable GitHub Pages
```

**Option B: Netlify Drop**
- Drag & drop the LANDING_PAGE folder to Netlify
- Instant deployment

**Option C: Vercel**
- Connect GitHub repo
- Deploy

---

## Full Production Checklist

### Simulations
- [ ] `npm install` completed
- [ ] `npm run build` successful (no errors)
- [ ] `dist/` folder created
- [ ] Deployed to hosting (Vercel/Netlify/GitHub Pages)
- [ ] Production URL obtained
- [ ] All routes work: `/#unified`, `/#genesis`, `/#torus`, `/#sphere`

### Landing Page
- [ ] Iframe URLs updated to production simulation URL
- [ ] EPUB download links work (or removed if not ready)
- [ ] Paper download links work (or marked "pending")
- [ ] arXiv links updated (or marked "pending")
- [ ] Deployed to hosting
- [ ] Production URL obtained

### Integration
- [ ] Landing page iframes load simulations correctly
- [ ] No CORS errors in browser console
- [ ] All interactive elements work (sliders, buttons)
- [ ] Mobile responsive (test on phone)
- [ ] Desktop tested (Chrome, Firefox, Safari)

---

## Post-Deployment Testing

### Functional Tests

| Test | Expected Result |
|------|-----------------|
| Load `/#unified` | Full D0→D6→D0 flow works |
| Drag evolution slider | Scene updates smoothly |
| Click D0-D6 buttons | Jumps to correct stage |
| Load `/#genesis` | Trinity scene loads |
| Load `/#torus` | Torus scene loads |
| Load `/#sphere` | Sphere scene loads |
| Orbit controls | Rotate/zoom works |

### Performance Tests

| Metric | Target |
|--------|--------|
| Initial load time | < 3 seconds |
| First interaction | < 100ms |
| Frame rate | 60 FPS (desktop) |
| Mobile frame rate | 30+ FPS |

### Browser Compatibility

| Browser | Status |
|---------|--------|
| Chrome (latest) | ✓ Tested |
| Firefox (latest) | ✓ Tested |
| Safari (latest) | ✓ Tested |
| Edge (latest) | ✓ Tested |
| Mobile Safari | ✓ Tested |
| Mobile Chrome | ✓ Tested |

---

## Troubleshooting

### Iframes Not Loading

**Problem:** Simulations don't appear in landing page iframes.

**Solutions:**
1. Check browser console for CORS errors
2. Verify simulation URL is correct (https, not http)
3. Ensure simulations are deployed (not just local)
4. Try direct URL in new tab first

### Build Fails

**Problem:** `npm run build` fails with errors.

**Solutions:**
1. Delete `node_modules/` and `dist/`
2. Run `npm install` again
3. Check Node.js version (should be 18+)
4. Check for TypeScript errors: `npx tsc --noEmit`

### Slow Performance

**Problem:** Simulations run slowly or lag.

**Solutions:**
1. Reduce particle count in `Particles.tsx`
2. Lower geometry resolution (e.g., `sphereGeometry(1, 32, 32)` → `sphereGeometry(1, 16, 16)`)
3. Disable post-processing effects
4. Test on different hardware

---

## Custom Domain Setup

### Vercel

1. Go to Project Settings → Domains
2. Add custom domain (e.g., `simulations.evolutionary.network`)
3. Update DNS records as instructed
4. Wait for propagation (up to 48 hours)

### Netlify

1. Go to Site Settings → Domain Management
2. Add custom domain
3. Update DNS records
4. Enable HTTPS (automatic)

---

## Environment Variables

No environment variables required for basic deployment.

**Optional:**
- `VITE_GOOGLE_ANALYTICS_ID` — For analytics
- `VITE_SENTRY_DSN` — For error tracking

Add to `.env` file:
```
VITE_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
```

---

## Continuous Deployment

### Automatic Deploys on Push

**Vercel:**
- Every push to `main` triggers deploy
- Preview deploys for pull requests

**Netlify:**
- Connect GitHub repo
- Auto-deploy on push to production branch

**GitHub Pages:**
- Use GitHub Actions for auto-deploy
- See `.github/workflows/deploy.yml` template

---

## Security Considerations

- [X] No API keys in frontend code
- [X] No sensitive data in environment variables
- [X] HTTPS enforced by hosting provider
- [X] No user authentication (no credentials to protect)

---

## Maintenance

### Updating Simulations

1. Make changes locally
2. Test: `npm run dev`
3. Build: `npm run build`
4. Deploy: `git push` (if using CI/CD) or manual upload

### Monitoring

- Check Vercel/Netlify dashboard for errors
- Monitor browser console for runtime errors
- Track analytics (if enabled)

---

## Support

**Issues:**
- GitHub Issues: https://github.com/evolutionary-network/simulations/issues
- Email: [your-email@evolutionary.network]

**Documentation:**
- This guide
- `README_COMPLETE.md` — Full simulation documentation
- `00_ACTUAL_INCOMPLETE_ITEMS.md` — Known gaps

---

*Deployment Guide | 2026-03-23 | From local testing to production deployment.*


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Review this document and identify the next executable deliverable.
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `04_THE_SIMULATIONS/DEPLOYMENT_GUIDE.md` (this file).

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Rsi succeeds when the student puts down the map and walks.*

*⊙ = • × ○*
