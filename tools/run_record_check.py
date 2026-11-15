"""판정 리포트 기록 줄 검사(실행_연결.md 10절 6 · 7번)의 기준 구현.

판정 리포트(PR 코멘트 등) 본문에서 기계용 실행 기록 줄
  <!-- agentic-run: role=judge model=... skill=...@sha criteria=...@sha head=sha actor=... -->
을 찾아,
- 필수 칸(role · model · skill · criteria · head · actor)이 비었으면 실패
- 판정 수행자(actor)가 작성자(PR 작성자)와 같으면 실패
- 리포트의 기준 판(criteria)이 지금 기준 판과 다르면 경고(판정은 소급하지 않음)
을 낸다. 같은 입력이면 같은 결과다.

쓰는 법: python run_record_check.py <리포트 파일> <작성자> [지금 기준 판]
끝 코드: 0 통과(경고는 있을 수 있음), 1 실패.
"""
import re
import sys

REQUIRED = ("role", "model", "skill", "criteria", "head", "actor")
LINE = re.compile(r"<!--\s*agentic-run:(.*?)-->", re.S)


def parse(text):
    m = LINE.search(text)
    if not m:
        return None
    fields = {}
    for part in m.group(1).split():
        if "=" in part:
            k, v = part.split("=", 1)
            fields[k.strip()] = v.strip()
    return fields


def check(text, author, current_criteria=None):
    errors, warnings = [], []
    f = parse(text)
    if f is None:
        return ["기록 줄(agentic-run)이 없다. 기록 없는 AI 판정은 통과로 치지 않는다"], warnings
    for k in REQUIRED:
        if not f.get(k):
            errors.append(f"빈 칸: {k}")
    if f.get("actor") and author and f["actor"] == author:
        errors.append(f"판정 수행자({f['actor']})가 작성자와 같다")
    if current_criteria and f.get("criteria") and f["criteria"] != current_criteria:
        warnings.append(f"기준 판이 다르다: 리포트 {f['criteria']} · 지금 {current_criteria}"
                        " (소급하지 않음, 다시 할지는 도메인 결정자)")
    return errors, warnings


def main(argv):
    if len(argv) not in (3, 4):
        print(__doc__)
        return 1
    with open(argv[1], encoding="utf-8") as fp:
        text = fp.read()
    errors, warnings = check(text, argv[2], argv[3] if len(argv) == 4 else None)
    for w in warnings:
        print(f"경고: {w}")
    for e in errors:
        print(f"실패: {e}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
