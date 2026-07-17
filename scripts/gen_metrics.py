"""Gera metrics.svg contando artefatos reais nos repositorios de asm444.

Cada barra e' um numero verificavel por quem clicar no repo. Nada e' auto-declarado:
a contagem vem da arvore de arquivos via API do GitHub, nunca de badge ou de README.
"""

import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
OWNER = "asm444"

# (rotulo, repo, caminho, predicado sobre o nome do arquivo)
# O predicado existe porque contar por extensao erra: conftest.py nao e' um modulo
# de teste, _openai-compat.js e' helper interno e nao um provedor.
METRICS = [
    ("Algebrow — test modules", "Algebrow", "tests",
     lambda n: n.startswith("TEST_") and n.endswith(".py")),
    ("down-news — services watched", "down-news", None, None),
    ("telinha — test modules", "smartClaude", "tests",
     lambda n: n.startswith("test_") and n.endswith(".py")),
    ("WhatsHeelper — compose services", "WhatsHeelper", None, None),
    ("model-chain-proxy — LLM providers", "model-chain-proxy", "providers",
     lambda n: n.endswith(".js") and not n.startswith("_")),
    ("maestro — department agents", "maestro", "agents",
     lambda n: n.endswith(".md")),
]

PALETTE = ["#1F6FEB", "#388BFD", "#58A6FF", "#79C0FF", "#A5D6FF", "#CAE8FF"]


def request(path, anonymous=False):
    """Chama a API do GitHub.

    anonymous=True omite o token de proposito: forca a resposta a ser a que um
    visitante nao autenticado veria. Sem isso, um token com acesso a repo privado
    devolve numero maior que o publico consegue conferir — e metrica que o leitor
    nao pode verificar nao entra no README.
    """
    req = urllib.request.Request(f"{API}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    token = os.environ.get("GITHUB_TOKEN")
    if token and not anonymous:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def count_dir(repo, path, predicate):
    entries = request(f"/repos/{OWNER}/{repo}/contents/{path}")
    return sum(1 for e in entries if e["type"] == "file" and predicate(e["name"]))


def count_yaml_top_keys(repo, path, section):
    """Conta chaves de 2 espacos sob `section:` num YAML.

    Regex aceita digito no nome de proposito: `n8n` e `office365` sao servicos reais
    e um padrao [a-z-]+ os descartaria em silencio.
    """
    import base64
    import re

    blob = request(f"/repos/{OWNER}/{repo}/contents/{path}")
    text = base64.b64decode(blob["content"]).decode("utf-8")
    body = re.search(rf"^{section}:\n(.*?)(?=^\S|\Z)", text, re.S | re.M)
    if not body:
        raise ValueError(f"secao '{section}:' nao encontrada em {repo}/{path}")
    return len(re.findall(r"^  ([A-Za-z0-9_.-]+):$", body.group(1), re.M))


def count_merged_prs():
    """Conta PRs do usuario MERGEADOS em repos de terceiros.

    So conta merged: um PR aberto ou fechado sem merge nao prova que o codigo
    foi aceito. Usa a Search API, que ve apenas repos publicos — e' de proposito:
    o numero tem de bater com o que um visitante anonimo consegue conferir.
    """
    data = request(
        "/search/issues?q=is:pr+author:asm444+-user:asm444+is:merged&per_page=1",
        anonymous=True,
    )
    return data["total_count"]


def collect():
    rows = []
    for label, repo, path, predicate in METRICS:
        if repo == "down-news":
            value = count_yaml_top_keys(repo, "config.yml", "services")
        elif repo == "WhatsHeelper":
            value = count_yaml_top_keys(repo, "docker-compose.yml", "services")
        else:
            value = count_dir(repo, path, predicate)
        rows.append((label, value, repo))
        print(f"{label}: {value}", file=sys.stderr)

    merged = count_merged_prs()
    rows.append(("PRs merged in others' repos", merged, None))
    print(f"PRs merged elsewhere: {merged}", file=sys.stderr)

    rows.sort(key=lambda r: -r[1])
    return rows


def render(rows):
    bar_h, gap, top, left, label_w, track = 26, 14, 58, 24, 290, 420
    height = top + len(rows) * (bar_h + gap) + 30
    width = left + label_w + track + 60
    peak = max(v for _, v, _ in rows)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Artifact counts measured from the repositories">',
        "<style>"
        ".t{font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;fill:#8B949E}"
        ".l{font-size:13px}.v{font-size:13px;fill:#C9D1D9;font-weight:600}"
        ".h{font-size:14px;fill:#C9D1D9;font-weight:600}"
        "@media(prefers-reduced-motion:reduce){.b{animation:none!important}}"
        ".b{transform-origin:left center;animation:g .9s cubic-bezier(.2,.8,.2,1) both}"
        "@keyframes g{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "</style>",
        f'<rect width="{width}" height="{height}" rx="8" fill="#0D1117"/>',
        f'<text x="{left}" y="30" class="t h">Counted from the repositories, not self-reported</text>',
    ]

    for i, (label, value, _) in enumerate(rows):
        y = top + i * (bar_h + gap)
        w = max(3, round(track * value / peak))
        color = PALETTE[i % len(PALETTE)]
        out.append(
            f'<text x="{left}" y="{y + 18}" class="t l" text-anchor="start">{label}</text>'
        )
        out.append(
            f'<rect x="{left + label_w}" y="{y + 3}" width="{track}" height="{bar_h - 6}" '
            f'rx="4" fill="#161B22"/>'
        )
        out.append(
            f'<rect class="b" x="{left + label_w}" y="{y + 3}" width="{w}" '
            f'height="{bar_h - 6}" rx="4" fill="{color}" '
            f'style="animation-delay:{i * 0.09:.2f}s"/>'
        )
        out.append(
            f'<text x="{left + label_w + w + 10}" y="{y + 18}" class="t v">{value}</text>'
        )

    out.append("</svg>")
    return "\n".join(out)


def main():
    try:
        rows = collect()
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as exc:
        print(f"falha ao coletar: {exc}", file=sys.stderr)
        return 1
    dest = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "metrics.svg")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(render(rows))
    print(f"escrito: {dest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
