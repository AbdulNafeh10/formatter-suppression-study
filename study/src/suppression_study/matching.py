"""Conservative diagnostic identities for the pinned F401/F821/F841 rules."""

import ast
import io
import tokenize


class MatchError(ValueError):
    """Correspondence could not be established without guessing."""


def same_source_key(item):
    """Position is valid as identity only within the SAME source snapshot."""
    return (
        item["code"],
        item["message"],
        item["location"]["row"],
        item["location"]["column"],
        item["end_location"]["row"],
        item["end_location"]["column"],
    )


def diagnostic_span(item, lines):
    points = []
    for name in ("location", "end_location"):
        location = item.get(name, {})
        row, column = location.get("row"), location.get("column")
        if (
            type(row) is not int
            or type(column) is not int
            or not 1 <= row <= len(lines)
            or not 1 <= column <= len(lines[row - 1]) + 1
        ):
            raise MatchError("Out-of-bounds diagnostic coordinates")
        points.append((row, column - 1))
    if points[0] >= points[1]:
        raise MatchError("Empty or reversed diagnostic span")
    return tuple(points)


class SourceIndex:
    def __init__(self, source):
        self.lines = source.split("\n")
        self.tree = ast.parse(source, type_comments=True, feature_version=(3, 11))
        self.nodes = []
        self._walk(self.tree, "$")
        ignored = {
            tokenize.COMMENT,
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.ENDMARKER,
            tokenize.ENCODING,
        }
        self.tokens = [
            token
            for token in tokenize.generate_tokens(io.StringIO(source).readline)
            if token.type not in ignored
        ]

    def _walk(self, node, path):
        if isinstance(node, (ast.Name, ast.alias)):

            def character_column(row, byte_column):
                return len(
                    self.lines[row - 1].encode("utf-8")[:byte_column].decode("utf-8")
                )

            start = (node.lineno, character_column(node.lineno, node.col_offset))
            end = (
                node.end_lineno,
                character_column(node.end_lineno, node.end_col_offset),
            )
            self.nodes.append((path, node, (start, end)))
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                self._walk(value, f"{path}.{field}")
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    if isinstance(child, ast.AST):
                        self._walk(child, f"{path}.{field}[{index}]")

    def tokens_for(self, span):
        overlapping = [t for t in self.tokens if t.start < span[1] and t.end > span[0]]
        if (
            not overlapping
            or overlapping[0].start != span[0]
            or overlapping[-1].end != span[1]
        ):
            raise MatchError(
                "Diagnostic or construct does not align with complete code tokens"
            )
        return [(t.type, t.string) for t in overlapping]

    def anchor(self, diagnostic):
        code = diagnostic.get("code")
        if code not in {"F401", "F821", "F841"}:
            raise MatchError(f"Unsupported diagnostic rule: {code}")
        span = diagnostic_span(diagnostic, self.lines)
        candidates = []
        for path, node, node_span in self.nodes:
            eligible = (
                code == "F401"
                and isinstance(node, ast.alias)
                or code == "F821"
                and isinstance(node, ast.Name)
                and isinstance(node.ctx, ast.Load)
                or code == "F841"
                and isinstance(node, ast.Name)
                and isinstance(node.ctx, ast.Store)
            )
            if eligible and node_span[0] <= span[0] and span[1] <= node_span[1]:
                candidates.append((path, node, node_span))
        if len(candidates) != 1:
            raise MatchError(
                f"Expected one relevant AST anchor, found {len(candidates)}"
            )
        path, node, node_span = candidates[0]
        if isinstance(node, ast.Name) and span != node_span:
            raise MatchError("Name diagnostic does not cover the complete identifier")
        return {
            "identity": f"{code}@{path}",
            "rule": code,
            "ast_path": path,
            "node_context": ast.dump(node, include_attributes=False),
            "construct_tokens": self.tokens_for(node_span),
            "diagnostic_tokens": self.tokens_for(span),
            "source_span": {"start": node_span[0], "end": node_span[1]},
            "diagnostic": diagnostic,
        }


def anchor_diagnostics(source, diagnostics):
    index = SourceIndex(source)
    anchors = {}
    for diagnostic in diagnostics:
        anchor = index.anchor(diagnostic)
        identity = anchor["identity"]
        if identity in anchors:
            raise MatchError(f"Duplicate underlying diagnostic identity: {identity}")
        anchors[identity] = anchor
    return anchors
