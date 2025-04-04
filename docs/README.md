monorepo/
├── .gitignore          # Global ignore rules
├── README.md           # Monorepo documentation
├── packages/           # Shared libraries/tools
│   ├── common-utils/   # Shared utilities (e.g., logging)
├── services/           # Deployable services
│   ├── api/            # Backend (Python/Go)
│   ├── web/            # Frontend (JavaScript/React)
│   ├── cli/            # CLI tool (Python/Go)
├── apps/
├── scripts/            # Build/deploy scripts
├── tools/              # Dev tools (e.g., linters)
└── docs/               # Documentation