# Release Cadence & Growth Loop

A visible monthly release rhythm signals the project is alive — the single biggest factor in adoption decisions. Each release creates a fresh reason to repost without being repetitive.

---

## Monthly Release Schedule

| Month | Version | Theme | Key Feature |
|-------|---------|-------|-------------|
| July 2026 | v0.3.0 | Framework Integrations | Native CrewAI + Haystack integrations |
| August 2026 | v0.4.0 | Observability | Langfuse/Arize Phoenix event export |
| September 2026 | v0.5.0 | Enterprise | Multi-tenant policy engine, RBAC |
| October 2026 | v0.6.0 | Detection | ML-based semantic anomaly detector |
| November 2026 | v0.7.0 | Compliance | SOC 2 mapping, automated audit reports |
| December 2026 | v1.0.0 | Stable | Production-ready GA release |

---

## Per-Release Promotion Checklist

Each release triggers the following actions:

### Day 0 (Release Day)
- [ ] Tag release on GitHub with changelog
- [ ] Publish to PyPI
- [ ] Update README badges (auto via GitHub Action)
- [ ] Post changelog on Dev.to
- [ ] Tweet/post on X with demo GIF
- [ ] Post on LinkedIn with "what's new" summary

### Day 1 (Newsletter Submissions)
- [ ] PyCoder's Weekly (submit via form)
- [ ] Python Weekly (submit via form)
- [ ] tl;dr sec (submit via form)
- [ ] TLDR AI (submit via form)
- [ ] Ben's Bites (submit via form)

### Day 2-3 (Community Engagement)
- [ ] Post on relevant Reddit threads (r/MachineLearning, r/artificial)
- [ ] Comment on relevant HN threads
- [ ] Update open framework issues with "now available in vX.Y"
- [ ] Bump stale PRs with "updated for vX.Y compatibility"

### Day 7 (Follow-up)
- [ ] Check newsletter inclusion
- [ ] Repost on Dev.to with "week 1 adoption numbers"
- [ ] Update comparison page with new features

---

## Newsletter Contact List

| Newsletter | Submission Method | URL |
|-----------|-------------------|-----|
| PyCoder's Weekly | Web form | https://pycoders.com/submissions |
| Python Weekly | Email | pythonweekly@substack.com |
| tl;dr sec | Web form | https://tldrsec.com/contribute |
| TLDR AI | Web form | https://tldr.tech/ai/submit |
| Ben's Bites | Web form | https://news.bensbites.com/submit |
| The Batch (DeepLearning.AI) | Email | thebatch@deeplearning.ai |
| Import AI | Email | jack@jack-clark.net |
| Last Week in AI | GitHub issue | https://github.com/skynettoday/skynet-today |

---

## Metrics to Track Per Release

| Metric | Target (monthly) |
|--------|-----------------|
| PyPI downloads (agent-memory-guard) | +500 |
| PyPI downloads (langchain-agent-memory-guard) | +200 |
| GitHub clones | +400 |
| GitHub stars | +20 |
| Newsletter mentions | 2+ |
| New framework issues/PRs opened by community | 3+ |

---

## Automation

The `update-downloads.yml` GitHub Action already tracks totals daily. Consider adding:
- A `release-announce.yml` workflow that auto-posts to social on tag push
- A monthly reminder issue (via scheduled workflow) to trigger the release checklist
