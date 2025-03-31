monorepo/
├── .gitignore          # Global ignore rules
├── README.md           # Monorepo documentation
├── packages/           # Shared libraries/tools
│   ├── common-utils/   # Shared utilities (e.g., logging)
├── services/           # Deployable services
│   ├── api/            # Backend (Python/Go)
│   ├── web/            # Frontend (JavaScript/React)
│   ├── cli/            # CLI tool (Python/Go)
├── scripts/            # Build/deploy scripts
├── tools/              # Dev tools (e.g., linters)
└── docs/               # Documentation


monorepo/
├── services/
│   ├── python-service-1/      
│   │   ├── features/           # Cucumber feature files
│   │   └── step_definitions/    # Step implementations
│   ├── ts-service-1/
│   │   ├── features/           # Cucumber feature files
│   │   └── step_definitions/    # Step implementations
├── apps/
│   ├── react-app-1/
│   │   ├── e2e/                # End-to-end tests
│   │   │   ├── features/       # Cucumber feature files
│   │   │   └── step_definitions/
└── ... (rest remains same)