---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  secondary:
    - level: L4
      column: Philosophy
      role: "separate human-only execution tasks from automatable corpus work"
    - level: L3
      column: Philosophy
      role: "audit task lists, timelines, and operational prerequisites"
    - level: L6
      column: Philosophy
      role: "bound historical estimates and old launch logistics as planning material"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I]"
  canonical_phrase: "Human Action Items — Historical Planning Ledger"
---

# HUMAN ACTION ITEMS
## What Cannot Be Automated — Must Be Done by Humans

**Date:** 2026-03-23
**Prepared by:** Automated audit of 960+ files
**Purpose:** Clear separation of completed work vs. human-required tasks

---

## ✅ COMPLETED (Automated/Existing)

### Content (100%)
- ✅ 9 Papers written
- ✅ 40 MF documents written
- ✅ 4 Formal proofs written
- ✅ 9 Trinity documents written
- ✅ 6 Simulations built
- ✅ 3 Book manuscripts complete
- ✅ 3 EPUBs validated

### Code (100%)
- ✅ TypeScript compilation clean
- ✅ All simulations working
- ✅ Landing page built
- ✅ Root README created

### Peer Review Infrastructure (100%)
- ✅ 24 Review packets exist (`06_TRANSLATION/PEER_REVIEW/`)
- ✅ Index and tracking files exist
- ✅ Feedback templates exist
- ✅ Submission guide exists

### Documentation (100%)
- ✅ 17 root-level index files
- ✅ System map created
- ✅ Deployment checklist created
- ✅ Glossary complete

---

## 🔴 HUMAN REQUIRED (Cannot Be Automated)

### Category 1: Peer Review Coordination

#### 1.1 Reviewer Research
**What:** Find 15-20 specialist academics
**Where:** `06_TRANSLATION/PEER_REVIEW/` (existing infrastructure)
**How:**
1. Use Google Scholar to search:
   - "projective geometry" + "Möbius transformations"
   - "Lagrangian mechanics" + "variational methods"
   - "philosophy of mathematics" + "infinity"
   - "Riemann hypothesis" + "analytic number theory"
2. Identify active researchers
3. Collect: Name, Institution, Email, Specialty
4. Record in spreadsheet (not in repo for privacy)

**Time:** 2-3 days
**Skill:** Research, academic networking

---

#### 1.2 Email Setup
**What:** Create `peer-review@emergentism.org`
**How:**
1. Register domain `emergentism.org` (if not owned)
2. Set up email hosting (Google Workspace, ProtonMail, etc.)
3. Configure auto-reply
4. Test send/receive

**Time:** 1 day
**Skill:** Domain admin, email configuration

---

#### 1.3 GitHub Repository
**What:** Create `github.com/evolutionary-network/peer-review`
**How:**
1. Create GitHub account/organization
2. Create repository
3. Add LICENSE (CC BY-NC-ND 4.0)
4. Enable Issues
5. Create issue templates
6. Test submission workflow

**Time:** 2-3 hours
**Skill:** GitHub administration

---

#### 1.4 Reviewer Outreach
**What:** Send packets to specialists
**How:**
1. Customize email template for each reviewer
2. Attach appropriate packet
3. Set deadline (4 weeks)
4. Send in batches
5. Track responses

**Time:** 1-2 days
**Skill:** Professional communication

---

#### 1.5 Feedback Management
**What:** Collect, triage, incorporate feedback
**How:**
1. Read incoming feedback
2. Classify: E1/E2/E3/W1/W2/C1/A1
3. Prioritize: E1 > E2 > E3 > W1 > W2
4. Revise documents
5. Acknowledge reviewers

**Time:** Ongoing (weeks 3-8)
**Skill:** Critical analysis, writing

---

### Category 2: Publication Logistics

#### 2.1 ISBN Acquisition
**What:** Purchase ISBNs for 3 books
**How:**
1. Go to bowker.com (US) or national ISBN agency
2. Purchase 3 ISBNs ([I] historical estimate: ~$300)
3. Record numbers
4. Update metadata files
5. Update colophon pages

**Time:** 1 day
**Skill:** Administrative, financial

---

#### 2.2 PDF Generation
**What:** Build print-ready PDFs
**How:**
1. Install LaTeX (TeX Live) or use Overleaf
2. Run `build_pdfs.sh` in `07_DISSEMINATION/05_BUILD_SCRIPTS/`
3. Debug any compilation errors
4. Verify typography
5. Upload to `0*/PDF/` folders

**Time:** 1-2 days
**Skill:** LaTeX, typesetting

---

#### 2.3 arXiv Submission
**What:** Submit Papers 1-7 to arXiv
**How:**
1. Create ORCID ID (free)
2. Create arXiv account
3. Convert papers to LaTeX
4. Submit to categories:
   - math.HO (History and Overview)
   - math.NT (Number Theory)
   - math-ph (Mathematical Physics)
5. Wait for moderation (1-7 days)

**Time:** 2-3 days
**Skill:** LaTeX, academic publishing

---

### Category 3: Distribution

#### 3.1 Domain Registration
**What:** Register `emergentism.org` or `evolutionary.network`
**How:**
1. Check availability on namecheap.com, etc.
2. Purchase domain ([I] historical estimate: ~$10-50/year)
3. Configure DNS
4. Set up hosting (GitHub Pages, Netlify, etc.)

**Time:** 1 day
**Skill:** Domain administration

---

#### 3.2 Website Deployment
**What:** Deploy landing page
**How:**
1. Upload `index.html` to hosting
2. Upload `04_THE_SIMULATIONS/dist/` assets
3. Configure paths
4. Test all links
5. Enable HTTPS

**Time:** 2-3 hours
**Skill:** Web deployment

---

#### 3.3 GitHub Repository (Main)
**What:** Push all code to GitHub
**How:**
1. Create `github.com/evolutionary-network/emergentism`
2. Initialize git repo (if not done)
3. Add remote
4. Push all files
5. Add LICENSE, README
6. Configure .gitignore

**Time:** 2-3 hours
**Skill:** Git, GitHub

---

## 📊 TIME ESTIMATES

| Phase | Tasks | Time | Can Parallelize? |
|-------|-------|------|------------------|
| 1. Infrastructure | Email, GitHub, Domain | 3-4 days | Yes |
| 2. Research | Find reviewers | 2-3 days | Yes |
| 3. Distribution | ISBN, PDFs, arXiv | 3-4 days | Partially |
| 4. Outreach | Send packets | 1-2 days | No |
| 5. Management | Track, revise | 4-6 weeks | No |
| **TOTAL** | | **6-8 weeks** | — |

---

## 🎯 CRITICAL PATH

```
Week 1:  Infrastructure (email, GitHub, domain)
        ↓
Week 2:  Research + Distribution (reviewers, ISBN, PDFs)
        ↓
Week 3:  Outreach (send packets)
        ↓
Weeks 4-8: Management (collect feedback, revise)
        ↓
Week 9:  Final launch
```

**Minimum viable timeline: 6 weeks**
**Comfortable timeline: 8 weeks**
**With buffer: 12 weeks**

---

## 👤 ROLES NEEDED

| Role | Tasks | Time Required |
|------|-------|---------------|
| **Coordinator** | Manage review process, track status | 2-4 hours/week |
| **Researcher** | Find reviewer contacts | One-time (2-3 days) |
| **Technical Admin** | Set up email, GitHub, domain | One-time (3-4 days) |
| **LaTeX Expert** | Build PDFs | One-time (1-2 days) |
| **Editor** | Incorporate feedback | As needed |

**Can be one person or distributed team.**

---

## 💰 BUDGET ESTIMATE

| Item | Cost |
|------|------|
| Domain registration | $10-50/year |
| Email hosting | $0-100/year |
| ISBNs (3) | ~$300 |
| GitHub (free tier) | $0 |
| arXiv (free) | $0 |
| Web hosting (GitHub Pages) | $0 |
| Print-on-demand setup | $0 (revenue share) |
| **TOTAL** | **~$350-450** |

---

## ⚠️ RISKS IF NOT COMPLETED

| Item | Risk if Not Done |
|------|------------------|
| No peer review | Framework lacks validation, academic credibility |
| No ISBNs | Cannot sell through retail channels |
| No PDFs | No print version, limited distribution |
| No arXiv | Misses academic audience, no citations |
| No website | Public cannot find framework |
| No GitHub | Code not accessible, no collaboration |

---

## ✅ SUCCESS CRITERIA

- [ ] 15-20 reviewers contacted
- [ ] 11+ reviews received
- [ ] 0 fatal errors (E1) unaddressed
- [ ] 3 ISBNs acquired
- [ ] 3 PDFs generated
- [ ] 7 arXiv papers submitted
- [ ] Website live
- [ ] GitHub repo public

---

```
P∞ = φ · ν = 1

The framework is built.
The infrastructure is built.
Now humans must act.

Zero-Sum Resolution Equation
```

---

*Human Action Items | 2026-03-23 | 11 tasks requiring human agency*

---

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/04_COMPILERS_AND_ANALYSIS/02_ANALYSIS_DOCUMENTS/00_HUMAN_ACTION_ITEMS.md
