"""
Day 9 - Task 3: Email Validation System
========================================
Uses sets to maintain valid email domains, validate addresses,
track unique registrations, and query by domain using set operations.

Author: Sehar Andleeb
Internship: Xeven Solutions - AI Engineering Internship 2026
Mentor: Mubashir Sir (Sr. Machine Learning Engineer)
"""

from __future__ import annotations

import re


# ─── Constants ────────────────────────────────────────────────────────────────
VALID_DOMAINS: frozenset[str] = frozenset({
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "icloud.com", "protonmail.com", "live.com",
    # Pakistani / corporate examples
    "xeven.com", "nust.edu.pk", "lums.edu.pk", "pu.edu.pk",
})

# Simple but effective RFC-5321-inspired pattern
_EMAIL_REGEX: re.Pattern[str] = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


# ─── Validation helpers ───────────────────────────────────────────────────────

def has_valid_format(email: str) -> bool:
    """Check whether the email string matches a valid format pattern.

    Args:
        email: Raw email string to test.

    Returns:
        True if the format is acceptable, False otherwise.
    """
    return bool(_EMAIL_REGEX.match(email.strip()))


def extract_domain(email: str) -> str:
    """Return the domain portion of an email address.

    Args:
        email: A properly formatted email address.

    Returns:
        Domain string (e.g. 'gmail.com').

    Raises:
        ValueError: If the email contains no '@' symbol.
    """
    if "@" not in email:
        raise ValueError(f"No '@' symbol found in: {email!r}")
    return email.split("@", maxsplit=1)[1].strip().lower()


def validate_email(
    email: str,
    valid_domains: frozenset[str]
) -> dict[str, bool | str]:
    """Full validation check: format + domain allowlist membership.

    Args:
        email: The email address to validate.
        valid_domains: frozenset of accepted domain strings.

    Returns:
        A dict with keys 'email', 'format_ok', 'domain_ok', 'is_valid'.
    """
    email = email.strip().lower()
    format_ok = has_valid_format(email)

    domain_ok = False
    if format_ok:
        try:
            domain = extract_domain(email)
            domain_ok = domain in valid_domains   # O(1) set lookup
        except ValueError:
            domain_ok = False

    return {
        "email":     email,
        "format_ok": format_ok,
        "domain_ok": domain_ok,
        "is_valid":  format_ok and domain_ok,
    }


# ─── Registry class ───────────────────────────────────────────────────────────

class EmailRegistry:
    """Track unique registered email addresses using a set.

    Attributes:
        _registered: Internal set ensuring O(1) duplicate detection.
        _valid_domains: frozenset of accepted domains for this registry.
    """

    def __init__(self, valid_domains: frozenset[str]) -> None:
        """Initialise an empty registry.

        Args:
            valid_domains: Domains allowed for registration.
        """
        self._registered: set[str] = set()
        self._valid_domains: frozenset[str] = valid_domains

    # ── Mutation ──────────────────────────────────────────────────────────────

    def register(self, email: str) -> str:
        """Attempt to register an email address.

        Args:
            email: The email to add.

        Returns:
            A human-readable status string.
        """
        email = email.strip().lower()
        result = validate_email(email, self._valid_domains)

        if not result["is_valid"]:
            reason = "invalid format" if not result["format_ok"] else "domain not allowed"
            return f"    {email:<35}  rejected  ({reason})"

        if email in self._registered:        # O(1) lookup
            return f"     {email:<35}  duplicate (already registered)"

        self._registered.add(email)
        return f"    {email:<35}  registered"

    def bulk_register(self, emails: list[str]) -> list[str]:
        """Register multiple emails at once and return status lines.

        Args:
            emails: List of email strings.

        Returns:
            List of status strings, one per email.
        """
        return [self.register(e) for e in emails]

    # ── Query ─────────────────────────────────────────────────────────────────

    def emails_from_domain(self, domain: str) -> set[str]:
        """Return all registered emails whose domain matches exactly.

        Args:
            domain: e.g. 'gmail.com'

        Returns:
            Set of matching email addresses.
        """
        return {e for e in self._registered if e.endswith(f"@{domain}")}

    def emails_from_domains(self, domains: set[str]) -> set[str]:
        """Return emails whose domains are in the supplied set.

        Uses a set expression — a mini-intersection between domains.

        Args:
            domains: Set of domain strings to match against.

        Returns:
            Set of matching email addresses.
        """
        return {e for e in self._registered
                if extract_domain(e) in domains}

    def domain_counts(self) -> dict[str, int]:
        """Count registrations per domain, sorted descending.

        Returns:
            Ordered dict of domain → count.
        """
        counts: dict[str, int] = {}
        for email in self._registered:
            domain = extract_domain(email)
            counts[domain] = counts.get(domain, 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))

    # ── Comparison between two registries ─────────────────────────────────────

    def compare(self, other: "EmailRegistry") -> dict[str, set[str]]:
        """Set-operation comparison between this registry and another.

        Args:
            other: Another EmailRegistry instance.

        Returns:
            Dict with keys 'common', 'only_self', 'only_other', 'all'.
        """
        a = self._registered
        b = other._registered
        return {
            "common":     a & b,      # intersection
            "only_self":  a - b,      # difference: in self but not other
            "only_other": b - a,      # difference: in other but not self
            "all":        a | b,      # union
        }

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def count(self) -> int:
        """Number of unique registered emails."""
        return len(self._registered)

    @property
    def all_emails(self) -> frozenset[str]:
        """Immutable snapshot of registered emails."""
        return frozenset(self._registered)


# ─── Display helpers ──────────────────────────────────────────────────────────

def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'─' * 58}")
    print(f"  {title}")
    print(f"{'─' * 58}")


def display_domain_counts(registry: EmailRegistry) -> None:
    """Print a small bar chart of emails per domain.

    Args:
        registry: The EmailRegistry to inspect.
    """
    counts = registry.domain_counts()
    print_section(" Registrations per Domain")
    for domain, cnt in counts.items():
        bar = "▪" * cnt
        print(f"  {domain:<25}  {cnt:>2}  {bar}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point: demonstrate the full email validation workflow."""

    print("=" * 58)
    print("   Day 9 – Task 3: Email Validation System")
    print("=" * 58)

    # ── 1. Standalone validation demo ─────────────────────────────────────────
    print_section("🔍 Standalone Validation Checks")
    test_emails = [
        "sehar.andleeb@gmail.com",     # valid
        "mubashir@xeven.com",          # valid corporate
        "ali.khan@nust.edu.pk",        # valid university
        "invalid-email",               # no @ → bad format
        "user@",                       # incomplete domain
        "user@unknown-domain.xyz",     # format ok, domain not in allowlist
        "SEHAR@GMAIL.COM",             # uppercase (normalised to lower)
        "double@@gmail.com",           # bad format
        "user@yahoo.com",              # valid
    ]

    for raw in test_emails:
        result = validate_email(raw, VALID_DOMAINS)
        fmt_mark = "✔" if result["format_ok"] else "✘"
        dom_mark = "✔" if result["domain_ok"]  else "✘"
        valid_tag = "VALID  " if result["is_valid"] else "INVALID"
        print(f"  [{valid_tag}]  fmt:{fmt_mark}  dom:{dom_mark}  {result['email']}")

    # ── 2. Build a main registry with valid + invalid + duplicate entries ─────
    print_section(" Registering Users into Main Registry")
    registry_a = EmailRegistry(VALID_DOMAINS)

    emails_to_register = [
        "sehar.andleeb@gmail.com",
        "fatima.malik@yahoo.com",
        "ali.khan@nust.edu.pk",
        "mubashir@xeven.com",
        "hamza@protonmail.com",
        "zara@outlook.com",
        "sehar.andleeb@gmail.com",    # duplicate — should be caught
        "test@fake-domain.io",        # domain not allowed
        "badformat.com",              # no @
        "nadia@lums.edu.pk",
        "omer@gmail.com",
        "hira@yahoo.com",
        "bilal@xeven.com",
        "omer@gmail.com",             # duplicate
    ]

    statuses = registry_a.bulk_register(emails_to_register)
    for status in statuses:
        print(status)

    print(f"\n  Registry A total unique registrations: {registry_a.count}")

    # ── 3. Domain query using set operations ──────────────────────────────────
    print_section("🔎 Domain-Based Queries (set operations)")

    gmail_users = registry_a.emails_from_domain("gmail.com")
    print(f"  Gmail users      : {sorted(gmail_users)}")

    pak_edu_users = registry_a.emails_from_domains({"nust.edu.pk", "lums.edu.pk", "pu.edu.pk"})
    print(f"  .edu.pk users    : {sorted(pak_edu_users)}")

    xeven_users = registry_a.emails_from_domain("xeven.com")
    print(f"  Xeven users      : {sorted(xeven_users)}")

    # ── 4. Domain distribution chart ──────────────────────────────────────────
    display_domain_counts(registry_a)

    # ── 5. Compare two registries using set operations ─────────────────────────
    print_section("⚖️  Registry Comparison (A vs B) — Set Operations")
    registry_b = EmailRegistry(VALID_DOMAINS)
    b_emails = [
        "sehar.andleeb@gmail.com",   # common with A
        "ali.khan@nust.edu.pk",      # common with A
        "new.user@protonmail.com",   # only in B
        "another@icloud.com",        # only in B
        "hira@yahoo.com",            # common with A
    ]
    for e in b_emails:
        registry_b.register(e)

    comparison = registry_a.compare(registry_b)
    print(f"  Registry A count   : {registry_a.count}")
    print(f"  Registry B count   : {registry_b.count}")
    print(f"  Common (A ∩ B)     : {len(comparison['common'])}  → {sorted(comparison['common'])}")
    print(f"  Only in A (A - B)  : {len(comparison['only_self'])}  → {sorted(comparison['only_self'])}")
    print(f"  Only in B (B - A)  : {len(comparison['only_other'])}  → {sorted(comparison['only_other'])}")
    print(f"  Total unique (A ∪ B): {len(comparison['all'])}")

    # ── 6. frozenset usage: immutable domain snapshot ─────────────────────────
    print_section("🔒 frozenset — Immutable Domain Snapshot")
    snapshot: frozenset[str] = registry_a.all_emails
    print(f"  Snapshot type     : {type(snapshot)}")
    print(f"  Snapshot size     : {len(snapshot)}")
    print("  Attempting to add to snapshot ...")
    try:
        snapshot.add("new@gmail.com")   # type: ignore[attr-defined]
    except AttributeError as exc:
        print(f"   AttributeError caught → {exc}")

    print("\n Task 3 complete.\n")


if __name__ == "__main__":
    main()
