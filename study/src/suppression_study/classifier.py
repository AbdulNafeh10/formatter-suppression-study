"""Classify only complete, reliable four-pass diagnostic correspondence."""

import ast
from collections import Counter

from .matching import MatchError, anchor_diagnostics, same_source_key


def classify(before, after, passes):
    result = {
        "classification": "Ambiguous",
        "matched_diagnostic_identities": [],
        "newly_hidden_count": None,
        "newly_exposed_count": None,
        "underlying_changes": None,
        "matching_errors": [],
    }

    def signature(source):
        return ast.dump(
            ast.parse(source, type_comments=True, feature_version=(3, 11)),
            include_attributes=False,
        )

    if signature(before) != signature(after):
        result.update(
            classification="AST changed",
            explanation="Strict AST equivalence failed; suppression attribution blocked.",
        )
        return result
    anchors = []
    try:
        for source, underlying_name, visible_name in (
            (before, "B_original_underlying", "A_original_visible"),
            (after, "D_formatted_underlying", "C_formatted_visible"),
        ):
            underlying, visible = passes[underlying_name], passes[visible_name]
            if Counter(map(same_source_key, visible)) - Counter(
                map(same_source_key, underlying)
            ):
                raise MatchError(
                    "Visible diagnostics are not a multiset subset of underlying diagnostics"
                )
            visible_keys = set(map(same_source_key, visible))
            mapped = anchor_diagnostics(source, underlying)
            for anchor in mapped.values():
                anchor["visible"] = (
                    same_source_key(anchor["diagnostic"]) in visible_keys
                )
            anchors.append(mapped)
        original, formatted = anchors
        result["anchors"] = {
            "original": list(original.values()),
            "formatted": list(formatted.values()),
        }
        common = sorted(original.keys() & formatted.keys())
        # A path alone is not enough: verify node and token context before matching.
        for identity in common:
            for field in ("node_context", "construct_tokens", "diagnostic_tokens"):
                if original[identity][field] != formatted[identity][field]:
                    raise MatchError(f"Mismatched {field} for {identity}")
        changed_messages = [
            identity
            for identity in common
            if original[identity]["diagnostic"]["message"]
            != formatted[identity]["diagnostic"]["message"]
        ]
        result["matched_diagnostic_identities"] = [
            {
                "identity": identity,
                "original": original[identity],
                "formatted": formatted[identity],
            }
            for identity in common
        ]
        removed, added = sorted(original.keys() - formatted.keys()), sorted(
            formatted.keys() - original.keys()
        )
        result["underlying_changes"] = {
            "removed": [original[key] for key in removed],
            "added": [formatted[key] for key in added],
            "message_changed": changed_messages,
        }
        if removed or added or changed_messages:
            result.update(
                classification="Diagnostic changed",
                explanation="Underlying diagnostic identities or messages differ; no suppression drift attribution.",
            )
            return result
        hidden = exposed = 0
        for pair in result["matched_diagnostic_identities"]:
            was_visible, now_visible = (
                pair["original"]["visible"],
                pair["formatted"]["visible"],
            )
            transition = "preserved"
            if was_visible and not now_visible:
                hidden += 1
                transition = "newly_hidden"
            elif not was_visible and now_visible:
                exposed += 1
                transition = "newly_exposed"
            pair["transition"] = transition
        classification = (
            "Mixed"
            if hidden and exposed
            else (
                "Newly hidden"
                if hidden
                else "Newly exposed" if exposed else "Preserved"
            )
        )
        result.update(
            classification=classification,
            newly_hidden_count=hidden,
            newly_exposed_count=exposed,
            explanation=(
                f"Underlying diagnostics match uniquely ({len(common)}); "
                f"{hidden} newly hidden, {exposed} newly exposed. "
                "Identities use rule, AST path, node and token context, not line equality."
            ),
        )
    except (MatchError, KeyError, TypeError) as exc:
        result["matching_errors"].append(str(exc))
        result["explanation"] = f"Reliable correspondence unavailable: {exc}"
    return result
