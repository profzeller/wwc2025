# Lab 3 — Threat Detection Workflow: Signal vs Noise

## Goal
Learn how security teams decide **what matters** when faced with many alerts — and why most alerts are **not** escalated.

This lab focuses on **reasoning and context**, not tools or memorization.

---

## Scenario
You are part of a small security team monitoring a basic environment.

The system generates many events every day:

- Logins
- Process activity
- Network connections
- File access

Your job is **not** to react to everything.

Your job is to decide:

- What is noise
- What is signal
- What needs more context
- What (rarely) requires escalation

---

## Key Concepts

- **Events → Alerts → Triage → Escalation**
- Signal vs. noise
- Context matters more than volume
- Escalation is a deliberate choice with cost

---

## What You’ll Do
You will use a **web-based Analyst Triage Board** to review a set of synthetic security events.

For each event, you will:

1. **Classify it as one of the following**
   - Noise
   - Signal
   - Needs more context

2. **If it is signal**
   - Decide whether you would escalate  
     - Yes  
     - No  
     - Not yet  
   - Explain your reasoning

3. **Identify missing context**
   - What additional data would help you decide?
   - What would change your mind?

There is no single “correct” answer — your goal is to **justify your decisions clearly**.

---

## Important Guardrails

- All data is **synthetic**
- No real IP addresses, domains, or brands
- Focus on *how* decisions are made, not on “catching” attackers
- Most alerts should be closed during triage

---

## Reflection Questions
Be ready to discuss:

- Which events were easiest to close as noise? Why?
- Which events required the most context?
- Which events did you choose to escalate, and why?
- What single piece of missing information would have changed the most decisions?

---

## Getting Started
This lab runs through the **WWC Lab Hub**.

1. Start the Lab Hub
2. Launch **Lab 3 — Threat Detection Workflow: Signal vs Noise**
3. Review events and begin triage

Your instructor may pause the lab for discussion or group debriefs.

---

## Takeaway
Effective threat detection is not about reacting to every alert.

It is about:

- Understanding context
- Making deliberate decisions
- Knowing when *not* to escalate
