from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from flask import (
    Blueprint,
    Response,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

assessment_bp = Blueprint("assessment", __name__)

DATA_FILE = Path("data/post_assessment_results.csv")

# QUESTIONS format:
# (prompt, correct_option_letter, options_dict)
QUESTIONS: List[Tuple[str, str, Dict[str, str]]] = [
    # Day 1 — Foundations
    (
        "1) What does the CIA Triad represent in cybersecurity?",
        "A",
        {
            "A": "Confidentiality, Integrity, Availability",
            "B": "Compliance, Inspection, Audit",
            "C": "Cyber, Internet, Access",
            "D": "Control, Identity, Authorization",
        },
    ),
    (
        "2) In a simple model, risk is best described as:",
        "B",
        {
            "A": "How expensive a security tool is",
            "B": "Likelihood × Impact",
            "C": "The number of vulnerabilities found",
            "D": "The amount of data stored",
        },
    ),
    (
        "3) Which option best matches the terms threat and vulnerability?",
        "C",
        {
            "A": "Threat = a weakness; Vulnerability = a person/group that causes harm",
            "B": "Threat = a security control; Vulnerability = a policy",
            "C": "Threat = something that can cause harm; Vulnerability = a weakness that can be exploited",
            "D": "Threat = an incident; Vulnerability = a patch",
        },
    ),
    (
        "4) Which control primarily reduces impact (not likelihood) after something goes wrong?",
        "D",
        {
            "A": "Turning off unused USB ports",
            "B": "Security awareness training",
            "C": "Applying patches quickly",
            "D": "Tested backups with a clear restore process",
        },
    ),
    (
        "5) Which is the best example of good cyber hygiene?",
        "A",
        {
            "A": "Using MFA and keeping systems updated",
            "B": "Sharing one admin account so work is faster",
            "C": "Disabling updates to avoid breaking software",
            "D": "Emailing passwords when someone forgets them",
        },
    ),
    (
        "6) Why are logs valuable even if you think you prevented the attack?",
        "B",
        {
            "A": "Logs guarantee attacks will stop",
            "B": "Logs provide evidence of what happened and help confirm or refute suspicion",
            "C": "Logs replace the need for backups",
            "D": "Logs prevent all insider threats",
        },
    ),
    # Day 2 — Defensive security, detection, response
    (
        "7) Which sequence matches a basic threat detection workflow?",
        "C",
        {
            "A": "Escalation → Alerts → Events → Triage",
            "B": "Triage → Events → Escalation → Alerts",
            "C": "Events → Alerts → Triage → Escalation",
            "D": "Alerts → Events → Escalation → Triage",
        },
    ),
    (
        "8) What best describes the idea of signal vs noise?",
        "A",
        {
            "A": "Signal is meaningful activity; noise is expected/low-value activity that can hide signal",
            "B": "Signal is any alert; noise is anything without an alert",
            "C": "Signal is always malware; noise is always user behavior",
            "D": "Signal is only network traffic; noise is only endpoint activity",
        },
    ),
    (
        "9) Which telemetry source is often most useful when investigating account compromise?",
        "D",
        {
            "A": "Printer error logs",
            "B": "Monitor brightness settings",
            "C": "Disk defragmentation logs only",
            "D": "Authentication/login logs (successes, failures, MFA events)",
        },
    ),
    (
        "10) What is the main purpose of triage in incident detection?",
        "B",
        {
            "A": "To punish users who clicked links",
            "B": "To quickly assess whether an alert is real, important, and needs action",
            "C": "To delete logs to save storage",
            "D": "To immediately rebuild affected systems",
        },
    ),
    (
        "11) During an incident, which role is primarily responsible for documenting actions and timelines?",
        "A",
        {
            "A": "Documentation/communications lead",
            "B": "End user who reported the issue",
            "C": "Attacker emulation lead",
            "D": "Facilities manager",
        },
    ),
    (
        "12) In the first minutes of an incident, which action is generally the best first step?",
        "C",
        {
            "A": "Immediately wipe the system so malware is gone",
            "B": "Post about it publicly so everyone knows",
            "C": "Capture what you know: facts, timestamps, preserve evidence, and follow the response process",
            "D": "Disable all user accounts permanently",
        },
    ),
    (
        "13) Which example is social engineering?",
        "D",
        {
            "A": "A server crashes due to a failed disk",
            "B": "A patch is applied to a browser",
            "C": "A firewall blocks a port",
            "D": "A caller impersonates IT support and pressures someone to reveal a code",
        },
    ),
    (
        "14) Why can MFA fatigue (push bombing) work?",
        "B",
        {
            "A": "It exploits encryption weaknesses in TLS",
            "B": "It pressures the user to approve a prompt out of annoyance, confusion, or urgency",
            "C": "It automatically bypasses all MFA systems without user interaction",
            "D": "It only works if the user has no password",
        },
    ),
    # Day 3 — Safe offense, integration, teaching
    (
        "15) In a beginner course, why do we teach offensive concepts at all?",
        "A",
        {
            "A": "To understand attacker thinking so we can defend better",
            "B": "To encourage students to attack real systems",
            "C": "To replace defensive security topics",
            "D": "To avoid learning about ethics",
        },
    ),
    (
        "16) Which activity is NOT appropriate in a classroom setting?",
        "C",
        {
            "A": "Running labs in a controlled environment you provide",
            "B": "Analyzing scenario-based phishing examples that do not target real organizations",
            "C": "Scanning or attacking real school/business networks without written authorization",
            "D": "Practicing incident response documentation with synthetic data",
        },
    ),
    (
        "17) Which step commonly comes first in a high-level attack chain?",
        "A",
        {
            "A": "Identify / Reconnaissance",
            "B": "Exfiltrate",
            "C": "Persist",
            "D": "Recover",
        },
    ),
    (
        "18) Why are misconfigurations often a major cause of incidents?",
        "D",
        {
            "A": "Misconfigurations only affect availability",
            "B": "Misconfigurations cannot be detected with logs",
            "C": "Misconfigurations are always less severe than CVEs",
            "D": "They can expose systems/data directly through bad defaults or excessive permissions",
        },
    ),
    (
        "19) What is the main goal of a capstone scenario in this workshop?",
        "B",
        {
            "A": "To memorize definitions from frameworks",
            "B": "To integrate concepts (CIA, hygiene, detection, response, safe offense) into one narrative exercise",
            "C": "To require advanced exploitation skills",
            "D": "To replace the need for assessments",
        },
    ),
    (
        "20) Which option best describes a teacher-friendly way to use frameworks (NIST, CIS, NICE)?",
        "C",
        {
            "A": "Teach framework acronyms as the main learning outcome",
            "B": "Avoid frameworks entirely because they are too complex",
            "C": "Translate frameworks into lesson objectives, activities, and lab deliverables",
            "D": "Use frameworks only for legal compliance paperwork",
        },
    ),
]


def _require_admin_token() -> None:
    """
    Require a shared secret token to access admin endpoints.
    Supported methods:
      - Query string: ?token=...
      - Header: Authorization: Bearer <token>
      - Header: X-Admin-Token: <token>
    """
    expected = os.environ.get("ASSESSMENT_ADMIN_TOKEN", "").strip()
    if not expected:
        # Fail closed if token is not configured.
        abort(403)

    provided = (request.args.get("token") or "").strip()

    if not provided:
        auth = (request.headers.get("Authorization") or "").strip()
        if auth.lower().startswith("bearer "):
            provided = auth.split(" ", 1)[1].strip()

    if not provided:
        provided = (request.headers.get("X-Admin-Token") or "").strip()

    if provided != expected:
        abort(403)


@assessment_bp.route("/assessment/post", methods=["GET", "POST"])
def post_assessment():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Name is required.", "error")
            return render_template("post_assessment.html", questions=QUESTIONS)

        answers: List[str] = []
        score = 0

        for idx, (_, correct, options) in enumerate(QUESTIONS):
            field = f"q{idx}"
            ans = request.form.get(field)
            if ans not in options:
                flash("Please answer every question before submitting.", "error")
                return render_template("post_assessment.html", questions=QUESTIONS)
            answers.append(ans)
            if ans == correct:
                score += 1

        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        write_header = not DATA_FILE.exists()

        timestamp = datetime.now(timezone.utc).isoformat()

        with DATA_FILE.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(
                    ["timestamp_utc", "name", "score", "total"]
                    + [f"q{i+1}" for i in range(len(QUESTIONS))]
                )
            writer.writerow([timestamp, name, score, len(QUESTIONS)] + answers)

        return redirect(url_for("assessment.post_assessment_thanks", score=score, total=len(QUESTIONS)))

    return render_template("post_assessment.html", questions=QUESTIONS)


@assessment_bp.route("/assessment/post/thanks")
def post_assessment_thanks():
    score = request.args.get("score")
    total = request.args.get("total")
    return render_template("post_assessment_thanks.html", score=score, total=total)


@assessment_bp.route("/assessment/results")
def assessment_results():
    _require_admin_token()

    rows: List[Dict[str, str]] = []
    headers: List[str] = []

    if DATA_FILE.exists():
        with DATA_FILE.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            for row in reader:
                rows.append(row)

    # Most recent first
    rows.reverse()

    # Provide a convenient CSV download URL that keeps the same token.
    token = request.args.get("token", "")
    csv_url = url_for("assessment.assessment_results_csv", token=token) if token else url_for("assessment.assessment_results_csv")

    return render_template("assessment_results.html", headers=headers, rows=rows, csv_url=csv_url)


@assessment_bp.route("/assessment/results.csv")
def assessment_results_csv():
    _require_admin_token()

    if not DATA_FILE.exists():
        # Return a valid CSV with no rows if empty.
        content = "timestamp_utc,name,score,total\n"
        return Response(content, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=post_assessment_results.csv"})

    content = DATA_FILE.read_text(encoding="utf-8")
    return Response(
        content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=post_assessment_results.csv"},
    )
