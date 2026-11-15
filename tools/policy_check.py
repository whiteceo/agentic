"""정책 합침 검사(실행_연결.md 10절 2 ~ 4번)의 기준 구현.

테넌트 정책(policies/tenant.yaml)과 도메인 정책(agentic-env.yaml)을 견주어
- 도메인 값이 테넌트보다 느슨하면 실패
- 모르는 키(합치는 규칙이 없는 키)가 있으면 실패
- 보관 기간이 자료 종류마다 바닥 > 천장이면 실패
하고, 줄마다 출처 파일을 붙인 실효 정책 표를 낸다. 같은 입력이면 같은 결과다.

쓰는 법: python policy_check.py <tenant.yaml> <agentic-env.yaml>
끝 코드: 0 통과, 1 실패, 2 입력 오류.
YAML 읽기에 PyYAML이 필요하다(pip install pyyaml).
"""
import sys

# 키마다 합치는 규칙(관리_계층_설계.md 4-1). 여기 없는 키는 '모르는 키'다.
RULES = {
    "version": "ignore",
    "allowed_models": "intersect",       # 허용 목록: 교집합
    "blocked_data_classes": "union",     # 차단 목록: 합집합
    "cost_caps": "min_map",              # 상한: 가장 작은 값
    "gate_floors": "max_map",            # 바닥: 가장 큰 값
    "retention": "retention",            # 자료 종류마다 바닥(최대) · 천장(최소) · 근거
    "identity": "tenant_only",           # 단일 값: 테넌트만
}
# 도메인 파일에만 있고 테넌트 정책과 견주지 않는 도메인 고유 키(실행_연결.md 5절)
DOMAIN_ONLY = {"risk_a_categories", "agents", "gates", "domains", "org", "spec_repo",
               "app_repos", "github_plan", "main_branch", "teams", "blocking_categories",
               "release", "hotfix_declarers", "screen_prefix", "ci_token_secret",
               "options", "setup_done"}


def load(path):
    import yaml  # 지연 가져오기: 시험에서는 dict를 바로 넘긴다
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def merge(tenant, domain, tname="tenant", dname="domain"):
    errors, table = [], []
    for key in sorted(set(tenant) | set(domain)):
        if key in DOMAIN_ONLY and key not in tenant:
            continue
        rule = RULES.get(key)
        if rule is None:
            errors.append(f"모르는 키: {key}")
            continue
        t, d = tenant.get(key), domain.get(key)
        if rule == "ignore":
            continue
        if rule == "tenant_only":
            if d is not None and d != t:
                errors.append(f"{key}: 테넌트만 정하는 값인데 도메인이 바꿈({t!r} → {d!r})")
            table.append((key, t, tname))
        elif rule == "intersect":
            if d is None:
                table.append((key, t, tname))
            else:
                extra = set(d) - set(t or [])
                if extra:
                    errors.append(f"{key}: 테넌트가 허용하지 않은 값 {sorted(extra)}")
                table.append((key, sorted(set(d) & set(t or [])), dname))
        elif rule == "union":
            if d is not None and set(t or []) - set(d):
                errors.append(f"{key}: 테넌트가 막은 값을 도메인이 뺌 {sorted(set(t) - set(d))}")
            table.append((key, sorted(set(t or []) | set(d or [])), f"{tname}+{dname}"))
        elif rule in ("min_map", "max_map"):
            t, d = t or {}, d or {}
            for sub in sorted(set(t) | set(d)):
                tv, dv = t.get(sub), d.get(sub)
                if tv is not None and dv is not None:
                    looser = dv > tv if rule == "min_map" else dv < tv
                    if looser:
                        word = "상한이 큼" if rule == "min_map" else "바닥이 낮음"
                        errors.append(f"{key}.{sub}: 도메인 값 {dv}이 테넌트 {tv}보다 느슨함({word})")
                    pick = min(tv, dv) if rule == "min_map" else max(tv, dv)
                    src = tname if pick == tv else dname
                else:
                    pick, src = (tv, tname) if tv is not None else (dv, dname)
                table.append((f"{key}.{sub}", pick, src))
        elif rule == "retention":
            t, d = t or {}, d or {}
            for kind in sorted(set(t) | set(d)):
                tk, dk = t.get(kind, {}), d.get(kind, {})
                floor = max(x for x in (tk.get("floor_days"), dk.get("floor_days")) if x is not None) \
                    if (tk.get("floor_days") is not None or dk.get("floor_days") is not None) else None
                ceils = [x for x in (tk.get("ceiling_days"), dk.get("ceiling_days")) if x is not None]
                ceil = min(ceils) if ceils else None
                if dk.get("floor_days") is not None and tk.get("floor_days") is not None \
                        and dk["floor_days"] > tk["floor_days"] and not dk.get("basis"):
                    errors.append(f"retention.{kind}: 바닥을 올렸는데 근거(basis)가 빔")
                if floor is not None and ceil is not None and floor > ceil:
                    errors.append(f"retention.{kind}: 바닥 {floor}일 > 천장 {ceil}일")
                table.append((f"retention.{kind}", {"floor_days": floor, "ceiling_days": ceil},
                              f"{tname}+{dname}"))
    return errors, table


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        tenant, domain = load(argv[1]), load(argv[2])
    except Exception as e:  # 입력 오류는 실패와 나눈다
        print(f"입력 오류: {e}")
        return 2
    errors, table = merge(tenant, domain, argv[1], argv[2])
    print("| 키 | 실효 값 | 출처 |")
    print("| :--- | :--- | :--- |")
    for k, v, src in table:
        print(f"| {k} | {v} | {src} |")
    for e in errors:
        print(f"실패: {e}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
