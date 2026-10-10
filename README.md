# agent-skills

직접 만든 Codex 스킬을 관리하는 개인 저장소입니다. 이 저장소의 `skills/`가 편집 원본이며, Codex 설치 위치에는 각 폴더의 심볼릭 링크를 둡니다.

## 관리하는 스킬

| 스킬 | 용도 |
| --- | --- |
| [jd-introduce](skills/jd-introduce/SKILL.md) | 채용 공고와 실제 경험을 연결한 짧은 지원 소개 |
| [project-portfolio](skills/project-portfolio/SKILL.md) | 판단 근거와 본인 기여가 드러나는 프로젝트 포트폴리오 |
| [resume-portfolio-review](skills/resume-portfolio-review/SKILL.md) | 이력서와 포트폴리오의 기여·성과·일관성·링크 검토 |
| [todoist-plan-tasks](skills/todoist-plan-tasks/SKILL.md) | 최신 운영 원칙에 맞춰 Todoist 할 일 추가 |

경험 기록, 회고, 운영 원칙의 원본은 `personal-record`에 둡니다. 이곳에는 그 자료를 사용하는 절차와 필요한 도구만 관리합니다. 외부에서 설치한 스킬과 시스템·플러그인 스킬은 각 설치 경로에서 관리합니다.

## 설치

Python 3만 있으면 됩니다. 저장소를 원하는 경로에 클론한 뒤 실행합니다.

```sh
git clone git@github.com:zzoe2346/agent-skills.git
cd agent-skills
python3 scripts/link_skills.py
```

기본 설치 위치는 현재 사용 중인 `${CODEX_HOME:-~/.codex}/skills`입니다. 이미 같은 저장소를 가리키는 링크가 있으면 그대로 두고, 다른 파일이나 폴더가 있으면 덮어쓰지 않고 중단합니다.

기존 복사본을 보관하고 링크로 전환하려면 먼저 변경 예정 항목을 확인한 뒤 실행합니다.

```sh
python3 scripts/link_skills.py --backup-existing --dry-run
python3 scripts/link_skills.py --backup-existing
```

기존 항목은 `~/.codex/skill-backups/agent-skills/<실행 시각>/` 아래에 보관됩니다. 이 백업은 스킬 검색 경로 밖에 있습니다.

[현재 공식 문서](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)의 사용자 스킬 경로 `~/.agents/skills`를 쓰는 환경에서는 설치 위치를 지정합니다. 같은 스킬을 두 검색 경로에 중복 설치하지 않습니다.

```sh
python3 scripts/link_skills.py --target-dir "$HOME/.agents/skills"
```

Codex는 스킬 변경을 자동으로 감지합니다. 목록이 갱신되지 않으면 앱을 다시 시작합니다.

## 개인 경로 설정

Todoist 스킬은 매번 `personal-record`의 `2_Areas/일상과 회고/운영 원칙.md`를 읽습니다. 원칙 내용을 이 저장소에 복사하지 않습니다.

볼트 경로는 다음 순서로 결정합니다.

1. `PERSONAL_RECORD_VAULT` 환경 변수
2. 이 저장소의 `config/local.json`에 있는 `personal_record_vault`
3. 기본값 `~/repo/personal-record`

필요하면 [config/local.example.json](config/local.example.json)을 `config/local.json`으로 복사하고 경로를 수정합니다. `local.json`은 Git에서 제외합니다. 환경 변수와 설정 파일의 경로에는 절대 경로 또는 `~/` 경로를 사용합니다.

## 수정과 동기화

`skills/<이름>/SKILL.md`와 그 폴더의 보조 파일을 수정한 뒤 커밋하고 푸시합니다. 링크로 설치된 환경은 별도 복사 없이 수정된 원본을 읽습니다. 다른 컴퓨터에서는 `git pull`로 갱신합니다. 새 스킬을 추가했다면 설치 스크립트를 다시 실행합니다.

각 스킬은 하나의 작업에 집중합니다. 사용 범위는 `SKILL.md`의 설명에, 실행 절차는 본문에, 긴 참고 자료는 `references/`에 둡니다. UI 정보와 자동 선택 정책은 `agents/openai.yaml`에서 관리합니다.
