#!/usr/bin/env python3
"""Extract exported function, class, and HTTP route signatures from Python and TypeScript files.

Usage:
    python3 scripts/extract-signatures.py <file-or-directory>
"""

from __future__ import annotations

import ast
import json
import pathlib
import re
import sys
from typing import Any

TS_EXPORT_RE = re.compile(
    r"^\s*export\s+(?:async\s+)?(?:function|class|interface|type|const)\s+"
    r"([A-Za-z0-9_]+)\s*([^\n{;]*)",
    re.MULTILINE,
)

ROUTE_RE = re.compile(
    r"\b(?:app|router|fastify)\.(get|post|put|patch|delete)\s*\(\s*['\"`]([^'\"`]+)['\"`]",
    re.IGNORECASE,
)


def extract_python_signatures(path: pathlib.Path) -> list[dict[str, Any]]:
    """Parse Python AST to extract public classes and functions with type annotations."""
    source = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return [{"kind": "syntax_error", "line": exc.lineno, "error": str(exc)}]

    items: list[dict[str, Any]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            args = [
                f"{arg.arg}: {ast.unparse(arg.annotation)}"
                if arg.annotation
                else arg.arg
                for arg in node.args.args
            ]
            returns = ast.unparse(node.returns) if node.returns else "Any"
            prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
            items.append(
                {
                    "kind": "function",
                    "name": node.name,
                    "line": node.lineno,
                    "signature": f"{prefix} {node.name}({', '.join(args)}) -> {returns}",
                    "docstring": (ast.get_docstring(node) or "").splitlines()[0:1],
                }
            )
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            items.append(
                {
                    "kind": "class",
                    "name": node.name,
                    "line": node.lineno,
                    "signature": f"class {node.name}",
                    "docstring": (ast.get_docstring(node) or "").splitlines()[0:1],
                }
            )
    return items


def extract_ts_signatures(path: pathlib.Path) -> list[dict[str, Any]]:
    """Extract exported symbols and HTTP route registrations from TypeScript/JavaScript files."""
    source = path.read_text(encoding="utf-8", errors="replace")
    items: list[dict[str, Any]] = []

    for match in ROUTE_RE.finditer(source):
        method, route_path = match.group(1).upper(), match.group(2)
        line = source.count("\n", 0, match.start()) + 1
        items.append(
            {
                "kind": "http_route",
                "name": f"{method} {route_path}",
                "line": line,
                "signature": f"{method} {route_path}",
            }
        )

    for match in TS_EXPORT_RE.finditer(source):
        name, rest = match.group(1), match.group(2).strip()
        line = source.count("\n", 0, match.start()) + 1
        items.append(
            {
                "kind": "export",
                "name": name,
                "line": line,
                "signature": f"export {name} {rest}".strip(),
            }
        )
    return items


def scan_target(target: pathlib.Path) -> dict[str, list[dict[str, Any]]]:
    results: dict[str, list[dict[str, Any]]] = {}
    files = [target] if target.is_file() else sorted(target.rglob("*"))
    for file_path in files:
        if any(
            part in {"node_modules", ".git", "dist", "build", "__pycache__", ".venv"}
            for part in file_path.parts
        ):
            continue
        if file_path.suffix == ".py":
            sigs = extract_python_signatures(file_path)
            if sigs:
                results[str(file_path)] = sigs
        elif file_path.suffix in {".ts", ".tsx", ".js", ".mjs"}:
            sigs = extract_ts_signatures(file_path)
            if sigs:
                results[str(file_path)] = sigs
    return results


def main() -> int:
    target_arg = sys.argv[1] if len(sys.argv) > 1 else "."
    target = pathlib.Path(target_arg)
    if not target.exists():
        print(f"Error: path '{target}' does not exist.", file=sys.stderr)
        return 1

    extracted = scan_target(target)
    print(json.dumps(extracted, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
