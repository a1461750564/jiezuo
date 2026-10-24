#!/usr/bin/env python3
"""Read-only lookup of Jiezuo's curated references; Python 3.10+, stdlib only.

Independently implemented. Catalog/search concepts informed by UI UX Pro Max;
no upstream engine or database is bundled. See THIRD_PARTY_NOTICES.md.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references" / "reference-catalog.json"
STOP_WORDS = {"a", "an", "and", "for", "in", "of", "the", "to", "with"}


def normalize(value):
    return unicodedata.normalize("NFKC", value).casefold().strip()


def version_number(value):
    if not re.fullmatch(r"v?\d+(?:\.\d+){0,2}", value):
        raise argparse.ArgumentTypeError("版本写成 19、19.2 或 19.2.1；先从项目确认版本，不传依赖范围或 prerelease")
    return tuple(int(v) for v in value.removeprefix("v").split("."))


def padded(value):
    return tuple(value) + (0,) * (3 - len(value))


def contains(text, term):
    if re.search(r"[\u3400-\u9fff]", term):
        return term in text
    return re.search(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", text) is not None


def relevance(entry, query):
    query = normalize(query)
    title = normalize(entry["title"])
    keywords = [normalize(t) for t in entry["keywords"]]
    # Explicit bilingual phrases also match inside an unsegmented Chinese query.
    hits = {term for term in keywords if contains(query, term)}
    tokens = re.findall(r"[a-z0-9]+(?:[.+-][a-z0-9]+)*|[\u3400-\u9fff]+", query)
    for token in tokens:
        if token not in STOP_WORDS and len(token) > 1 and (
            contains(title, token) or any(contains(term, token) for term in keywords)
        ):
            hits.add(token)
    if not hits:
        return 0, []
    # Lexical ranking only: not confidence, quality, or permission to adopt a design.
    score = sum(3 + min(len(term), 12) / 12 for term in hits)
    score += 4 if query in keywords or query == title else 0
    return round(score, 3), sorted(hits)


def applicability(entry, stack, version, variant):
    scope = entry.get("applies_to", {})
    owner = scope.get("stack")
    if stack and owner and stack != owner:
        return None, "stack"
    # A package version belongs only to the explicitly named stack.
    needs_precision = False
    if version and owner and stack == owner:
        actual = padded(version)
        # "19" does not assert 19.0.0; it may denote any installed 19.x release.
        upper = padded(version[:-1] + (version[-1] + 1,)) if len(version) < 3 else None
        minimum = padded(version_number(scope["min_version"])) if scope.get("min_version") else None
        before = padded(version_number(scope["before_version"])) if scope.get("before_version") else None
        if minimum and actual < minimum:
            if upper is None or upper <= minimum:
                return None, "version"
            needs_precision = True
        if before:
            if actual >= before:
                return None, "version"
            if upper and upper > before:
                needs_precision = True
    if variant and scope.get("variant") and variant != scope["variant"]:
        return None, "variant"
    missing = []
    if owner and not stack:
        missing.append("stack")
    bounded = "min_version" in scope or "before_version" in scope
    if bounded and not version:
        missing.append("version")
    if needs_precision:
        missing.append("version-precision")
    if scope.get("variant") and not variant:
        missing.append("variant")
    if missing:
        return {"status": "needs-context", "missing": missing, "scope": scope}, None
    if owner and not bounded:
        return {"status": "check-project-docs", "scope": scope}, None
    return {"status": "within-curated-scope", "scope": scope}, None


def load_catalog():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("entries"), list):
        raise ValueError("目录 schema_version 或 entries 不合法")
    seen = set()
    for entry in data["entries"]:
        for key in ("id", "domain", "title", "keywords", "guidance", "use_when", "avoid_when", "reference", "sources"):
            if not entry.get(key):
                raise ValueError(f"条目 {entry.get('id')} 缺少 {key}")
        if entry["id"] in seen:
            raise ValueError(f"目录 ID 重复：{entry['id']}")
        seen.add(entry["id"])
        reference = entry["reference"].split("#", 1)[0]
        path = (ROOT / reference).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f"条目 {entry['id']} 的本地参考不存在或超出 Skill")
        if any(source not in data["sources"] for source in entry["sources"]):
            raise ValueError(f"条目 {entry['id']} 引用了未知来源")
    return data


def lookup(data, query, domain, stack, version, variant, limit):
    matches, excluded = [], {"stack": 0, "version": 0, "variant": 0}
    for entry in data["entries"]:
        if domain and entry["domain"] != domain:
            continue
        score, terms = relevance(entry, query)
        if score == 0:
            continue
        scope, reason = applicability(entry, stack, version, variant)
        if reason:
            excluded[reason] += 1
            continue
        item = dict(entry)
        item["applicability"] = scope
        item["match"] = {"score": score, "terms": terms}
        item["reference_path"] = str((ROOT / entry["reference"].split("#", 1)[0]).resolve())
        item["sources"] = [{"id": key, **data["sources"][key]} for key in entry["sources"]]
        matches.append(item)
    matches.sort(key=lambda item: (-item["match"]["score"], item["id"]))
    return {
        "status": "matched" if matches else "no-match",
        "query": query,
        "filters": {"domain": domain, "stack": stack, "version": ".".join(map(str, version)) if version else None, "variant": variant},
        "catalog_updated_at": data["updated_at"],
        "total_matches": len(matches),
        "excluded": excluded,
        "results": matches[:limit],
        "note": "相关性不是设计评分或兼容性证明；缺少上下文先核对项目。零命中不生成默认风格、字体或布局。",
    }


def print_text(result):
    print(f"{result['status']} | {result['total_matches']} matches | {result['query']}")
    if not result["results"]:
        print("没有适用命中。核对领域、项目栈、版本与分支，换具体关键词或查对应官方资料；不自动推荐模板。")
    for item in result["results"]:
        print(f"\n[{item['id']}] {item['title']} ({item['domain']})")
        print("适用性：" + json.dumps(item["applicability"], ensure_ascii=False))
        print("参考：" + item["reference_path"] + " | " + item["reference"])
        for key, label in (("guidance", "要点"), ("use_when", "适合"), ("avoid_when", "不适合")):
            print(label + "：" + item[key])
        for source in item["sources"]:
            print("来源：" + source["url"])
        print("命中词：" + "、".join(item["match"]["terms"]))
    print("\n" + result["note"])


def main():
    parser = argparse.ArgumentParser(description="界作离线参考检索：只读精选目录，不联网、不写文件、不执行来源代码")
    parser.add_argument("query", nargs="?", help="具体问题；支持目录中的中文和英文关键词")
    parser.add_argument("--domain", help="限定领域；--list 查看")
    parser.add_argument("--stack", help="明确的项目技术栈；--list 查看，不自动猜测项目")
    parser.add_argument("--version", type=version_number, help="该 stack 的项目版本，例如 19.2、14、5")
    parser.add_argument("--variant", help="app-router/pages-router、radix/base-ui/react-aria、runes/legacy")
    parser.add_argument("--limit", type=int, default=4, help="返回 1–10 条，默认 4")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--list", action="store_true", help="列出实际目录范围")
    args = parser.parse_args()
    try:
        data = load_catalog()
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"目录读取失败：{error}\n")
    domains = sorted({e["domain"] for e in data["entries"]})
    stacks = sorted({e["applies_to"]["stack"] for e in data["entries"] if e.get("applies_to", {}).get("stack")})
    variants = sorted({e["applies_to"]["variant"] for e in data["entries"] if e.get("applies_to", {}).get("variant")})
    if args.list:
        print(json.dumps({"domains": domains, "stacks": stacks, "variants": variants, "entries": len(data["entries"]), "upstream": data["upstream"]}, ensure_ascii=False, indent=2))
        return
    if not args.query or not args.query.strip():
        parser.error("请给具体查询，或用 --list 查看目录")
    if args.domain and args.domain not in domains:
        parser.error("未知 domain；可用：" + ", ".join(domains))
    if args.stack and args.stack not in stacks:
        parser.error("未知 stack；可用：" + ", ".join(stacks))
    if args.variant and args.variant not in variants:
        parser.error("未知 variant；可用：" + ", ".join(variants))
    if args.variant:
        owned_variants = {e["applies_to"]["variant"] for e in data["entries"] if e.get("applies_to", {}).get("stack") == args.stack and e["applies_to"].get("variant")}
        if not args.stack or args.variant not in owned_variants:
            parser.error("--variant 必须属于指定 --stack；用 --list 查看分支，不能把 Router 或组件底层混给其他栈")
    if args.version and not args.stack:
        parser.error("--version 必须与 --stack 一起使用，避免比较错包的版本")
    if not 1 <= args.limit <= 10:
        parser.error("--limit 必须为 1–10")
    result = lookup(data, args.query, args.domain, args.stack, args.version, args.variant, args.limit)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
