#!/usr/bin/env python3
"""
Pre-deploy supply-chain gate for 12_PUBLIC_SITE.

Checks:
1. No external or protocol-relative static HTML/CSS/SVG/XML/Web App Manifest
   resource declarations, including declarative refresh/speculation rules and
   recursively linked local document/style surfaces (security gate;
   runtime-generated JavaScript is intentionally out of scope)
2. All internal hrefs resolve to existing files
3. No orphan pages (every public page has at least one inbound link)
4. Required assets present where referenced
5. Basic HTML well-formedness (DOCTYPE, html/head/body tags)
6. Tier-marker presence on doctrine pages
7. Operators route uses current evidence tier markers
8. Public reading bundle is wired
9. Generated library pages preserve the generator chrome contract
10. Historical-withholding bytes, redirects, and search boundary agree
11. Deployment publication boundary excludes source/control/runtime files
12. Current/provisional public semantics match their source contract
13. Claim cards, lifecycles, and barred-claim policy match source contracts
14. The public book and its build manifest match deterministic source hashes
15. The frozen-library manifest names the current reader deterministically
16. The contact-limited public lifecycle has zero unclassified artifacts

Exit 0 if all checks pass, 1 if any fail.
"""

import base64
import gzip
import json
import hashlib
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import unquote_to_bytes, urljoin, urlparse
from xml.etree import ElementTree

try:
    import tinycss2
except ImportError:  # The gate fails closed below if CSS cannot be parsed.
    tinycss2 = None

TINYCSS2_REQUIRED_VERSION = "1.5.1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
WITHHELD_REGISTRY_PATH = os.path.join(BASE_DIR, "withheld-routes.json")
ERRORS = []
WARNINGS = []


def load_withheld_registry():
    with open(WITHHELD_REGISTRY_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def withheld_artifact_paths():
    return {item["artifact"] for item in load_withheld_registry()["artifacts"]}

def error(msg):
    ERRORS.append(msg)
    print(f"  ✗ {msg}")

def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠ {msg}")

def ok(msg):
    print(f"  ✓ {msg}")

def get_public_html_files():
    files = []
    withheld = withheld_artifact_paths()
    patterns = load_vercelignore_patterns() or []
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [
            d for d in dirs if d not in {"node_modules", "vendor", ".git", ".vercel", ".next",
                                          "90_ARCHIVE", "_archive", "_STAGING_COMPASS_RESTRUCTURE"}
        ]
        for f in filenames:
            # ``.htm`` is a standard static HTML suffix.  XHTML is collected
            # through the XML-aware route below so CDATA and namespace rules
            # cannot be weakened by HTMLParser's recovery behavior.
            if f.lower().endswith((".html", ".htm")):
                rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
                if (
                    not rel.startswith("partials/")
                    and rel.replace(os.sep, "/") not in withheld
                    and not is_vercel_ignored(rel, patterns)
                ):
                    files.append(rel)
    return sorted(files)

def read_file(rel_path):
    path = os.path.join(BASE_DIR, rel_path)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def read_svg_payload(rel_path):
    """Read an SVG or bounded, validated gzip-compressed SVG payload."""

    if not rel_path.lower().endswith(".svgz"):
        return read_file(rel_path)
    path = os.path.join(BASE_DIR, rel_path)
    try:
        with gzip.open(path, "rb") as fh:
            payload = fh.read(MAX_SVGZ_BYTES + 1)
    except OSError as exc:
        raise ValueError(f"cannot decompress SVGZ ({exc})") from exc
    if len(payload) > MAX_SVGZ_BYTES:
        raise ValueError(f"SVGZ exceeds {MAX_SVGZ_BYTES} decompressed bytes")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"SVGZ is not UTF-8 ({exc})") from exc

class StartTagCollector(HTMLParser):
    """Collect parsed declarations without mistaking raw-text payloads for markup."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.style_blocks = []
        self.script_blocks = []
        self._raw_tag = None
        self._raw_attrs = None
        self._raw_parts = None

    def _finish_raw_block(self):
        if self._raw_tag is None:
            return
        body = "".join(self._raw_parts)
        if self._raw_tag == "style":
            self.style_blocks.append(body)
        elif self._raw_tag == "script":
            self.script_blocks.append((self._raw_attrs, body))
        self._raw_tag = None
        self._raw_attrs = None
        self._raw_parts = None

    def handle_starttag(self, tag, attrs):
        # Preserve duplicates in source order. Browsers use the first duplicate
        # resource attribute; collapsing to a dict would let a later local value
        # hide an earlier external one from this security gate.
        self.tags.append(
            (tag.lower(), [(name.lower(), value or "") for name, value in attrs if name])
        )
        lowered = tag.lower()
        local_tag = lowered.rsplit(":", 1)[-1]
        if local_tag in {"style", "script"}:
            self._raw_tag = local_tag
            self._raw_attrs = [(name.lower(), value or "") for name, value in attrs if name]
            self._raw_parts = []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag.lower().rsplit(":", 1)[-1] in {"style", "script"}:
            self._finish_raw_block()

    def handle_data(self, data):
        if self._raw_parts is not None:
            self._raw_parts.append(data)

    def handle_endtag(self, tag):
        if tag.lower().rsplit(":", 1)[-1] == self._raw_tag:
            self._finish_raw_block()

    def close(self):
        if self._raw_parts is not None and self.rawdata:
            # HTMLParser leaves unclosed raw-text content in ``rawdata`` rather
            # than dispatching handle_data at EOF. Consume it explicitly.
            self._raw_parts.append(self.rawdata)
            self.rawdata = ""
        super().close()
        # Browsers treat unclosed raw-text elements as continuing through EOF.
        # Preserve that behavior so malformed markup cannot hide a declaration.
        self._finish_raw_block()


def extract_start_tags(body):
    parser = StartTagCollector()
    parser.feed(body)
    parser.close()
    return parser.tags


def extract_style_blocks(body):
    parser = StartTagCollector()
    parser.feed(body)
    parser.close()
    return parser.style_blocks


def extract_speculation_rule_blocks(body):
    """Return inline JSON rules that make browser prefetches declaratively."""

    parser = StartTagCollector()
    parser.feed(body)
    parser.close()
    return [
        source
        for attrs, source in parser.script_blocks
        if any(
            name == "type" and value.strip().lower() == "speculationrules"
            for name, value in attrs
        )
    ]


def attribute_values(attrs, name):
    return [value for attr, value in attrs if attr == name]


def resource_attribute_values(attrs, name):
    """Return an SVG resource attribute without trusting its prefix spelling."""

    if name == "xlink:href":
        return [
            value
            for attr, value in attrs
            if ":" in attr and attr.rsplit(":", 1)[-1] == "href"
        ]
    return attribute_values(attrs, name)


def extract_hrefs(body):
    return [
        value
        for tag, attrs in extract_start_tags(body)
        if tag.rsplit(":", 1)[-1] != "base"
        for value in attribute_values(attrs, "href")
        if value
    ]


def extract_base_href(body):
    for tag, attrs in extract_start_tags(body):
        if tag.rsplit(":", 1)[-1] == "base":
            hrefs = attribute_values(attrs, "href")
            if hrefs:
                return hrefs[0]
    return None


def base_href_values(body):
    return [
        value
        for tag, attrs in extract_start_tags(body)
        if tag.rsplit(":", 1)[-1] == "base"
        for value in attribute_values(attrs, "href")
        if value
    ]


def normalized_url_reference(value):
    """Normalize browser-tolerated backslashes before classifying a URL."""

    return value.strip().replace("\\", "/")


def decoded_local_url_path(path):
    """Decode one URL path exactly once before filesystem containment checks."""

    try:
        decoded = unquote_to_bytes(path).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"URL path is not valid UTF-8 ({exc})") from exc
    if "\x00" in decoded:
        raise ValueError("URL path contains a NUL byte")
    # Browsers tolerate backslashes as path separators.  Decode before this
    # normalization so %5c cannot hide a path traversal from the root check.
    return decoded.replace("\\", "/")


def is_external_resource(value):
    normalized = normalized_url_reference(value)
    parsed = urlparse(normalized)
    # WHATWG URL resolution treats every two-or-more-slash prefix as a
    # network-path reference, including /// and //// forms that urlparse
    # otherwise reports as a local path.
    return (
        normalized.startswith("//")
        or bool(parsed.netloc)
        or (
            bool(parsed.scheme)
            and parsed.scheme.lower() not in {"blob", "data"}
        )
    )


def resolve_base_route(from_file, base_href):
    """Resolve one local ``<base href>`` in public-site route space.

    An external or protocol-relative base changes every otherwise local relative
    URL into a network load. It is a fail-closed condition, not an out-of-scope
    link.
    """

    normalized = normalized_url_reference(base_href)
    parsed_reference = urlparse(normalized)
    if normalized.startswith("//") or parsed_reference.scheme or parsed_reference.netloc:
        return None, "external"
    route = urljoin("/" + from_file.replace(os.sep, "/"), normalized)
    parsed_route = urlparse(route)
    if parsed_route.scheme or parsed_route.netloc:
        return None, "external"
    try:
        route_path = decoded_local_url_path(parsed_route.path or "/")
    except ValueError:
        return None, "invalid"
    target = os.path.normpath(os.path.join(BASE_DIR, route_path.lstrip("/")))
    if not is_inside_public_root(target):
        return None, "escape"
    return route_path or "/", "local"


def base_href_issues(from_file, body):
    """Return unsafe base elements independently of ordinary href validation."""

    issues = []
    for value in base_href_values(body):
        _, state = resolve_base_route(from_file, value)
        if state == "external":
            issues.append(("base", value))
        elif state == "escape":
            issues.append(("base outside public-site root", value))
        elif state == "invalid":
            issues.append(("invalid base URL", value))
    return issues


def srcset_candidates(value):
    """Return URL candidates from a srcset without treating descriptors as URLs."""

    candidates = []
    for candidate in value.split(","):
        url = candidate.strip().split(maxsplit=1)[0] if candidate.strip() else ""
        if url:
            candidates.append(url)
    return candidates


RESOURCE_LINK_RELS = {
    "apple-touch-icon",
    "apple-touch-icon-precomposed",
    "apple-touch-startup-image",
    "compression-dictionary",
    "dictionary",
    "dns-prefetch",
    "icon",
    "manifest",
    "mask-icon",
    "modulepreload",
    "pingback",
    "preconnect",
    "prefetch",
    "preload",
    "prerender",
    "serviceworker",
    "stylesheet",
}
RESOURCE_ATTRIBUTES = {
    "altglyph": ("href", "xlink:href"),
    "audio": ("href", "src", "xlink:href"),
    "bgsound": ("src",),
    "body": ("background",),
    "color-profile": ("href", "xlink:href"),
    "cursor": ("href", "xlink:href"),
    "embed": ("src",),
    "feimage": ("href", "xlink:href"),
    "fencedframe": ("src",),
    "filter": ("href", "xlink:href"),
    "font-face-uri": ("href", "xlink:href"),
    "foreignobject": ("href", "xlink:href"),
    "frame": ("src",),
    "glyphref": ("href", "xlink:href"),
    "iframe": ("href", "src", "xlink:href"),
    "img": ("src", "srcset"),
    "image": ("href", "xlink:href"),
    "input": ("src",),
    "lineargradient": ("href", "xlink:href"),
    "marker": ("href", "xlink:href"),
    "model": ("environmentmap", "src"),
    "mpath": ("href", "xlink:href"),
    "object": ("data",),
    "pattern": ("href", "xlink:href"),
    "portal": ("src",),
    "radialgradient": ("href", "xlink:href"),
    "script": ("href", "src", "xlink:href"),
    "source": ("src", "srcset"),
    "table": ("background",),
    "td": ("background",),
    "textpath": ("href", "xlink:href"),
    "tfoot": ("background",),
    "thead": ("background",),
    "track": ("src",),
    "tr": ("background",),
    "tbody": ("background",),
    "tref": ("href", "xlink:href"),
    "th": ("background",),
    "use": ("href", "xlink:href"),
    "video": ("href", "poster", "src", "xlink:href"),
}
AUTOMATIC_ATTRIBUTION_TAGS = set(RESOURCE_ATTRIBUTES) | {"a", "area", "link"}
PING_RESOURCE_TAGS = {"a", "area"}
SVG_URL_PRESENTATION_ATTRIBUTES = {
    "clip-path",
    "color-profile",
    "cursor",
    "fill",
    "filter",
    "marker-end",
    "marker-mid",
    "marker-start",
    "marker",
    "mask",
    "shape-inside",
    "shape-subtract",
    "stroke",
}
# A URL-bearing SMIL target can turn a local SVG resource reference into a
# later network request.  The public projection has no approved use for this
# capability, so the SVG pass rejects it rather than trying to emulate timing,
# target inheritance, and CSS/SVG animation precedence.
SMIL_URL_TARGET_ATTRIBUTES = (
    {attribute for attributes in RESOURCE_ATTRIBUTES.values() for attribute in attributes}
    | SVG_URL_PRESENTATION_ATTRIBUTES
    | {"background-image", "style"}
)
SMIL_ANIMATION_ELEMENTS = {"animate", "animatemotion", "animatetransform", "set"}
AUTOMATIC_DOCUMENT_LINK_RELS = {"prefetch", "prerender"}
DOCUMENT_NAVIGATION_SUFFIXES = (
    ".html",
    ".htm",
    ".xhtml",
    ".xht",
    ".xml",
    ".svg",
    ".svgz",
    ".rss",
    ".atom",
    ".rdf",
    ".xsl",
    ".xslt",
)
MANIFEST_DOCUMENT_CANDIDATE_LABELS = {
    "manifest start_url",
    "manifest shortcut URL",
    "manifest share target",
    "manifest file handler",
    "manifest protocol handler",
    "manifest related application",
}
CSS_STRING_URL_FUNCTIONS = {
    "-webkit-cross-fade",
    "-webkit-image-set",
    "cross-fade",
    "image",
    "image-set",
}
MAX_EMBEDDED_DOCUMENT_DEPTH = 4
MAX_DATA_DOCUMENT_BYTES = 1_000_000
MAX_SVGZ_BYTES = 1_000_000
REJECTED_DATA_DOCUMENT_MEDIA_TYPES = {
    "application/javascript",
    "application/xml",
    "application/xhtml+xml",
    "text/javascript",
    "text/css",
    "text/html",
    "text/xml",
}
SVG_DATA_MEDIA_TYPE = "image/svg+xml"
XML_STYLESHEET_PI_RE = re.compile(r"<\?xml-stylesheet\b[\s\S]*?\?>", re.IGNORECASE)
XML_UNSAFE_DECLARATION_RE = re.compile(r"<!\s*(?:doctype|entity)\b", re.IGNORECASE)
SVG_ROOT_START_RE = re.compile(r"<(?:[A-Za-z_][\w.-]*:)?svg(?:\s|/?>)", re.IGNORECASE)
# A prefixed XHTML root is XML syntax even without an XML declaration.  Keep
# this separate from ordinary ``<html>`` so permissive text/html pages are not
# accidentally forced through the XML parser.
PREFIXED_XHTML_ROOT_START_RE = re.compile(
    r"<[A-Za-z_][\w.-]*:html(?:\s|/?>)", re.IGNORECASE
)
XML_BASE_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"


def css_resource_values(css, *, declaration_context=False):
    """Return CSS resource URLs after standards-aware tokenization.

    CSS escapes can turn apparently local text into an external URL.  The
    parser decodes those escapes before classification; malformed URL-bearing
    syntax fails closed rather than being silently ignored.
    """

    if tinycss2 is None:
        raise ValueError(
            "tinycss2 is unavailable; install "
            "09_TOOLS/01_SCRIPTS/requirements.txt"
        )
    if getattr(tinycss2, "__version__", None) != TINYCSS2_REQUIRED_VERSION:
        raise ValueError(
            f"tinycss2=={TINYCSS2_REQUIRED_VERSION} is required; found "
            f"{getattr(tinycss2, '__version__', 'unknown')}"
        )

    parser = tinycss2.parse_declaration_list if declaration_context else tinycss2.parse_stylesheet
    tokens = parser(css, skip_comments=True, skip_whitespace=True)
    values = []
    errors = []

    def significant(items):
        return [
            item
            for item in items or []
            if item.type not in {"comment", "whitespace"}
        ]

    def function_url_value(token):
        arguments = significant(token.arguments)
        if len(arguments) == 1 and arguments[0].type in {"string", "url"}:
            return arguments[0].value
        errors.append(f"unparseable url() expression: {tinycss2.serialize(token.arguments)!r}")
        return None

    def visit(items):
        for token in items or []:
            token_type = token.type
            if token_type == "error":
                errors.append(f"CSS parse error: {getattr(token, 'message', 'unknown error')}")
            elif token_type == "url":
                values.append(token.value)
            elif token_type == "function":
                name = token.lower_name
                if name == "url":
                    value = function_url_value(token)
                    if value is not None:
                        values.append(value)
                else:
                    if name in CSS_STRING_URL_FUNCTIONS:
                        values.extend(
                            argument.value
                            for argument in significant(token.arguments)
                            if argument.type == "string"
                        )
                    visit(token.arguments)
            elif token_type == "at-rule":
                if token.lower_at_keyword == "import":
                    prelude = significant(token.prelude)
                    if not prelude:
                        errors.append("unparseable @import expression")
                    else:
                        source = prelude[0]
                        if source.type in {"string", "url"}:
                            values.append(source.value)
                        elif source.type == "function" and source.lower_name == "url":
                            value = function_url_value(source)
                            if value is not None:
                                values.append(value)
                        else:
                            errors.append(
                                "unparseable @import expression: "
                                f"{tinycss2.serialize(token.prelude)!r}"
                            )
                else:
                    visit(getattr(token, "prelude", None))
                    visit(getattr(token, "content", None))
            elif token_type == "declaration":
                visit(token.value)
            else:
                visit(getattr(token, "content", None))

    visit(tokens)
    if errors:
        raise ValueError("; ".join(errors))
    return values


def css_resource_candidates(css, label, *, declaration_context=False):
    return [
        (label, value)
        for value in css_resource_values(css, declaration_context=declaration_context)
    ]


def css_value_resource_candidates(value, label):
    """Parse one CSS-valued presentation attribute as a declaration value."""

    return css_resource_candidates(
        f"resource: {value}", label, declaration_context=True
    )


def css_import_values(css):
    """Return only top-level stylesheet imports after full CSS validation."""

    # Reuse the complete parser first so malformed nested CSS fails closed.
    css_resource_values(css)
    tokens = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
    values = []
    for token in tokens:
        if token.type != "at-rule" or token.lower_at_keyword != "import":
            continue
        prelude = [
            item
            for item in token.prelude or []
            if item.type not in {"comment", "whitespace"}
        ]
        if not prelude:
            raise ValueError("unparseable @import expression")
        source = prelude[0]
        if source.type in {"string", "url"}:
            values.append(source.value)
            continue
        if source.type == "function" and source.lower_name == "url":
            arguments = [
                item
                for item in source.arguments or []
                if item.type not in {"comment", "whitespace"}
            ]
            if len(arguments) == 1 and arguments[0].type in {"string", "url"}:
                values.append(arguments[0].value)
                continue
        raise ValueError(
            "unparseable @import expression: "
            f"{tinycss2.serialize(token.prelude)!r}"
        )
    return values


def html_resource_candidates(body):
    """Return static browser resource URLs without collapsing duplicate attrs."""

    candidates = []
    for tag, attrs in extract_start_tags(body):
        resource_tag = tag.rsplit(":", 1)[-1]
        if resource_tag == "link":
            rels = {
                token.lower()
                for value in attribute_values(attrs, "rel")
                for token in value.split()
            }
            if rels.intersection(RESOURCE_LINK_RELS):
                candidates.extend(("link", value) for value in attribute_values(attrs, "href"))
            if "preload" in rels and any(
                value.strip().lower() == "image"
                for value in attribute_values(attrs, "as")
            ):
                for value in attribute_values(attrs, "imagesrcset"):
                    candidates.extend(
                        ("link imagesrcset", candidate)
                        for candidate in srcset_candidates(value)
                    )
        elif resource_tag in RESOURCE_ATTRIBUTES:
            for attr in RESOURCE_ATTRIBUTES[resource_tag]:
                for value in resource_attribute_values(attrs, attr):
                    if attr == "srcset":
                        candidates.extend(
                            (f"{resource_tag} srcset", candidate)
                            for candidate in srcset_candidates(value)
                        )
                    else:
                        candidates.append((resource_tag, value))
        if resource_tag in AUTOMATIC_ATTRIBUTION_TAGS:
            for value in attribute_values(attrs, "attributionsrc"):
                candidates.extend(
                    (f"{resource_tag} attributionsrc", candidate)
                    for candidate in value.split()
                )
        if resource_tag in PING_RESOURCE_TAGS:
            for value in attribute_values(attrs, "ping"):
                candidates.extend(
                    (f"{resource_tag} ping", candidate)
                    for candidate in value.split()
                )
        for attr in SVG_URL_PRESENTATION_ATTRIBUTES:
            for value in attribute_values(attrs, attr):
                candidates.extend(css_value_resource_candidates(value, f"{resource_tag} {attr}"))
    return candidates


def xml_base_issues(body):
    """Reject XML bases in HTML/SVG markup rather than misresolving descendants.

    XML Base applies recursively and is materially different from HTML's
    ``<base>`` element.  This site does not need it; rejecting it is a
    deterministic fail-closed rule for inline SVG and embedded XML.
    """

    return [
        ("xml:base", value)
        for _, attrs in extract_start_tags(body)
        for attr, value in attrs
        if attr == "xml:base" or (":" in attr and attr.rsplit(":", 1)[-1] == "base")
    ]


def meta_refresh_target(content):
    """Return one refresh URL, or ``None`` when no URL was declared."""

    _, separator, target = content.partition(";")
    if not separator:
        return None
    target = target.strip()
    if target.lower().startswith("url"):
        _, equals, target = target.partition("=")
        if not equals:
            raise ValueError("unparseable meta refresh URL")
    target = target.strip().strip("\"'")
    if not target:
        raise ValueError("empty meta refresh URL")
    return target


def meta_refresh_candidates(body):
    """Return declarative refresh navigation targets from ``meta`` elements."""

    candidates = []
    for tag, attrs in extract_start_tags(body):
        if tag.rsplit(":", 1)[-1] != "meta" or not any(
            value.strip().lower() == "refresh"
            for value in attribute_values(attrs, "http-equiv")
        ):
            continue
        for content in attribute_values(attrs, "content"):
            target = meta_refresh_target(content)
            if target is None:
                continue
            candidates.append(("meta refresh", target))
    return candidates


def speculation_rule_source_candidates(source):
    """Return URLs from one declarative browser speculation-rules JSON block.

    ``href_matches`` can select URLs from the live document at runtime.  The
    public projection has no use for it, so the gate refuses it rather than
    guessing whether its future matches stay in the public root.
    """

    try:
        rules = json.loads(source)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid speculationrules JSON ({exc.msg})") from exc
    if not isinstance(rules, dict):
        raise ValueError("speculationrules JSON root must be an object")
    candidates = []
    for action in ("prefetch", "prerender"):
        entries = rules.get(action, [])
        if not isinstance(entries, list):
            raise ValueError(f"speculationrules {action} must be a list")
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"speculationrules {action} entry must be an object")
            source = entry.get("source")
            if source is not None and source != "list":
                raise ValueError("document-selected speculationrules are not permitted")
            if "where" in entry or "urls" not in entry:
                raise ValueError("only explicit speculationrules URL lists are permitted")
            urls = entry["urls"]
            if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
                raise ValueError(f"speculationrules {action} urls must be a list of strings")
            candidates.extend((f"speculationrules {action}", url) for url in urls)
    return candidates


def speculation_rule_candidates(body):
    """Return URLs from declarative browser speculation rules in HTML."""

    candidates = []
    for source in extract_speculation_rule_blocks(body):
        candidates.extend(speculation_rule_source_candidates(source))
    return candidates


def html_static_resource_candidates(body):
    """Return every local/external static URL declaration carried by HTML/CSS."""

    candidates = list(html_resource_candidates(body))
    candidates.extend(meta_refresh_candidates(body))
    candidates.extend(speculation_rule_candidates(body))
    for tag, attrs in extract_start_tags(body):
        for value in attribute_values(attrs, "style"):
            candidates.extend(
                css_resource_candidates(value, f"{tag} inline style", declaration_context=True)
            )
    for css in extract_style_blocks(body):
        candidates.extend(css_resource_candidates(css, "style"))
    return candidates


def embedded_srcdoc_values(body):
    return [
        value
        for tag, attrs in extract_start_tags(body)
        if tag.rsplit(":", 1)[-1] == "iframe"
        for value in attribute_values(attrs, "srcdoc")
        if value
    ]


def data_document_payload(value):
    """Return a textual data-document payload, or ``None`` for ordinary data.

    A data URL is local only until its decoded HTML/CSS/SVG is interpreted.
    HTML and CSS data documents are prohibited so dynamic nested syntax cannot
    evade this static gate; SVG payloads are decoded and checked recursively
    because the public site intentionally uses local SVG data icons.
    """

    normalized = normalized_url_reference(value)
    if not normalized.lower().startswith("data:"):
        return None
    header, separator, encoded = normalized[5:].partition(",")
    if not separator:
        return "invalid", "data URL has no payload separator"
    parts = [part.strip() for part in header.split(";")]
    media_type = parts[0].lower() if parts and parts[0] else "text/plain"
    is_rejected_xml = media_type.endswith("+xml") and media_type != SVG_DATA_MEDIA_TYPE
    if (
        media_type not in REJECTED_DATA_DOCUMENT_MEDIA_TYPES | {SVG_DATA_MEDIA_TYPE}
        and not is_rejected_xml
    ):
        return None
    try:
        if any(part.lower() == "base64" for part in parts[1:]):
            payload = base64.b64decode(encoded, validate=True)
        else:
            payload = unquote_to_bytes(encoded)
    except (ValueError, UnicodeError) as exc:
        return "invalid", f"cannot decode {media_type} data URL ({exc})"
    if len(payload) > MAX_DATA_DOCUMENT_BYTES:
        return "invalid", f"{media_type} data URL exceeds {MAX_DATA_DOCUMENT_BYTES} bytes"
    try:
        return media_type, payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        return "invalid", f"cannot decode {media_type} data URL as UTF-8 ({exc})"


def get_public_css_files():
    files = []
    patterns = load_vercelignore_patterns() or []
    excluded_dirs = {
        "node_modules", "vendor", ".git", ".vercel", ".next", "90_ARCHIVE", "_archive",
        "_STAGING_COMPASS_RESTRUCTURE",
    }
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [directory for directory in dirs if directory not in excluded_dirs]
        for filename in filenames:
            if filename.lower().endswith(".css"):
                rel = os.path.relpath(os.path.join(root, filename), BASE_DIR)
                if not is_vercel_ignored(rel, patterns):
                    files.append(rel)
    return sorted(files)


def get_public_svg_files():
    """Return every deployable SVG, regardless of filename case."""

    files = []
    patterns = load_vercelignore_patterns() or []
    excluded_dirs = {
        "node_modules", "vendor", ".git", ".vercel", ".next", "90_ARCHIVE", "_archive",
        "_STAGING_COMPASS_RESTRUCTURE",
    }
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [directory for directory in dirs if directory not in excluded_dirs]
        for filename in filenames:
            if filename.lower().endswith((".svg", ".svgz")):
                rel = os.path.relpath(os.path.join(root, filename), BASE_DIR)
                if not is_vercel_ignored(rel, patterns):
                    files.append(rel)
    return sorted(files)


def get_public_xml_files():
    """Return non-SVG XML assets for XML-base and PI safety checks."""

    files = []
    patterns = load_vercelignore_patterns() or []
    excluded_dirs = {
        "node_modules", "vendor", ".git", ".vercel", ".next", "90_ARCHIVE", "_archive",
        "_STAGING_COMPASS_RESTRUCTURE",
    }
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [directory for directory in dirs if directory not in excluded_dirs]
        for filename in filenames:
            if filename.lower().endswith(
                (".xml", ".xhtml", ".xht", ".rss", ".atom", ".rdf", ".xsl", ".xslt")
            ):
                rel = os.path.relpath(os.path.join(root, filename), BASE_DIR)
                if not is_vercel_ignored(rel, patterns):
                    files.append(rel)
    return sorted(files)


def get_public_webmanifest_files():
    """Return deployed Web App Manifest candidates, including common manifest.json."""

    files = []
    patterns = load_vercelignore_patterns() or []
    excluded_dirs = {
        "node_modules", "vendor", ".git", ".vercel", ".next", "90_ARCHIVE", "_archive",
        "_STAGING_COMPASS_RESTRUCTURE",
    }
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [directory for directory in dirs if directory not in excluded_dirs]
        for filename in filenames:
            lowered = filename.lower()
            if lowered.endswith(".webmanifest") or lowered == "manifest.json":
                rel = os.path.relpath(os.path.join(root, filename), BASE_DIR)
                if not is_vercel_ignored(rel, patterns):
                    files.append(rel)
    return sorted(files)


def xml_name_parts(name):
    """Return the namespace URI and local name from ElementTree's expanded name."""

    # ``parse_xml_document`` retains comments so CSS hidden inside an XHTML
    # style comment cannot disappear before validation.  Comments have a
    # callable ElementTree tag rather than an expanded XML name.
    if not isinstance(name, str):
        return "", ""
    if name.startswith("{"):
        namespace, _, local = name[1:].partition("}")
        return namespace, local.lower()
    return "", name.rsplit(":", 1)[-1].lower()


def parse_xml_document(payload, label):
    """Parse XML with a small fail-closed preflight for unsafe declarations."""

    if XML_UNSAFE_DECLARATION_RE.search(payload):
        raise ValueError(f"{label} contains a prohibited XML declaration")
    try:
        parser = ElementTree.XMLParser(
            target=ElementTree.TreeBuilder(insert_comments=True)
        )
        return ElementTree.fromstring(payload, parser=parser)
    except ElementTree.ParseError as exc:
        raise ValueError(f"{label} is not well-formed XML ({exc})") from exc


def xml_payload_kind(payload, label):
    """Classify an extensionless payload as SVG/XML only when it looks XML-like."""

    candidate = payload.lstrip("\ufeff \t\r\n")
    while candidate.startswith("<!--"):
        end = candidate.find("-->")
        if end < 0:
            raise ValueError(f"{label} has an unclosed leading XML comment")
        candidate = candidate[end + 3 :].lstrip(" \t\r\n")
    looks_like_xml_svg = (
        candidate.lower().startswith("<?xml")
        or re.match(r"<!DOCTYPE\s+svg\b", candidate, re.IGNORECASE)
        or SVG_ROOT_START_RE.match(candidate)
        or PREFIXED_XHTML_ROOT_START_RE.match(candidate)
        or (
            candidate.startswith("<?")
            and (XML_STYLESHEET_PI_RE.search(candidate) or SVG_ROOT_START_RE.search(candidate))
        )
    )
    if not looks_like_xml_svg:
        return None
    root = parse_xml_document(payload, label)
    root_name = xml_name_parts(root.tag)[1]
    if root_name == "svg":
        return "svg"
    if root_name == "html":
        return "html"
    return "xml"


def xml_base_attribute_values(element):
    return [
        value
        for attr, value in element.attrib.items()
        if xml_name_parts(attr) == (XML_BASE_NAMESPACE, "base")
    ]


def xml_plain_attribute_values(element, name):
    return [
        value
        for attr, value in element.attrib.items()
        for namespace, local in [xml_name_parts(attr)]
        if not namespace and local == name
    ]


def xml_plain_attributes(element):
    return {
        local: value
        for attr, value in element.attrib.items()
        for namespace, local in [xml_name_parts(attr)]
        if not namespace
    }


def svg_srcdoc_values(root):
    return [
        value
        for element in root.iter()
        if xml_name_parts(element.tag)[1] == "iframe"
        for value in xml_plain_attribute_values(element, "srcdoc")
        if value
    ]


def svg_resource_candidates(payload, label):
    """Return SVG resource declarations using namespace-aware XML parsing."""

    root = parse_xml_document(payload, label)
    _, root_name = xml_name_parts(root.tag)
    if root_name != "svg":
        raise ValueError(f"{label} root is not an SVG element")

    candidates = []
    issues = []
    if XML_STYLESHEET_PI_RE.search(payload):
        issues.append(("prohibited SVG XML stylesheet", "xml-stylesheet"))

    for element in root.iter():
        _, tag = xml_name_parts(element.tag)
        plain_attributes = xml_plain_attributes(element)
        for value in xml_base_attribute_values(element):
            # Correctly resolving nested XML Base chains is unnecessary here:
            # public SVG has no approved XML Base use, so reject all of them.
            issues.append(("xml:base", value))

        if tag in SMIL_ANIMATION_ELEMENTS:
            target_attribute = plain_attributes.get("attributename", "").strip().lower()
            target_attribute = target_attribute.rsplit(":", 1)[-1]
            if target_attribute in SMIL_URL_TARGET_ATTRIBUTES:
                issues.append(
                    ("prohibited SVG SMIL URL animation", f"{tag} {target_attribute}")
                )

        if tag == "base":
            for value in xml_plain_attribute_values(element, "href"):
                # HTML base semantics inside foreignObject affect a nested
                # document. Public SVG has no approved use, so do not attempt
                # cross-namespace base-resolution replay here.
                issues.append(("prohibited SVG foreign HTML base", value))

        if tag == "meta" and plain_attributes.get("http-equiv", "").strip().lower() == "refresh":
            for content in xml_plain_attribute_values(element, "content"):
                target = meta_refresh_target(content)
                if target is not None:
                    candidates.append(("meta refresh", target))

        if (
            tag == "script"
            and plain_attributes.get("type", "").strip().lower() == "speculationrules"
        ):
            candidates.extend(speculation_rule_source_candidates(element.text or ""))

        for attr in RESOURCE_ATTRIBUTES.get(tag, ()):
            for qualified_attr, value in element.attrib.items():
                namespace, local = xml_name_parts(qualified_attr)
                if (
                    (attr == "xlink:href" and namespace == XLINK_NAMESPACE and local == "href")
                    or (attr != "xlink:href" and not namespace and local == attr)
                ):
                    if attr == "srcset":
                        candidates.extend(
                            (f"{tag} srcset", candidate)
                            for candidate in srcset_candidates(value)
                        )
                    else:
                        candidates.append((tag, value))

        if tag in AUTOMATIC_ATTRIBUTION_TAGS:
            for qualified_attr, value in element.attrib.items():
                namespace, local = xml_name_parts(qualified_attr)
                if not namespace and local == "attributionsrc":
                    candidates.extend(
                        (f"{tag} attributionsrc", candidate)
                        for candidate in value.split()
                    )
        if tag in PING_RESOURCE_TAGS:
            for qualified_attr, value in element.attrib.items():
                namespace, local = xml_name_parts(qualified_attr)
                if not namespace and local == "ping":
                    candidates.extend(
                        (f"{tag} ping", candidate)
                        for candidate in value.split()
                    )

        if tag == "link":
            local_attributes = {
                local: value
                for qualified_attr, value in element.attrib.items()
                for namespace, local in [xml_name_parts(qualified_attr)]
                if not namespace
            }
            rels = set(local_attributes.get("rel", "").lower().split())
            if rels.intersection(RESOURCE_LINK_RELS):
                if "href" in local_attributes:
                    candidates.append(("link", local_attributes["href"]))
            if (
                "preload" in rels
                and local_attributes.get("as", "").strip().lower() == "image"
                and "imagesrcset" in local_attributes
            ):
                candidates.extend(
                    ("link imagesrcset", candidate)
                    for candidate in srcset_candidates(local_attributes["imagesrcset"])
                )

        for attr in SVG_URL_PRESENTATION_ATTRIBUTES:
            for qualified_attr, value in element.attrib.items():
                namespace, local = xml_name_parts(qualified_attr)
                if not namespace and local == attr:
                    candidates.extend(css_value_resource_candidates(value, f"{tag} {attr}"))

        for qualified_attr, value in element.attrib.items():
            namespace, local = xml_name_parts(qualified_attr)
            if not namespace and local == "style":
                candidates.extend(
                    css_resource_candidates(value, f"{tag} inline style", declaration_context=True)
                )
        if tag == "style" and element.text:
            candidates.extend(css_resource_candidates(element.text, "svg style"))
    return candidates, issues


def svg_external_resource_references(payload, from_file, *, depth=0, label="SVG"):
    candidates, issues = svg_resource_candidates(payload, label)
    found = list(issues)
    found.extend(
        (candidate_label, value)
        for candidate_label, value in candidates
        if value and is_external_resource(value)
    )
    found.extend(data_document_external_references(candidates, from_file, depth=depth))
    root = parse_xml_document(payload, label)
    for srcdoc in svg_srcdoc_values(root):
        if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
            found.append(("unverifiable SVG iframe srcdoc", "nested-document depth exceeded"))
            continue
        found.extend(
            (f"SVG iframe srcdoc {nested_label}", nested_value)
            for nested_label, nested_value in external_resource_references(
                srcdoc, from_file, depth=depth + 1
            )
        )
    return found


def svg_resource_root_escapes(payload, from_file, *, depth=0, label="SVG"):
    candidates, _ = svg_resource_candidates(payload, label)
    escapes = local_resource_escapes(from_file, candidates)
    escapes.extend(data_document_root_escapes(candidates, from_file, depth=depth))
    if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
        return escapes
    root = parse_xml_document(payload, label)
    for srcdoc in svg_srcdoc_values(root):
        escapes.extend(
            (f"SVG iframe srcdoc {nested_label}", nested_value)
            for nested_label, nested_value in html_resource_root_escapes(
                srcdoc, from_file, depth=depth + 1
            )
        )
    return escapes


def xml_document_issues(payload, label):
    """Return safety issues for non-SVG XML assets without treating sitemap locs as loads."""

    root = parse_xml_document(payload, label)
    issues = []
    if XML_STYLESHEET_PI_RE.search(payload):
        issues.append(("prohibited XML stylesheet", "xml-stylesheet"))
    for element in root.iter():
        for value in xml_base_attribute_values(element):
            issues.append(("xml:base", value))
    return issues


def xml_element_text(element):
    """Return all XML text, including preserved XHTML style comments."""

    return "".join(element.itertext())


def xhtml_resource_context(payload, label):
    """Collect XHTML declarations without HTMLParser's namespace recovery.

    XHTML is XML.  In particular, a prefixed ``h:style`` can carry a CDATA or
    XML-comment CSS payload that ``HTMLParser`` does not expose as raw text.
    This parser therefore walks the XML tree directly and treats the same
    static resource declarations as ordinary HTML.
    """

    root = parse_xml_document(payload, label)
    if xml_name_parts(root.tag)[1] != "html":
        raise ValueError(f"{label} root is not an XHTML html element")

    candidates = []
    base_values = []
    srcdocs = []
    for element in root.iter():
        _, tag = xml_name_parts(element.tag)
        if not tag:
            continue
        plain_attributes = xml_plain_attributes(element)

        if tag == "base":
            base_values.extend(xml_plain_attribute_values(element, "href"))

        if tag == "meta" and plain_attributes.get("http-equiv", "").strip().lower() == "refresh":
            for content in xml_plain_attribute_values(element, "content"):
                target = meta_refresh_target(content)
                if target is not None:
                    candidates.append(("meta refresh", target))

        if (
            tag == "script"
            and plain_attributes.get("type", "").strip().lower() == "speculationrules"
        ):
            candidates.extend(speculation_rule_source_candidates(xml_element_text(element)))

        for attr in RESOURCE_ATTRIBUTES.get(tag, ()):
            for qualified_attr, value in element.attrib.items():
                namespace, local = xml_name_parts(qualified_attr)
                if (
                    (attr == "xlink:href" and namespace == XLINK_NAMESPACE and local == "href")
                    or (attr != "xlink:href" and not namespace and local == attr)
                ):
                    if attr == "srcset":
                        candidates.extend(
                            (f"{tag} srcset", candidate)
                            for candidate in srcset_candidates(value)
                        )
                    else:
                        candidates.append((tag, value))

        if tag in AUTOMATIC_ATTRIBUTION_TAGS:
            for value in xml_plain_attribute_values(element, "attributionsrc"):
                candidates.extend(
                    (f"{tag} attributionsrc", candidate)
                    for candidate in value.split()
                )
        if tag in PING_RESOURCE_TAGS:
            for value in xml_plain_attribute_values(element, "ping"):
                candidates.extend(
                    (f"{tag} ping", candidate)
                    for candidate in value.split()
                )

        if tag == "link":
            rels = set(plain_attributes.get("rel", "").lower().split())
            href = plain_attributes.get("href")
            if href and rels.intersection(RESOURCE_LINK_RELS):
                candidates.append(("link", href))
            if (
                "preload" in rels
                and plain_attributes.get("as", "").strip().lower() == "image"
                and "imagesrcset" in plain_attributes
            ):
                candidates.extend(
                    ("link imagesrcset", candidate)
                    for candidate in srcset_candidates(plain_attributes["imagesrcset"])
                )

        for attr in SVG_URL_PRESENTATION_ATTRIBUTES:
            for value in xml_plain_attribute_values(element, attr):
                candidates.extend(css_value_resource_candidates(value, f"{tag} {attr}"))
        for value in xml_plain_attribute_values(element, "style"):
            candidates.extend(
                css_resource_candidates(value, f"{tag} inline style", declaration_context=True)
            )
        if tag == "style":
            candidates.extend(css_resource_candidates(xml_element_text(element), "xhtml style"))
        if tag == "iframe":
            srcdocs.extend(xml_plain_attribute_values(element, "srcdoc"))
    return root, candidates, base_values, [value for value in srcdocs if value]


def xhtml_base_href_issues(from_file, base_values):
    issues = []
    for value in base_values:
        _, state = resolve_base_route(from_file, value)
        if state == "external":
            issues.append(("base", value))
        elif state == "escape":
            issues.append(("base outside public-site root", value))
        elif state == "invalid":
            issues.append(("invalid base URL", value))
    return issues


def xhtml_external_resource_references(payload, from_file, *, depth=0, label="XHTML"):
    """Return external XHTML declarations using XML-aware content extraction."""

    _, candidates, base_values, srcdocs = xhtml_resource_context(payload, label)
    found = list(xml_document_issues(payload, label))
    found.extend(xhtml_base_href_issues(from_file, base_values))
    found.extend(
        (candidate_label, value)
        for candidate_label, value in candidates
        if value and is_external_resource(value)
    )
    found.extend(data_document_external_references(candidates, from_file, depth=depth))
    for srcdoc in srcdocs:
        if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
            found.append(("unverifiable XHTML iframe srcdoc", "nested-document depth exceeded"))
            continue
        found.extend(
            (f"XHTML iframe srcdoc {nested_label}", nested_value)
            for nested_label, nested_value in external_resource_references(
                srcdoc, from_file, depth=depth + 1
            )
        )
    return found


def xhtml_resource_root_escapes(payload, from_file, *, depth=0, label="XHTML"):
    """Return XHTML static references that leave the public-site root."""

    _, candidates, base_values, srcdocs = xhtml_resource_context(payload, label)
    base_href = base_values[0] if base_values else None
    escapes = local_resource_escapes(from_file, candidates, base_href)
    escapes.extend(data_document_root_escapes(candidates, from_file, depth=depth))
    if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
        return escapes
    for srcdoc in srcdocs:
        escapes.extend(
            (f"XHTML iframe srcdoc {nested_label}", nested_value)
            for nested_label, nested_value in html_resource_root_escapes(
                srcdoc, from_file, depth=depth + 1
            )
        )
    return escapes


def webmanifest_resource_candidates(payload, label):
    """Return URL-bearing Web App Manifest members with strict structural checks."""

    try:
        manifest = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON ({exc.msg})") from exc
    if not isinstance(manifest, dict):
        raise ValueError(f"{label} JSON root must be an object")

    candidates = []

    def scalar(container, key, candidate_label):
        if key not in container:
            return
        value = container[key]
        if not isinstance(value, str):
            raise ValueError(f"{label} {candidate_label} must be a string")
        candidates.append((candidate_label, value))

    def source_entries(items, candidate_label):
        if not isinstance(items, list):
            raise ValueError(f"{label} {candidate_label} must be a list")
        for item in items:
            if not isinstance(item, dict):
                raise ValueError(f"{label} {candidate_label} entry must be an object")
            scalar(item, "src", candidate_label)

    def source_list(container, key, candidate_label):
        if key in container:
            source_entries(container[key], candidate_label)

    def localized_source_map(container, key, candidate_label):
        if key not in container:
            return
        locales = container[key]
        if not isinstance(locales, dict):
            raise ValueError(f"{label} {candidate_label} must be a locale map")
        for locale, items in locales.items():
            if not isinstance(locale, str):
                raise ValueError(f"{label} {candidate_label} locale must be a string")
            source_entries(items, candidate_label)

    for key in ("id", "scope", "start_url"):
        scalar(manifest, key, f"manifest {key}")
    source_list(manifest, "icons", "manifest icon")
    localized_source_map(manifest, "icons_localized", "manifest localized icon")
    source_list(manifest, "screenshots", "manifest screenshot")
    localized_source_map(manifest, "screenshots_localized", "manifest localized screenshot")

    if "shortcuts" in manifest:
        shortcuts = manifest["shortcuts"]
        if not isinstance(shortcuts, list):
            raise ValueError(f"{label} manifest shortcuts must be a list")
        for shortcut in shortcuts:
            if not isinstance(shortcut, dict):
                raise ValueError(f"{label} manifest shortcut entry must be an object")
            scalar(shortcut, "url", "manifest shortcut URL")
            source_list(shortcut, "icons", "manifest shortcut icon")
            localized_source_map(shortcut, "icons_localized", "manifest localized shortcut icon")

    for object_key, url_key, candidate_label in (
        ("share_target", "action", "manifest share target"),
    ):
        if object_key in manifest:
            target = manifest[object_key]
            if not isinstance(target, dict):
                raise ValueError(f"{label} {object_key} must be an object")
            scalar(target, url_key, candidate_label)

    for list_key, url_key, candidate_label in (
        ("file_handlers", "action", "manifest file handler"),
        ("protocol_handlers", "url", "manifest protocol handler"),
        ("related_applications", "url", "manifest related application"),
    ):
        if list_key not in manifest:
            continue
        entries = manifest[list_key]
        if not isinstance(entries, list):
            raise ValueError(f"{label} {list_key} must be a list")
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"{label} {list_key} entry must be an object")
            scalar(entry, url_key, candidate_label)

    for list_key, candidate_label in (
        ("scope_extensions", "manifest scope extension"),
        ("url_handlers", "manifest URL handler"),
    ):
        if list_key not in manifest:
            continue
        entries = manifest[list_key]
        if not isinstance(entries, list):
            raise ValueError(f"{label} {list_key} must be a list")
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"{label} {list_key} entry must be an object")
            scalar(entry, "origin", candidate_label)

    if "serviceworker" in manifest:
        serviceworker = manifest["serviceworker"]
        if not isinstance(serviceworker, dict):
            raise ValueError(f"{label} serviceworker must be an object")
        scalar(serviceworker, "src", "manifest serviceworker source")
        scalar(serviceworker, "scope", "manifest serviceworker scope")
    return candidates


def html_automatic_document_candidates(body):
    """Return local-document declarations browsers can automatically open."""

    candidates = list(meta_refresh_candidates(body))
    candidates.extend(speculation_rule_candidates(body))
    for tag, attrs in extract_start_tags(body):
        if tag.rsplit(":", 1)[-1] != "link":
            continue
        rels = {
            token.lower()
            for value in attribute_values(attrs, "rel")
            for token in value.split()
        }
        if rels.intersection(AUTOMATIC_DOCUMENT_LINK_RELS):
            candidates.extend(("link automatic document", value) for value in attribute_values(attrs, "href"))
    return candidates


def xhtml_automatic_document_candidates(root, candidates):
    """Return automatic document targets from an XML-parsed XHTML tree."""

    selected = [
        (label, value)
        for label, value in candidates
        if label == "meta refresh" or label.startswith("speculationrules ")
    ]
    for element in root.iter():
        _, tag = xml_name_parts(element.tag)
        if tag != "link":
            continue
        attrs = xml_plain_attributes(element)
        rels = set(attrs.get("rel", "").lower().split())
        if rels.intersection(AUTOMATIC_DOCUMENT_LINK_RELS) and attrs.get("href"):
            selected.append(("link automatic document", attrs["href"]))
    return selected


def svg_automatic_document_candidates(root, candidates):
    """Return automatic document targets from SVG foreign HTML declarations."""

    return xhtml_automatic_document_candidates(root, candidates)


def local_document_target_files(candidates, from_file, base_href=None):
    """Resolve automatic navigation targets without assuming a filename suffix.

    Extensionless targets are routine for static routes.  Queue them as an
    HTML-like document for the same recursive static-declaration pass; known
    document suffixes are likewise queued even if reached only from a Web App
    Manifest or browser prefetch hint.
    """

    targets = set()
    for _, value in candidates:
        target = local_file_target(value, from_file, base_href)
        if target is None:
            continue
        name = os.path.basename(target).lower()
        if not os.path.splitext(name)[1] or name.endswith(DOCUMENT_NAVIGATION_SUFFIXES):
            targets.add(target)
    return targets


def manifest_document_target_files(candidates, from_file):
    """Return local document routes activated by Web App Manifest members."""

    return local_document_target_files(
        [
            (label, value)
            for label, value in candidates
            if label in MANIFEST_DOCUMENT_CANDIDATE_LABELS
        ],
        from_file,
    )


def manifest_link_target_files(body, from_file):
    """Return local manifest paths declared by HTML, rejecting opaque manifest URLs."""

    targets = []
    base_href = extract_base_href(body)
    for tag, attrs in extract_start_tags(body):
        if tag.rsplit(":", 1)[-1] != "link":
            continue
        rels = {
            token.lower()
            for value in attribute_values(attrs, "rel")
            for token in value.split()
        }
        if "manifest" not in rels:
            continue
        for href in attribute_values(attrs, "href"):
            if is_non_network_resource_reference(href):
                raise ValueError("data/blob/fragment Web App Manifest URLs are not permitted")
            if is_external_resource(href):
                continue  # The ordinary HTML resource pass reports it.
            target, state = resolve_link(from_file, href, base_href)
            if state == "escape" or target is None or not is_inside_public_root(target):
                continue  # The ordinary public-root pass reports it.
            if os.path.isfile(target):
                targets.append(os.path.relpath(target, BASE_DIR))
    return targets


def local_stylesheet_target_files(body, from_file):
    """Return local stylesheet targets without assuming a filename extension."""

    targets = []
    base_href = extract_base_href(body)
    for tag, attrs in extract_start_tags(body):
        if tag.rsplit(":", 1)[-1] != "link":
            continue
        rels = {
            token.lower()
            for value in attribute_values(attrs, "rel")
            for token in value.split()
        }
        if "stylesheet" not in rels:
            continue
        for href in attribute_values(attrs, "href"):
            if is_external_resource(href) or is_non_network_resource_reference(href):
                continue
            target, state = resolve_link(from_file, href, base_href)
            if state == "escape" or target is None or not is_inside_public_root(target):
                continue
            if os.path.isfile(target):
                targets.append(os.path.relpath(target, BASE_DIR))
    return targets


def local_embedded_document_target_files(body, from_file):
    """Return local frame/object documents even when they have no .html suffix."""

    targets = []
    base_href = extract_base_href(body)
    attributes_by_tag = {
        "embed": ("src",),
        "fencedframe": ("src",),
        "frame": ("href", "src", "xlink:href"),
        "iframe": ("href", "src", "xlink:href"),
        "object": ("data",),
        "portal": ("src",),
    }
    for tag, attrs in extract_start_tags(body):
        resource_tag = tag.rsplit(":", 1)[-1]
        for attr in attributes_by_tag.get(resource_tag, ()):
            for value in resource_attribute_values(attrs, attr):
                if is_external_resource(value) or is_non_network_resource_reference(value):
                    continue
                target, state = resolve_link(from_file, value, base_href)
                if state == "escape" or target is None or not is_inside_public_root(target):
                    continue
                if os.path.isfile(target):
                    targets.append(os.path.relpath(target, BASE_DIR))
    return targets


def local_file_target(value, from_file, base_href=None):
    """Resolve one local static target, returning a public-root-relative file."""

    if is_external_resource(value) or is_non_network_resource_reference(value):
        return None
    target, state = resolve_link(from_file, value, base_href)
    if state == "escape" or target is None or not is_inside_public_root(target):
        return None
    if not os.path.isfile(target):
        return None
    return os.path.relpath(target, BASE_DIR)


def read_static_document_payload(rel_path):
    return read_svg_payload(rel_path) if rel_path.lower().endswith(".svgz") else read_file(rel_path)


def local_xml_like_target_files(candidates, from_file, base_href=None):
    """Find extensionless or uncommon-suffix local SVG/XML payloads by content."""

    targets = set()
    known_static_suffixes = (".svg", ".svgz", ".xml", ".xhtml", ".xht")
    for _, value in candidates:
        target = local_file_target(value, from_file, base_href)
        if target is None or target.lower().endswith(known_static_suffixes):
            continue
        payload = read_static_document_payload(target)
        if XML_STYLESHEET_PI_RE.search(payload):
            raise ValueError(f"{target} contains an XML stylesheet processing instruction")
        if xml_payload_kind(payload, target) is not None:
            targets.add(target)
    return targets


def local_css_import_target_files(css, from_file, base_href=None):
    """Return local ``@import`` targets without trusting a filename extension."""

    return [
        target
        for value in css_import_values(css)
        if (target := local_file_target(value, from_file, base_href)) is not None
    ]


def inline_css_import_target_files(body, from_file):
    """Return local CSS imports declared inside HTML ``style`` blocks."""

    targets = []
    base_href = extract_base_href(body)
    for css in extract_style_blocks(body):
        targets.extend(local_css_import_target_files(css, from_file, base_href))
    return targets


def local_html_surface_targets(body, from_file, *, depth=0):
    """Discover local style/document/manifest targets through nested ``srcdoc``."""

    css_targets = set(local_stylesheet_target_files(body, from_file))
    css_targets.update(inline_css_import_target_files(body, from_file))
    document_targets = set(local_embedded_document_target_files(body, from_file))
    document_targets.update(
        local_document_target_files(
            html_automatic_document_candidates(body),
            from_file,
            extract_base_href(body),
        )
    )
    manifest_targets = set(manifest_link_target_files(body, from_file))
    if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
        return css_targets, document_targets, manifest_targets
    for srcdoc in embedded_srcdoc_values(body):
        nested_css, nested_documents, nested_manifests = local_html_surface_targets(
            srcdoc, from_file, depth=depth + 1
        )
        css_targets.update(nested_css)
        document_targets.update(nested_documents)
        manifest_targets.update(nested_manifests)
    return css_targets, document_targets, manifest_targets


def xhtml_local_surface_targets(payload, from_file, label, *, depth=0):
    """Discover local recursive surfaces from XML-parsed XHTML."""

    root, candidates, base_values, srcdocs = xhtml_resource_context(payload, label)
    base_href = base_values[0] if base_values else None
    css_targets = set()
    document_targets = set()
    manifest_targets = set()
    embedded_attributes = {
        "embed": ("src",),
        "fencedframe": ("src",),
        "frame": ("href", "src"),
        "iframe": ("href", "src"),
        "object": ("data",),
        "portal": ("src",),
    }

    for element in root.iter():
        _, tag = xml_name_parts(element.tag)
        if not tag:
            continue
        attrs = xml_plain_attributes(element)
        if tag == "link":
            rels = set(attrs.get("rel", "").lower().split())
            href = attrs.get("href")
            if href and "stylesheet" in rels:
                target = local_file_target(href, from_file, base_href)
                if target is not None:
                    css_targets.add(target)
            if href and "manifest" in rels:
                if is_non_network_resource_reference(href):
                    raise ValueError("data/blob/fragment Web App Manifest URLs are not permitted")
                target = local_file_target(href, from_file, base_href)
                if target is not None:
                    manifest_targets.add(target)
        if tag == "style":
            css_targets.update(
                local_css_import_target_files(
                    xml_element_text(element), from_file, base_href
                )
            )
        for attr in embedded_attributes.get(tag, ()):
            value = attrs.get(attr)
            if value:
                target = local_file_target(value, from_file, base_href)
                if target is not None:
                    document_targets.add(target)

    document_targets.update(local_xml_like_target_files(candidates, from_file, base_href))
    document_targets.update(
        local_document_target_files(
            xhtml_automatic_document_candidates(root, candidates), from_file, base_href
        )
    )
    if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
        return css_targets, document_targets, manifest_targets
    for srcdoc in srcdocs:
        nested_css, nested_documents, nested_manifests = local_html_surface_targets(
            srcdoc, from_file, depth=depth + 1
        )
        css_targets.update(nested_css)
        document_targets.update(nested_documents)
        manifest_targets.update(nested_manifests)
    return css_targets, document_targets, manifest_targets


def svg_local_surface_targets(payload, from_file, label, *, depth=0):
    """Discover local HTML-like surfaces declared inside SVG foreign content."""

    root = parse_xml_document(payload, label)
    css_targets = set(svg_css_import_target_files(payload, from_file, label))
    document_targets = set()
    manifest_targets = set()
    resource_candidates, _ = svg_resource_candidates(payload, label)
    document_targets.update(local_xml_like_target_files(resource_candidates, from_file))
    document_targets.update(
        local_document_target_files(
            svg_automatic_document_candidates(root, resource_candidates), from_file
        )
    )
    embedded_attributes = {
        "embed": ("src",),
        "fencedframe": ("src",),
        "frame": ("href", "src"),
        "iframe": ("href", "src"),
        "object": ("data",),
        "portal": ("src",),
    }
    for element in root.iter():
        _, tag = xml_name_parts(element.tag)
        attrs = xml_plain_attributes(element)
        if tag == "link":
            rels = set(attrs.get("rel", "").lower().split())
            href = attrs.get("href")
            if href and "stylesheet" in rels:
                target = local_file_target(href, from_file)
                if target is not None:
                    css_targets.add(target)
            if href and "manifest" in rels:
                if is_non_network_resource_reference(href):
                    raise ValueError("data/blob/fragment Web App Manifest URLs are not permitted")
                target = local_file_target(href, from_file)
                if target is not None:
                    manifest_targets.add(target)
        for attr in embedded_attributes.get(tag, ()):
            value = attrs.get(attr)
            if value:
                target = local_file_target(value, from_file)
                if target is not None:
                    document_targets.add(target)
    if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
        return css_targets, document_targets, manifest_targets
    for srcdoc in svg_srcdoc_values(root):
        nested_css, nested_documents, nested_manifests = local_html_surface_targets(
            srcdoc, from_file, depth=depth + 1
        )
        css_targets.update(nested_css)
        document_targets.update(nested_documents)
        manifest_targets.update(nested_manifests)
    return css_targets, document_targets, manifest_targets


def svg_css_import_target_files(payload, from_file, label):
    """Return local CSS imports declared inside namespace-aware SVG style blocks."""

    root = parse_xml_document(payload, label)
    targets = []
    for element in root.iter():
        _, tag = xml_name_parts(element.tag)
        if tag == "style" and element.text:
            targets.extend(local_css_import_target_files(element.text, from_file))
    return targets


def is_non_network_resource_reference(value):
    return normalized_url_reference(value).lower().startswith(("data:", "blob:", "#"))


def local_resource_escapes(from_file, candidates, base_href=None):
    """Return resource references that resolve outside the public-site root."""

    escapes = []
    for label, value in candidates:
        if (
            not value
            or is_external_resource(value)
            or is_non_network_resource_reference(value)
        ):
            continue
        target, state = resolve_link(from_file, value, base_href)
        if state == "invalid":
            escapes.append((f"unverifiable {label}", value))
        elif state == "escape" or (target is not None and not is_inside_public_root(target)):
            escapes.append((label, value))
    return escapes


def data_document_external_references(candidates, from_file, *, depth):
    """Return unsafe nested declarations carried by data-document URLs."""

    found = []
    for label, value in candidates:
        decoded = data_document_payload(value)
        if decoded is None:
            continue
        media_type, payload = decoded
        if media_type == "invalid":
            found.append((f"unverifiable {label} data document", payload))
        elif media_type in REJECTED_DATA_DOCUMENT_MEDIA_TYPES or (
            media_type.endswith("+xml") and media_type != SVG_DATA_MEDIA_TYPE
        ):
            found.append((f"prohibited {label} {media_type} data document", media_type))
        elif depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
            found.append((f"unverifiable {label} SVG data document", "nested-document depth exceeded"))
        else:
            try:
                found.extend(
                    (f"{label} SVG data {nested_label}", nested_value)
                    for nested_label, nested_value in svg_external_resource_references(
                        payload,
                        from_file,
                        depth=depth + 1,
                        label=f"{label} SVG data document",
                    )
                )
            except ValueError as exc:
                found.append((f"unverifiable {label} SVG data document", str(exc)))
    return found


def data_document_root_escapes(candidates, from_file, *, depth):
    """Return local resource escapes carried by allowed SVG data payloads."""

    escapes = []
    for label, value in candidates:
        decoded = data_document_payload(value)
        if decoded is None:
            continue
        media_type, payload = decoded
        if media_type != SVG_DATA_MEDIA_TYPE or depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
            continue
        try:
            escapes.extend(
                (f"{label} SVG data {nested_label}", nested_value)
                for nested_label, nested_value in svg_resource_root_escapes(
                    payload,
                    from_file,
                    depth=depth + 1,
                    label=f"{label} SVG data document",
                )
            )
        except ValueError:
            # The matching external-reference pass emits the fail-closed error.
            continue
    return escapes


def external_resource_references(body, from_file="index.html", *, depth=0):
    """Return external static resources, including CSS and duplicate attrs."""

    found = list(base_href_issues(from_file, body)) + xml_base_issues(body)
    all_candidates = html_static_resource_candidates(body)
    found.extend(
        (label, value)
        for label, value in all_candidates
        if value and is_external_resource(value)
    )
    found.extend(data_document_external_references(all_candidates, from_file, depth=depth))
    for srcdoc in embedded_srcdoc_values(body):
        if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
            found.append(("unverifiable iframe srcdoc", "nested-document depth exceeded"))
            continue
        found.extend(
            (f"iframe srcdoc {label}", value)
            for label, value in external_resource_references(
                srcdoc, from_file, depth=depth + 1
            )
        )
    return found


def html_resource_root_escapes(body, from_file, *, depth=0):
    base_href = extract_base_href(body)
    candidates = html_static_resource_candidates(body)
    escapes = local_resource_escapes(from_file, candidates, base_href)
    escapes.extend(data_document_root_escapes(candidates, from_file, depth=depth))
    if depth >= MAX_EMBEDDED_DOCUMENT_DEPTH:
        return escapes
    for srcdoc in embedded_srcdoc_values(body):
        escapes.extend(
            (f"iframe srcdoc {label}", value)
            for label, value in html_resource_root_escapes(
                srcdoc, from_file, depth=depth + 1
            )
        )
    return escapes


def is_inside_public_root(path):
    root = os.path.realpath(BASE_DIR)
    target = os.path.realpath(path)
    try:
        return os.path.commonpath((root, target)) == root
    except ValueError:
        return False

def resolve_link(from_file, href, base_href=None):
    normalized_href = normalized_url_reference(href)
    parsed_href = urlparse(normalized_href)
    if (
        normalized_href.startswith("//")
        or
        parsed_href.scheme
        or parsed_href.netloc
        or normalized_href.startswith(("mailto:", "javascript:", "data:", "#"))
    ):
        return None, "external"
    # Query and fragment do not name a different worktree object.  Keeping a
    # manifest/cache-busting query in the filesystem path would otherwise hide
    # a local resource from the recursive static scan.
    try:
        href = decoded_local_url_path(parsed_href.path)
    except ValueError:
        return None, "invalid"
    if not href:
        return None, "external"
    if href.startswith("/"):
        target = os.path.normpath(os.path.join(BASE_DIR, href.lstrip("/")))
        return target, "absolute"
    from_dir = os.path.dirname(from_file)
    if base_href:
        # A <base href="../"> on /home/ resolves to the site root before the
        # link is applied; joining raw filesystem paths would incorrectly step
        # above BASE_DIR for a later href="../". Resolve in route space first.
        base, base_state = resolve_base_route(from_file, base_href)
        if base_state != "local":
            return None, base_state
        target_route = urljoin(base, href)
        parsed_target = urlparse(target_route)
        if parsed_target.scheme or parsed_target.netloc:
            return None, "external"
        try:
            target_path = decoded_local_url_path(parsed_target.path)
        except ValueError:
            return None, "invalid"
        target = os.path.normpath(os.path.join(BASE_DIR, target_path.lstrip("/")))
    else:
        target = os.path.normpath(os.path.join(BASE_DIR, from_dir, href))
    return target, "relative"

def check_external_refs():
    print("\n[1] Static HTML/CSS/SVG/manifest resource references (security gate)")
    found = False

    def report(source, external, escapes):
        nonlocal found
        for tag, value in external:
            found = True
            if tag == "base outside public-site root":
                error(f"{source}: {tag} -> {value}")
            elif tag == "unverifiable iframe srcdoc":
                error(f"{source}: {tag} ({value})")
            else:
                error(f"{source}: external {tag} -> {value}")
        for tag, value in escapes:
            found = True
            if tag.startswith("unverifiable "):
                error(f"{source}: {tag} -> {value}")
            else:
                error(f"{source}: {tag} -> {value} (escapes public-site root)")

    html_pending = set(get_public_html_files())
    seen_html = set()
    css_pending = set(get_public_css_files())
    seen_css = set()
    svg_pending = set(get_public_svg_files())
    seen_svg = set()
    xml_pending = set(get_public_xml_files())
    seen_xml = set()
    manifest_pending = set(get_public_webmanifest_files())
    seen_manifests = set()

    while html_pending or css_pending or svg_pending or xml_pending or manifest_pending:
        if html_pending:
            html_file = min(html_pending)
            html_pending.remove(html_file)
            if html_file in seen_html:
                continue
            seen_html.add(html_file)
            try:
                body = read_static_document_payload(html_file)
                kind = xml_payload_kind(body, html_file)
                if kind == "svg":
                    external = svg_external_resource_references(body, html_file, label=html_file)
                    escapes = svg_resource_root_escapes(body, html_file, label=html_file)
                    css_targets, document_targets, manifest_targets = svg_local_surface_targets(
                        body, html_file, html_file
                    )
                elif kind == "xml":
                    external = xml_document_issues(body, html_file)
                    escapes = []
                    css_targets, document_targets, manifest_targets = set(), set(), set()
                elif kind == "html":
                    external = xhtml_external_resource_references(body, html_file, label=html_file)
                    escapes = xhtml_resource_root_escapes(body, html_file, label=html_file)
                    css_targets, document_targets, manifest_targets = xhtml_local_surface_targets(
                        body, html_file, html_file
                    )
                else:
                    external = external_resource_references(body, html_file)
                    escapes = html_resource_root_escapes(body, html_file)
                    css_targets, document_targets, manifest_targets = local_html_surface_targets(
                        body, html_file
                    )
                    document_targets.update(
                        local_xml_like_target_files(
                            html_static_resource_candidates(body), html_file
                        )
                    )
            except ValueError as exc:
                found = True
                error(f"{html_file}: cannot verify static resource references ({exc})")
                continue
            css_pending.update(css_targets)
            html_pending.update(document_targets)
            manifest_pending.update(manifest_targets)
            report(html_file, external, escapes)
            continue

        if css_pending:
            css_file = min(css_pending)
            css_pending.remove(css_file)
            if css_file in seen_css:
                continue
            seen_css.add(css_file)
            try:
                css = read_file(css_file)
                candidates = css_resource_candidates(css, "css")
                css_import_values(css)
                document_targets = local_xml_like_target_files(candidates, css_file)
            except ValueError as exc:
                found = True
                error(f"{css_file}: cannot verify CSS resource references ({exc})")
                continue
            css_pending.update(local_css_import_target_files(css, css_file))
            html_pending.update(document_targets)
            external = [
                (tag, value) for tag, value in candidates if value and is_external_resource(value)
            ]
            external.extend(data_document_external_references(candidates, css_file, depth=0))
            escapes = local_resource_escapes(css_file, candidates)
            escapes.extend(data_document_root_escapes(candidates, css_file, depth=0))
            report(css_file, external, escapes)
            continue

        if svg_pending:
            svg_file = min(svg_pending)
            svg_pending.remove(svg_file)
            if svg_file in seen_svg:
                continue
            seen_svg.add(svg_file)
            try:
                payload = read_svg_payload(svg_file)
                external = svg_external_resource_references(payload, svg_file, label=svg_file)
                escapes = svg_resource_root_escapes(payload, svg_file, label=svg_file)
                css_targets, document_targets, manifest_targets = svg_local_surface_targets(
                    payload, svg_file, svg_file
                )
            except ValueError as exc:
                found = True
                error(f"{svg_file}: cannot verify SVG resource references ({exc})")
                continue
            css_pending.update(css_targets)
            html_pending.update(document_targets)
            manifest_pending.update(manifest_targets)
            report(svg_file, external, escapes)
            continue

        if xml_pending:
            xml_file = min(xml_pending)
            xml_pending.remove(xml_file)
            if xml_file in seen_xml:
                continue
            seen_xml.add(xml_file)
            try:
                payload = read_file(xml_file)
                root = parse_xml_document(payload, xml_file)
                root_name = xml_name_parts(root.tag)[1]
                if root_name == "svg":
                    external = svg_external_resource_references(payload, xml_file, label=xml_file)
                    escapes = svg_resource_root_escapes(payload, xml_file, label=xml_file)
                    css_targets, document_targets, manifest_targets = svg_local_surface_targets(
                        payload, xml_file, xml_file
                    )
                elif root_name == "html":
                    external = xhtml_external_resource_references(payload, xml_file, label=xml_file)
                    escapes = xhtml_resource_root_escapes(payload, xml_file, label=xml_file)
                    css_targets, document_targets, manifest_targets = xhtml_local_surface_targets(
                        payload, xml_file, xml_file
                    )
                else:
                    external = xml_document_issues(payload, xml_file)
                    escapes = []
                    css_targets, document_targets, manifest_targets = set(), set(), set()
            except ValueError as exc:
                found = True
                error(f"{xml_file}: cannot verify XML resource references ({exc})")
                continue
            css_pending.update(css_targets)
            html_pending.update(document_targets)
            manifest_pending.update(manifest_targets)
            report(xml_file, external, escapes)
            continue

        manifest_file = min(manifest_pending)
        manifest_pending.remove(manifest_file)
        if manifest_file in seen_manifests:
            continue
        seen_manifests.add(manifest_file)
        try:
            candidates = webmanifest_resource_candidates(read_file(manifest_file), manifest_file)
            document_targets = local_xml_like_target_files(candidates, manifest_file)
            document_targets.update(manifest_document_target_files(candidates, manifest_file))
        except ValueError as exc:
            found = True
            error(f"{manifest_file}: cannot verify Web App Manifest resources ({exc})")
            continue
        html_pending.update(document_targets)
        external = [
            (tag, value) for tag, value in candidates if value and is_external_resource(value)
        ]
        external.extend(data_document_external_references(candidates, manifest_file, depth=0))
        escapes = local_resource_escapes(manifest_file, candidates)
        escapes.extend(data_document_root_escapes(candidates, manifest_file, depth=0))
        report(manifest_file, external, escapes)
    if not found:
        ok("No external or protocol-relative static HTML/CSS/SVG/manifest resource declarations")
    return not found

def check_internal_links():
    print("\n[2] Internal link resolution")
    dead = []
    escapes = []
    unsafe_bases = []
    for html_file in get_public_html_files():
        body = read_file(html_file)
        base_href = extract_base_href(body)
        issues = base_href_issues(html_file, body)
        if issues:
            unsafe_bases.extend((html_file, label, value) for label, value in issues)
            continue
        for href in extract_hrefs(body):
            target, ltype = resolve_link(html_file, href, base_href)
            if target is None:
                continue
            if not is_inside_public_root(target):
                escapes.append((html_file, href))
                continue
            if os.path.exists(target):
                continue
            if os.path.isdir(target) and os.path.exists(os.path.join(target, "index.html")):
                continue
            if not href.endswith("/") and not os.path.splitext(target)[1]:
                index_file = os.path.join(target, "index.html")
                if os.path.exists(index_file):
                    continue
            dead.append((html_file, href, os.path.relpath(target, BASE_DIR)))
    if dead:
        for src, href, missing in dead:
            error(f"{src} -> {href} (missing: {missing})")
    if escapes:
        for src, href in escapes:
            error(f"{src} -> {href} (escapes public-site root)")
    if unsafe_bases:
        for src, label, value in unsafe_bases:
            error(f"{src}: unsafe {label} -> {value}")
    if not dead and not escapes and not unsafe_bases:
        ok("All internal links resolve")
    return not dead and not escapes and not unsafe_bases

def check_orphans():
    print("\n[3] Orphan page check")
    html_files = get_public_html_files()
    html_set = {os.path.normpath(os.path.join(BASE_DIR, f)) for f in html_files}
    # Crawl root = the site's actual front door.
    entry = os.path.normpath(os.path.join(BASE_DIR, "index.html"))
    reachable = set()
    queue = [entry] if os.path.exists(entry) else []
    while queue:
        full = os.path.normpath(queue.pop(0))
        if full in reachable or full not in html_set:
            continue
        reachable.add(full)
        html_file = os.path.relpath(full, BASE_DIR)
        body = read_file(html_file)
        base_href = extract_base_href(body)
        for href in extract_hrefs(body):
            target, _ = resolve_link(html_file, href, base_href)
            if not target:
                continue
            target = os.path.normpath(target)
            if os.path.isdir(target):
                target = os.path.normpath(os.path.join(target, "index.html"))
            elif not os.path.splitext(target)[1]:
                target = os.path.normpath(os.path.join(target, "index.html"))
            if target in html_set and target not in reachable:
                queue.append(target)
    ignored = {
        # PWA offline fallback: served by the service worker, unlinked by design
        os.path.normpath(os.path.join(BASE_DIR, "offline", "index.html")),
        # Custom 404: served by Vercel on miss, unlinked by design
        os.path.normpath(os.path.join(BASE_DIR, "404.html")),
        # 2026-07-20 (receipt 146, `146_FOUNDER_RULING_EXECUTE_2026_07_20.md`):
        # legacy homepage snapshot,
        # intentionally unlinked (K3)
        os.path.normpath(os.path.join(BASE_DIR, "index_legacy_2026_07_19.html")),
        # /home/ is a retained legacy body behind the permanent /home/ -> / redirect.
        os.path.normpath(os.path.join(BASE_DIR, "home", "index.html")),
        # This is the target of exact reversible historical redirects.  It is
        # deliberately not linked from the current reader funnel.
        os.path.normpath(os.path.join(BASE_DIR, "historical-boundary", "index.html")),
    }

    # Frozen/noindex projections remain in repository custody and can be
    # directly addressable for provenance, but they are not part of the current
    # public journey.  Do not hide a declared current or provisional route this
    # way: those must retain a real inbound path from the front door.
    try:
        parity = json.loads(read_file("public_semantic_parity.json"))
        declared = set(parity.get("currentSurfaces", []))
        declared.update(parity.get("declaredProvisional", {}).get("routes", []))
        declared.update(parity.get("infrastructureRoutes", {}).get("routes", []))
    except Exception as exc:
        error(f"cannot load public route declarations for orphan check: {exc}")
        return False

    def has_noindex_meta(rel_path):
        for tag, attrs in extract_start_tags(read_file(rel_path)):
            if tag != "meta":
                continue
            values = dict(attrs)
            if values.get("name", "").lower() == "robots" and "noindex" in values.get("content", "").lower():
                return True
        return False

    for rel_path in html_files:
        if rel_path in declared or not has_noindex_meta(rel_path):
            continue
        ignored.add(os.path.normpath(os.path.join(BASE_DIR, rel_path)))
    orphans = [
        os.path.relpath(full, BASE_DIR)
        for full in sorted(html_set - reachable - ignored)
    ]
    if orphans:
        for o in orphans:
            error(f"Not reachable from /: {o}")
    else:
        ok("All public pages reachable from /")
    return len(orphans) == 0

def check_required_assets():
    print("\n[4] Required asset presence")
    all_ok = True
    # Check xai.css exists
    xai = os.path.join(BASE_DIR, "assets", "css", "xai.css")
    if os.path.exists(xai):
        ok("assets/css/xai.css present")
    else:
        error("assets/css/xai.css missing")
        all_ok = False
    # Check theme.js exists
    theme = os.path.join(BASE_DIR, "assets", "js", "theme.js")
    if os.path.exists(theme):
        ok("assets/js/theme.js present")
    else:
        error("assets/js/theme.js missing")
        all_ok = False
    # Check source-note.css exists
    sn = os.path.join(BASE_DIR, "assets", "css", "source-note.css")
    if os.path.exists(sn):
        ok("assets/css/source-note.css present")
    else:
        error("assets/css/source-note.css missing")
        all_ok = False
    # Check dimensions.js exists
    dim = os.path.join(BASE_DIR, "dimensions", "dimensions.js")
    if os.path.exists(dim):
        ok("dimensions/dimensions.js present")
    else:
        error("dimensions/dimensions.js missing")
        all_ok = False

    # Deployed binary/visual assets must be real worktree objects, never Git
    # LFS pointer stubs. Keep this scan cheap and scoped to deployable assets.
    asset_extensions = {
        ".woff", ".woff2", ".ttf", ".otf",
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico",
    }
    lfs_prefix = b"version https://git-lfs.github.com/spec/v1"
    patterns = load_vercelignore_patterns() or []
    checked_assets = 0
    asset_failures = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [
            d for d in dirs
            if d not in {".git", ".vercel", ".next", "node_modules", "90_ARCHIVE", "_archive"}
        ]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in asset_extensions:
                continue
            path = os.path.join(root, filename)
            rel = os.path.relpath(path, BASE_DIR).replace(os.sep, "/")
            if is_vercel_ignored(rel, patterns):
                continue
            checked_assets += 1
            try:
                with open(path, "rb") as fh:
                    sample = fh.read(256)
            except OSError as exc:
                asset_failures.append(f"{rel}: unreadable ({exc})")
                continue
            if not sample:
                asset_failures.append(f"{rel}: empty deployed asset")
            elif sample.startswith(lfs_prefix):
                asset_failures.append(f"{rel}: Git LFS pointer, not asset bytes")

    if not checked_assets:
        error("no deployable font/icon/image assets found")
        all_ok = False
    elif asset_failures:
        for finding in asset_failures:
            error(finding)
        all_ok = False
    else:
        ok(f"{checked_assets} deployable font/icon/image assets are real worktree objects")
    return all_ok

def check_html_wellformedness():
    print("\n[5] HTML well-formedness")
    issues = []
    for html_file in get_public_html_files():
        body = read_file(html_file)
        if not body.strip().upper().startswith("<!DOCTYPE"):
            issues.append((html_file, "missing DOCTYPE"))
        if "<html" not in body.lower():
            issues.append((html_file, "missing <html> tag"))
        if "</html>" not in body.lower():
            issues.append((html_file, "missing </html> tag"))
        if "<head>" not in body.lower():
            issues.append((html_file, "missing <head> tag"))
        if "</head>" not in body.lower():
            issues.append((html_file, "missing </head> tag"))
        if "<body>" not in body.lower() and '<body ' not in body.lower():
            issues.append((html_file, "missing <body> tag"))
        if "</body>" not in body.lower():
            issues.append((html_file, "missing </body> tag"))
    if issues:
        for f, issue in issues:
            error(f"{f}: {issue}")
    else:
        ok("All pages have DOCTYPE, html, head, body tags")
    return len(issues) == 0

def declared_semantic_html_files():
    """Return exactly the lifecycle-declared current/provisional HTML routes."""

    manifest_path = os.path.join(BASE_DIR, "public_semantic_parity.json")
    with open(manifest_path, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    current = manifest.get("currentSurfaces")
    provisional = manifest.get("declaredProvisional", {}).get("routes")
    if not isinstance(current, list) or not isinstance(provisional, list):
        raise ValueError("public semantic manifest lacks current/provisional route lists")
    routes = current + provisional
    if not all(isinstance(route, str) for route in routes):
        raise ValueError("public semantic manifest contains a non-string route")
    public_root = os.path.realpath(BASE_DIR)
    files = set()
    for route in routes:
        normalized = normalized_url_reference(route)
        parsed = urlparse(normalized)
        if (
            not normalized
            or normalized.startswith("/")
            or parsed.scheme
            or parsed.netloc
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError(f"invalid declared public route: {route!r}")
        target = os.path.realpath(os.path.join(BASE_DIR, parsed.path))
        try:
            inside = os.path.commonpath((public_root, target)) == public_root
        except ValueError:
            inside = False
        if not inside:
            raise ValueError(f"declared public route escapes 12_PUBLIC_SITE: {route!r}")
        if target.lower().endswith(".html"):
            files.add(os.path.relpath(target, public_root))
    return sorted(files)


def check_tier_markers():
    print("\n[6] Evidence tier markers on declared current/provisional doctrine pages")
    try:
        doctrine_files = declared_semantic_html_files()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        error(f"cannot load declared semantic HTML routes: {exc}")
        return False

    missing = []
    for html_file in doctrine_files:
        if not os.path.isfile(os.path.join(BASE_DIR, html_file)):
            missing.append(f"{html_file} (declared route is missing)")
            continue
        body = read_file(html_file)
        if not re.search(r'\[A\]|\[S\]|\[I\]|\[C\]|\[B\]|\[D\]', body):
            missing.append(html_file)
    if missing:
        for f in missing:
            error(f"No evidence tier markers: {f}")
    else:
        ok("All declared current/provisional doctrine pages have evidence tier markers")
    return not missing

def check_operator_tier_hygiene():
    print("\n[7] Operators tier hygiene")
    legacy_marker = re.compile(
        r"\[(?:[ABCSID]*/)*(?:E|T)(?:/[ABCSIDET]*)?\]"
        r"|\[(?:E|T)\s+for"
        r"|[;,]\s+(?:E|T)\s+for"
    )
    offenders = []
    for html_file in get_public_html_files():
        if not html_file.startswith("operators/"):
            continue
        body = read_file(html_file)
        if legacy_marker.search(body):
            offenders.append(html_file)
    if offenders:
        for f in offenders:
            error(f"{f}: legacy operator tier marker escaped public normalization")
    else:
        ok("Operators route uses current [A/B/S/I/D/C] tier markers")
    return len(offenders) == 0

def check_public_reading_bundle():
    print("\n[8] Public reading bundle wiring")
    required_surfaces = [
        "read/index.html",
        "reading-manifest.json",
    ]
    all_ok = True
    for rel in required_surfaces:
        if os.path.exists(os.path.join(BASE_DIR, rel)):
            ok(f"{rel} present")
        else:
            error(f"{rel} missing")
            all_ok = False

    manifest_path = os.path.join(BASE_DIR, "reading-manifest.json")
    if not os.path.exists(manifest_path):
        return False

    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except Exception as exc:
        error(f"reading-manifest.json is not valid JSON: {exc}")
        return False

    documents = manifest.get("documents", [])
    counts = {}
    for doc in documents:
        counts[doc.get("section")] = counts.get(doc.get("section"), 0) + 1
        href = doc.get("href", "")
        if not href:
            error(f"manifest document missing href: {doc}")
            all_ok = False
            continue
        target = os.path.join(BASE_DIR, href)
        if href.endswith("/"):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            error(f"manifest target missing: {href}")
            all_ok = False

    registry = load_withheld_registry()
    withheld_artifacts = {item["artifact"] for item in registry["artifacts"]}
    withheld_manifest_hrefs = set()
    for item in registry["artifacts"]:
        manifest_doc = item.get("manifestDocument")
        if manifest_doc is None:
            continue
        withheld_manifest_hrefs.add(manifest_doc["href"])

    published_hrefs = {doc.get("href") for doc in documents}
    leaked_hrefs = sorted(withheld_manifest_hrefs & published_hrefs)
    if leaked_hrefs:
        for href in leaked_hrefs:
            error(f"withheld artifact remains in reading-manifest.json: {href}")
        all_ok = False
    else:
        ok("withheld artifacts are absent from reading-manifest.json")
    expected_hrefs = set()
    expected = {}
    for section in (value for key, value in manifest.get("routes", {}).items() if key != "read"):
        section_name = section.rstrip("/")
        root = os.path.join(BASE_DIR, section_name)
        section_hrefs = set()
        for walk_root, _, names in os.walk(root):
            if "index.html" not in names:
                continue
            artifact = os.path.relpath(os.path.join(walk_root, "index.html"), BASE_DIR).replace(os.sep, "/")
            if artifact == f"{section_name}/index.html" or artifact in withheld_artifacts:
                continue
            body = read_file(artifact)
            if "Generated by 12_PUBLIC_SITE/generate_public_library.py" not in body:
                continue
            section_hrefs.add(os.path.dirname(artifact).replace(os.sep, "/") + "/")
        expected_hrefs.update(section_hrefs)
        expected[section_name] = len(section_hrefs)

    actual_hrefs = {doc.get("href") for doc in documents}
    for href in sorted(expected_hrefs - actual_hrefs):
        error(f"generated public document missing from reading-manifest.json: {href}")
        all_ok = False
    for href in sorted(actual_hrefs - expected_hrefs):
        error(f"reading-manifest.json names a non-current generated document: {href}")
        all_ok = False

    for section, expected_count in expected.items():
        actual = counts.get(section, 0)
        if actual == expected_count:
            ok(f"{section}: {actual} rendered docs")
        else:
            error(f"{section}: expected {expected_count} rendered docs, found {actual}")
            all_ok = False

    total_expected = sum(expected.values())
    if len(documents) == total_expected:
        ok(f"public corpus documents wired: {len(documents)}")
    else:
        error(f"expected {total_expected} public corpus documents, found {len(documents)}")
        all_ok = False

    index_body = read_file("index.html")
    # 2026-07-28: the public front is worldview-first with an immediate practice.
    # These are the declared current reader, evidence, participation, and exit
    # hubs; the frozen historical library is not a first-contact requirement.
    for href in [
        "practice/",
        "plainly/",
        "discoveries/",
        "record/",
        "lab/",
        "book/",
        "about/",
        "contribute/",
        "exit/",
    ]:
        if f'href="{href}"' in index_body:
            ok(f"landing links {href}")
        else:
            error(f"landing missing link to {href}")
            all_ok = False

    practice_body = read_file("practice/index.html")
    for marker in [
        'id="receipt-builder"',
        "Face 1 · commitment",
        "Face 2 · observed outcome",
        "no transmission",
        "comparative benefit over simpler decision practices remains open",
    ]:
        if marker not in practice_body:
            error(f"practice missing local-receipt boundary marker: {marker}")
            all_ok = False

    return all_ok

def check_generated_library_chrome():
    print("\n[9] Generated library chrome contract")
    manifest_path = os.path.join(BASE_DIR, "reading-manifest.json")
    if not os.path.exists(manifest_path):
        error("reading-manifest.json missing; cannot verify generated chrome")
        return False

    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except Exception as exc:
        error(f"reading-manifest.json is not valid JSON: {exc}")
        return False

    generated_pages = set()
    for section, href in manifest.get("routes", {}).items():
        # /read/ is a hand-curated current route through the reader, practice,
        # research, and exit.  It shares the library visual language but is not
        # a frozen generated-library projection.
        if section == "read":
            continue
        if href.endswith("/"):
            generated_pages.add(os.path.normpath(os.path.join(href, "index.html")))
    for doc in manifest.get("documents", []):
        href = doc.get("href", "")
        if href.endswith("/"):
            generated_pages.add(os.path.normpath(os.path.join(href, "index.html")))

    required_markers = [
        '<main class="library-shell">',
        '<section class="library-hero">',
        '<div class="library-route-row">',
        '<article class="library-article">',
        '<aside class="library-meta">',
        "Generated by 12_PUBLIC_SITE/generate_public_library.py",
    ]
    drifted = []
    for rel in sorted(generated_pages):
        path = os.path.join(BASE_DIR, rel)
        if not os.path.exists(path):
            drifted.append((rel, "missing generated page"))
            continue
        body = read_file(rel)
        missing = [marker for marker in required_markers if marker not in body]
        if missing:
            drifted.append((rel, "missing " + ", ".join(missing)))

    if drifted:
        for rel, finding in drifted:
            error(f"{rel}: generated-library chrome drift ({finding})")
        return False

    ok(f"Generated library chrome present on {len(generated_pages)} pages")
    return True

def load_vercelignore_patterns():
    path = os.path.join(BASE_DIR, ".vercelignore")
    if not os.path.exists(path):
        return None
    patterns = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                patterns.append(stripped)
    return patterns

def vercelignore_matches(rel_path, pattern):
    rel_path = rel_path.replace(os.sep, "/")
    pattern = pattern.replace(os.sep, "/")
    if pattern.startswith("!"):
        return False
    anchored = pattern.startswith("/")
    if "[" in pattern or "]" in pattern:
        raise ValueError(
            f"unsupported character-class pattern in .vercelignore: {pattern!r}"
        )
    directory_only = pattern.endswith("/")
    if anchored:
        pattern = pattern[1:]
    if directory_only:
        pattern = pattern[:-1]
    if not pattern:
        raise ValueError("empty .vercelignore pattern is unsupported")

    regex = []
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "*":
            if index + 1 < len(pattern) and pattern[index + 1] == "*":
                while index + 1 < len(pattern) and pattern[index + 1] == "*":
                    index += 1
                if index + 1 < len(pattern) and pattern[index + 1] == "/":
                    regex.append(r"(?:[^/]+/)*")
                    index += 1
                else:
                    regex.append(r".*")
            else:
                regex.append(r"[^/]*")
        elif char == "?":
            regex.append(r"[^/]")
        else:
            regex.append(re.escape(char))
        index += 1
    expression = "".join(regex)
    candidate = rel_path.strip("/")
    parts = candidate.split("/") if candidate else []
    directory_parts = parts if rel_path.endswith("/") else parts[:-1]
    if directory_only:
        if not anchored and "/" not in pattern:
            return any(
                re.fullmatch(expression, part, flags=re.IGNORECASE) is not None
                for part in directory_parts
            )
        directory_prefixes = (
            "/".join(directory_parts[:index])
            for index in range(1, len(directory_parts) + 1)
        )
        return any(
            re.fullmatch(expression, prefix, flags=re.IGNORECASE) is not None
            for prefix in directory_prefixes
        )
    if "/" not in pattern and not anchored:
        return re.fullmatch(
            expression, parts[-1] if parts else "", flags=re.IGNORECASE
        ) is not None
    return re.fullmatch(expression, candidate, flags=re.IGNORECASE) is not None

def is_vercel_ignored(rel_path, patterns):
    rel_path = rel_path.replace(os.sep, "/").strip("/")
    cache = {}

    def is_kept(candidate, *, directory=False):
        cache_key = (candidate, directory)
        if cache_key in cache:
            return cache[cache_key]
        parts = candidate.split("/") if candidate else []
        if len(parts) > 1:
            parent = "/".join(parts[:-1])
            if not is_kept(parent, directory=True):
                cache[cache_key] = False
                return False
        ignored = False
        match_path = candidate + "/" if directory else candidate
        for pattern in patterns:
            negated = pattern.startswith("!")
            raw = pattern[1:] if negated else pattern
            if vercelignore_matches(match_path, raw):
                ignored = not negated
        cache[cache_key] = not ignored
        return not ignored

    return not is_kept(rel_path)


def header_source_covers(source, route):
    if source == route:
        return True
    if source.endswith("(.*)"):
        return route.startswith(source[:-4])
    return False


def normalize_index_route(value):
    if not isinstance(value, str):
        return None
    raw = value.strip()
    if raw.startswith(("https://", "http://")):
        raw = urlparse(raw).path
    elif raw.startswith("/"):
        pass
    elif re.fullmatch(r"[A-Za-z0-9._~%+@/-]+", raw) and "/" in raw:
        raw = "/" + raw
    else:
        return None
    raw = raw.split("#", 1)[0].split("?", 1)[0]
    return raw or "/"


def routes_named_by_index_surface(rel_path):
    path = os.path.join(BASE_DIR, rel_path)
    body = read_file(rel_path)
    routes = set()
    if rel_path.endswith(".json"):
        data = json.loads(body)

        def visit(value):
            if isinstance(value, dict):
                for nested in value.values():
                    visit(nested)
            elif isinstance(value, list):
                for nested in value:
                    visit(nested)
            else:
                route = normalize_index_route(value)
                if route:
                    routes.add(route)

        visit(data)
        return routes

    if rel_path.endswith(".xml"):
        for location in re.findall(r"<loc>(.*?)</loc>", body, flags=re.IGNORECASE | re.DOTALL):
            route = normalize_index_route(location)
            if route:
                routes.add(route)
        return routes

    base_href = extract_base_href(body)
    for href in extract_hrefs(body):
        if href.startswith(("https://", "http://")):
            route = normalize_index_route(href)
            if route:
                routes.add(route)
            continue
        target, _ = resolve_link(rel_path, href, base_href)
        if target is None:
            continue
        try:
            rel = os.path.relpath(target, BASE_DIR).replace(os.sep, "/")
        except ValueError:
            continue
        if rel == "index.html":
            routes.add("/")
        elif rel.endswith("/index.html"):
            routes.add("/" + rel)
            routes.add("/" + rel[:-10])
        elif os.path.isdir(target) or href.split("#", 1)[0].endswith("/"):
            routes.add("/" + rel.rstrip("/") + "/")
        else:
            routes.add("/" + rel)
    return routes


def check_historical_public_boundary():
    print("\n[10] Historical public-withholding boundary")
    all_ok = True
    try:
        registry = load_withheld_registry()
    except Exception as exc:
        error(f"withheld-routes.json is not valid JSON: {exc}")
        return False

    entries = registry.get("artifacts", [])
    registered = [item.get("artifact") for item in entries]
    registered_artifacts = set(registered)
    if registry.get("schemaVersion") != 2:
        error("withheld-routes.json must use schemaVersion 2")
        all_ok = False
    policy = registry.get("policy", {})
    try:
        # The withholding builder owns the exact supported rule vocabulary.
        # Import lazily: the parity checker imports this module for deployment
        # semantics, while the full release gate reaches this branch only after
        # module initialization is complete.
        from build_withholding_boundary import POLICY_RULE_IDS
        expected_policy_rules = set(POLICY_RULE_IDS)
    except Exception as exc:
        error(f"cannot load exact withholding-policy rules: {exc}")
        return False
    if policy.get("mode") != "exact-artifact fail-closed" or set(policy.get("rules", [])) != expected_policy_rules:
        error("withheld-routes.json fail-closed policy contract drift")
        all_ok = False
    if not registered or None in registered_artifacts or len(registered) != len(registered_artifacts):
        error("withheld-routes.json must name a non-empty unique artifact set")
        all_ok = False
    else:
        ok(f"withholding registry names {len(entries)} exact historical artifacts")

    build_check = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "build_withholding_boundary.py"), "--check"],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if build_check.returncode:
        error(build_check.stdout.strip() or build_check.stderr.strip() or "withholding boundary drift")
        all_ok = False
    else:
        ok(build_check.stdout.strip())

    boundary = registry.get("boundary", {})
    boundary_artifact = boundary.get("artifactRoute", "")
    boundary_public_route = boundary.get("publicRoute", "")
    marker = boundary.get("marker", "")
    boundary_path = os.path.join(BASE_DIR, boundary_artifact)
    if not os.path.exists(boundary_path):
        error(f"historical boundary page missing: {boundary_artifact}")
        all_ok = False
    else:
        boundary_body = read_file(boundary_artifact)
        required_boundary_markers = [
            marker,
            'name="robots" content="noindex, noarchive, nosnippet, nofollow"',
            'http-equiv="Cache-Control" content="no-store, max-age=0"',
            "preserved, not published",
        ]
        missing_markers = [value for value in required_boundary_markers if not value or value not in boundary_body]
        if missing_markers:
            error(f"historical boundary page missing marker(s): {missing_markers}")
            all_ok = False
        else:
            ok("historical boundary page is explicit, noindex, and no-store")

    patterns = load_vercelignore_patterns() or []
    for item in entries:
        artifact = item.get("artifact", "")
        if not artifact or artifact.startswith("/") or ".." in artifact.split("/"):
            error(f"unsafe artifact path in withholding registry: {artifact!r}")
            all_ok = False
            continue
        path = os.path.join(BASE_DIR, artifact)
        if not os.path.isfile(path):
            error(f"withheld artifact missing from git worktree: {artifact}")
            all_ok = False
            continue
        with open(path, "rb") as fh:
            current_bytes = fh.read()
        actual_hash = hashlib.sha256(current_bytes).hexdigest()
        actual_size = len(current_bytes)
        if actual_hash != item.get("sha256") or actual_size != item.get("bytes"):
            error(
                f"withheld artifact custody drift: {artifact} "
                f"sha256={actual_hash} bytes={actual_size}"
            )
            all_ok = False

        git_path = f"12_PUBLIC_SITE/{artifact}"
        process = subprocess.run(
            ["git", "-C", REPO_DIR, "show", f"HEAD:{git_path}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if process.returncode:
            error(f"withheld artifact is not present at HEAD: {git_path}")
            all_ok = False
        else:
            head_hash = hashlib.sha256(process.stdout).hexdigest()
            if head_hash != actual_hash or len(process.stdout) != actual_size:
                error(f"withheld artifact differs from HEAD custody: {artifact}")
                all_ok = False

        if artifact not in patterns or not is_vercel_ignored(artifact, patterns):
            error(f".vercelignore lacks exact withheld artifact exclusion: {artifact}")
            all_ok = False

    if all_ok:
        ok(f"all {len(entries)} artifact bytes match registered SHA-256, HEAD, and exact deploy exclusions")

    try:
        with open(os.path.join(BASE_DIR, "vercel.json"), "r", encoding="utf-8") as fh:
            vercel = json.load(fh)
    except Exception as exc:
        error(f"vercel.json is not valid JSON: {exc}")
        return False

    redirect_map = {
        rule.get("source"): rule
        for rule in vercel.get("redirects", [])
    }
    header_rules = vercel.get("headers", [])
    required_robots = {"noindex", "noarchive", "nosnippet"}
    all_public_routes = [boundary_public_route]
    for item in entries:
        all_public_routes.extend(item.get("publicRoutes", []))
        for route in item.get("publicRoutes", []):
            redirect = redirect_map.get(route, {})
            if redirect.get("destination") != boundary_public_route or redirect.get("permanent") is not False:
                error(f"withheld route lacks exact reversible boundary redirect: {route}")
                all_ok = False

    for route in all_public_routes:
        route_headers = {}
        for rule in header_rules:
            if header_source_covers(rule.get("source", ""), route):
                for header in rule.get("headers", []):
                    route_headers[header.get("key", "").lower()] = header.get("value", "")
        robots = {token.strip().lower() for token in route_headers.get("x-robots-tag", "").split(",")}
        cache_control = route_headers.get("cache-control", "").lower()
        cdn_cache_control = route_headers.get("cdn-cache-control", "").lower()
        if not required_robots.issubset(robots):
            error(f"withheld route lacks noindex/noarchive/nosnippet headers: {route}")
            all_ok = False
        if "no-store" not in cache_control or "no-store" not in cdn_cache_control:
            error(f"withheld route lacks browser/CDN no-store headers: {route}")
            all_ok = False

    index_surfaces = [
        "reading-manifest.json",
        "atlas/index.html",
        "atlas/site_index.json",
        "sitemap.xml",
        "book/rag_index.json",
        "read/index.html",
        "canon/index.html",
        "operators/index.html",
    ]
    # An exact withheld artifact is not a current index/search surface.  Its
    # bytes remain checked above for custody and headers, while its old links do
    # not govern the current public journey.
    index_surfaces = [
        surface
        for surface in index_surfaces
        if surface not in registered_artifacts and not is_vercel_ignored(surface, patterns)
    ]
    withheld_public_routes = {
        route
        for item in entries
        for route in item.get("publicRoutes", [])
    }
    for surface in index_surfaces:
        try:
            named_routes = routes_named_by_index_surface(surface)
        except Exception as exc:
            error(f"cannot inspect index/search surface {surface}: {exc}")
            all_ok = False
            continue
        leaked_routes = sorted(withheld_public_routes & named_routes)
        for route in leaked_routes:
            error(f"withheld route remains in current index/search surface: {surface} -> {route}")
            all_ok = False

    # Redirects are not a substitute for a truthful public link graph.  Every
    # deployable HTML page, including noindex provenance pages, must send a
    # withheld route to the explicit historical boundary rather than quietly
    # reviving it through an old navigation or inline source link.
    public_link_leaks = []
    for surface in get_public_html_files():
        try:
            named_routes = routes_named_by_index_surface(surface)
        except Exception as exc:
            error(f"cannot inspect public link surface {surface}: {exc}")
            all_ok = False
            continue
        for route in sorted(withheld_public_routes & named_routes):
            public_link_leaks.append((surface, route))
    if public_link_leaks:
        for surface, route in public_link_leaks:
            error(f"withheld route remains linked from deployable HTML: {surface} -> {route}")
        all_ok = False
    else:
        ok(f"no deployable HTML link revives an exact withheld route ({len(get_public_html_files())} pages checked)")

    sitemap_body = read_file("sitemap.xml")
    if boundary_public_route in sitemap_body:
        error("noindex historical boundary must not be advertised in sitemap.xml")
        all_ok = False

    service_worker = read_file("sw.js")
    if "WITHHELD_ROUTES" not in service_worker or "isWithheldRoute" not in service_worker:
        error("service worker lacks the explicit withheld-route cache bypass")
        all_ok = False
    for route in sorted(set(all_public_routes)):
        if route not in service_worker:
            error(f"service worker withheld-route registry missing: {route}")
            all_ok = False

    if all_ok:
        ok("reversible redirects, headers, indexes, search, sitemap, and service-worker boundary agree")
    return all_ok

def check_publication_boundary():
    print("\n[11] Deployment publication boundary")
    patterns = load_vercelignore_patterns()
    if patterns is None:
        error(".vercelignore missing")
        return False

    required_patterns = {
        "book-pwa/",
        "90_ARCHIVE/",
        "_archive/",
        "_STAGING_COMPASS_RESTRUCTURE/",
        "docs/",
        "__pycache__/",
        "*.py",
        "*.sh",
        "*.md",
        ".env",
        ".env.*",
        "*.db",
        "*.tsbuildinfo",
    }
    missing = sorted(required_patterns - set(patterns))
    if missing:
        for pattern in missing:
            error(f".vercelignore missing required pattern: {pattern}")
        return False

    risky_paths = [
        "book-pwa/.env",
        "book-pwa/dev.db",
        "book-pwa/README.md",
        "docs/superpowers/README.md",
        "_STAGING_COMPASS_RESTRUCTURE/00_COMPASS_RESTRUCTURE_RECEIPT.md",
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        "00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md",
        "generate_public_library.py",
        "predeploy_check.py",
        "predeploy_check.sh",
        "audit_live_domain_against_manifest.py",
        "withheld-routes.json",
        "deploy.sh",
        "deploy_vercel.sh",
        "deploy_target_contract.py",
        "__pycache__/predeploy_check.cpython-311.pyc",
        "compass/_archive/index_2026_07_12_pre_restructure.html",
        "a/b/_archive/c.html",
    ]
    leaked = [rel for rel in risky_paths if not is_vercel_ignored(rel, patterns)]
    if leaked:
        for rel in leaked:
            error(f"publication boundary would not ignore: {rel}")
        return False

    safe_paths = [
        "_archiveish/index.html",
        "compass/_archiveish/index.html",
        "compass/archive/index.html",
        "_archive.html",
    ]
    overmatched = [rel for rel in safe_paths if is_vercel_ignored(rel, patterns)]
    if overmatched:
        for rel in overmatched:
            error(f"publication boundary overmatches safe path: {rel}")
        return False

    vercel_entry = read_file("deploy_vercel.sh")
    for marker in (
        ".vercel/project.json",
        "deploy_target_contract.py",
        "--vercel-link",
        "predeploy_check.py",
        "check_site_build_artifacts.py",
        "exec vercel --prod --yes",
    ):
        if marker not in vercel_entry:
            error(f"Vercel entrypoint lacks fail-closed marker: {marker}")
            return False
    target_contract = read_file("deploy_target_contract.py")
    for marker in (
        "EMERGENTISM_VERCEL_PROJECT_ID_PIN",
        "EMERGENTISM_VERCEL_ORG_ID_PIN",
        "hmac.compare_digest",
        "--self-test",
    ):
        if marker not in target_contract:
            error(f"Vercel target contract lacks explicit-pin marker: {marker}")
            return False

    fallback = read_file("deploy.sh")
    if "--delete-excluded" in fallback:
        error("fallback deploy still uses global excluded-file deletion")
        return False
    for marker in (
        ".emergentism-static-target-v1",
        "emergentism.org-static-target-v1",
        "emergentism-static-v1)/releases/",
        "mkdir '${RELEASE_PATH}'",
        'rsync "${RSYNC_ARGS[@]}" --',
        "--self-test",
        "No live symlink, domain, or DNS target was changed",
    ):
        if marker not in fallback:
            error(f"fallback deploy lacks versioned-target guard: {marker}")
            return False

    book_ai = read_file("assets/js/book-ai.js")
    for marker in (
        "key-free book",
        'fetch("/book/rag_index.json")',
        "textContent",
        "no external endpoint",
    ):
        if marker not in book_ai:
            error(f"current book retrieval lacks key-free marker: {marker}")
            return False
    for forbidden in (
        "localStorage",
        "x-api-key",
        "anthropic-dangerous-direct-browser-access",
        "headers.authorization",
        "fetch(c.url",
        'type: "password"',
        "Endpoint URL",
        '"Bearer "',
    ):
        if forbidden in book_ai:
            error(f"current book public asset still exposes browser credential flow: {forbidden}")
            return False

    for command, label in (
        (["bash", os.path.join(BASE_DIR, "deploy.sh"), "--self-test"], "fallback target contract"),
        (["bash", os.path.join(BASE_DIR, "deploy_vercel.sh"), "--self-test"], "Vercel target contract"),
    ):
        process = subprocess.run(
            command,
            cwd=BASE_DIR,
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if process.returncode:
            error((process.stdout + process.stderr).strip() or f"{label} self-test failed")
            return False

    ok(".vercelignore, key-free retrieval, and fail-closed deployment entrypoints agree")
    return True

def check_semantic_parity():
    print("\n[12] Dimension-first semantic parity")
    process = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "check_public_semantic_parity.py")],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        for line in (process.stdout + process.stderr).strip().splitlines():
            error(line)
        return False
    ok(process.stdout.strip())
    return True

def check_claim_card_contract():
    print("\n[13] Claim-card and lifecycle contract")
    commands = (
        [sys.executable, os.path.join(REPO_DIR, "09_TOOLS/02_COMPILERS/compile_claim_cards.py"), "--check"],
        [sys.executable, os.path.join(REPO_DIR, "09_TOOLS/01_SCRIPTS/check_barred_claims.py"), "--scope", "all"],
        [sys.executable, os.path.join(REPO_DIR, "09_TOOLS/01_SCRIPTS/check_node_product_ranking.py")],
    )
    all_ok = True
    for command in commands:
        process = subprocess.run(command, cwd=REPO_DIR, text=True, capture_output=True, check=False)
        if process.returncode:
            all_ok = False
            for line in (process.stdout + process.stderr).strip().splitlines():
                error(line)
        else:
            ok(process.stdout.strip())
    return all_ok

def check_public_book_build():
    print("\n[14] Deterministic public-book build")
    process = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "build_book.py"), "--check"],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        for line in (process.stdout + process.stderr).strip().splitlines():
            error(line)
        return False
    ok(process.stdout.strip())
    return True

def check_reading_manifest_contract():
    print("\n[15] Reading-manifest lifecycle contract")
    process = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, "refresh_reading_manifest.py"), "--check"],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        for line in (process.stdout + process.stderr).strip().splitlines():
            error(line)
        return False
    ok(process.stdout.strip())
    return True


def check_contact_limited_lifecycle():
    print("\n[16] Contact-limited public lifecycle closure")
    checker = os.path.join(
        REPO_DIR, "09_TOOLS", "01_SCRIPTS", "check_contact_limited.py"
    )
    process = subprocess.run(
        [sys.executable, "-B", checker],
        cwd=REPO_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        for line in (process.stdout + process.stderr).strip().splitlines():
            error(line)
        return False
    summary = process.stdout.strip().splitlines()
    ok(summary[0] if summary else "contact-limited lifecycle ratchet passed")
    return True

def main():
    print("=" * 60)
    print("Pre-deploy supply-chain gate — 12_PUBLIC_SITE")
    print("=" * 60)

    results = [
        check_external_refs(),
        check_internal_links(),
        check_orphans(),
        check_required_assets(),
        check_html_wellformedness(),
        check_tier_markers(),
        check_operator_tier_hygiene(),
        check_public_reading_bundle(),
        check_generated_library_chrome(),
        check_historical_public_boundary(),
        check_publication_boundary(),
        check_semantic_parity(),
        check_claim_card_contract(),
        check_public_book_build(),
        check_reading_manifest_contract(),
        check_contact_limited_lifecycle(),
    ]

    # `results` was built and never read: the exit decision used only the global ERRORS
    # list, so any check that returned False WITHOUT appending to ERRORS was silently
    # ignored and the deploy went green. Fold the returned verdicts into the same
    # condition. Only an explicit False counts, so a check that returns None (no explicit
    # return) is not treated as a failure it never claimed.
    failed = [i for i, r in enumerate(results) if r is False]

    print("\n" + "=" * 60)
    if ERRORS or failed:
        if failed and not ERRORS:
            print(
                f"FAIL: {len(failed)} check(s) returned False without recording an error "
                f"(indices {failed}). A check that fails silently is a deploy hole."
            )
        print(f"FAIL: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        sys.exit(1)
    elif WARNINGS:
        print(f"PASS with warnings: {len(WARNINGS)} warning(s)")
        sys.exit(0)
    else:
        print("PASS: all checks green")
        sys.exit(0)

if __name__ == "__main__":
    main()
