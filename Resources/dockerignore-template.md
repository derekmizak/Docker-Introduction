# .dockerignore Templates (2025 Edition)

**Last Updated:** October 2025
**Purpose:** Optimize Docker build context and exclude unnecessary files

---

## 📋 What is .dockerignore?

The `.dockerignore` file tells Docker which files and directories to exclude when building images. It works like `.gitignore` but for Docker builds.

### Why use .dockerignore?

✅ **Faster builds** - Smaller build context = faster uploads to Docker daemon
✅ **Smaller images** - Excludes unnecessary files from final image
✅ **Security** - Prevents secrets and sensitive files from being copied
✅ **Cache optimization** - Better layer caching

### Where to place it?

Place `.dockerignore` in the **same directory as your Dockerfile** (usually project root).

```
my-project/
├── .dockerignore     ← Place here
├── Dockerfile
├── src/
└── package.json
```

---

## 🎯 Universal .dockerignore Template

Use this as a starting point for any project:

```dockerignore
# Git
.git
.gitignore
.gitattributes
.github

# CI/CD
.gitlab-ci.yml
.travis.yml
.circleci
Jenkinsfile

# Documentation
README.md
CHANGELOG.md
CONTRIBUTING.md
LICENSE
*.md
docs/

# Editor and IDE
.vscode
.idea
.DS_Store
*.swp
*.swo
*~
.project
.settings
.classpath

# Environment files (IMPORTANT - contains secrets!)
.env
.env.local
.env.*.local
.env.development
.env.production
.env.test
*.env

# Secrets and credentials (CRITICAL!)
secrets/
*.key
*.pem
*.p12
*.pfx
credentials.json
service-account.json

# Build artifacts
dist/
build/
out/
target/
*.log

# Testing
test/
tests/
spec/
*.test.js
*.spec.js
coverage/
.nyc_output
jest.config.js

# Docker
docker-compose*.yml
Dockerfile*
.dockerignore

# Temporary files
tmp/
temp/
*.tmp
*.bak
*.cache
```

---

## 📦 Language-Specific Templates

### Node.js / JavaScript

```dockerignore
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
.npm
.yarn

# Testing
coverage/
.nyc_output
__tests__
**/*.test.js
**/*.spec.js
jest.config.js
vitest.config.js

# Build tools
.eslintrc*
.prettierrc*
.babelrc*
webpack.config.js
rollup.config.js
tsconfig.json

# Environment
.env*
!.env.example

# Editor
.vscode
.idea
*.swp

# Git
.git
.gitignore

# Documentation
README.md
CHANGELOG.md
docs/

# CI/CD
.github
.gitlab-ci.yml

# macOS
.DS_Store

# Logs
logs/
*.log
npm-debug.log*

# Build output (include only if not needed in image)
# dist/
# build/
```

### Python

```dockerignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
venv/
env/
ENV/
.venv
*.egg-info/
dist/
build/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Jupyter
.ipynb_checkpoints
*.ipynb

# Environment
.env*
!.env.example

# Editor
.vscode
.idea
*.swp

# Git
.git
.gitignore

# Documentation
README.md
docs/
*.md

# CI/CD
.github
.gitlab-ci.yml

# mypy
.mypy_cache/
.dmypy.json

# pytest
pytest.ini
.pytest.ini

# Requirements (if copying individually)
# requirements-dev.txt
# requirements-test.txt
```

### Go

```dockerignore
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib
bin/
build/

# Test binary
*.test

# Output of go coverage tool
*.out
coverage/

# Dependency directories
vendor/

# Go workspace file
go.work

# Environment
.env*
!.env.example

# Editor
.vscode
.idea
*.swp

# Git
.git
.gitignore

# Documentation
README.md
docs/
*.md

# CI/CD
.github
.gitlab-ci.yml

# Testing
*_test.go
testdata/
```

### Java / Spring Boot

```dockerignore
# Build artifacts
target/
build/
out/
*.class

# Gradle
.gradle/
gradle/
gradlew
gradlew.bat

# Maven
.mvn/
mvnw
mvnw.cmd
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup

# IDE
.idea/
*.iml
.classpath
.project
.settings/
*.iws

# Testing
test/
src/test/

# Logs
*.log
logs/

# Environment
.env*
!.env.example

# Git
.git
.gitignore

# Documentation
README.md
docs/
*.md

# CI/CD
.github
.gitlab-ci.yml
Jenkinsfile
```

### .NET / C#

```dockerignore
# Build results
[Dd]ebug/
[Dd]ebugPublic/
[Rr]elease/
[Rr]eleases/
x64/
x86/
[Ww][Ii][Nn]32/
[Aa][Rr][Mm]/
[Aa][Rr][Mm]64/
bld/
[Bb]in/
[Oo]bj/
[Ll]og/
[Ll]ogs/

# Visual Studio
.vs/
*.user
*.userosscache
*.suo
*.sln.docstates

# NuGet
*.nupkg
*.snupkg
packages/
.nuget/

# Testing
[Tt]est[Rr]esult*/
[Bb]uild[Ll]og.*
*.trx
*.coverage
*.coveragexml

# Environment
.env*
!.env.example

# Git
.git
.gitignore

# Documentation
README.md
docs/
*.md

# CI/CD
.github
azure-pipelines.yml
```

### PHP

```dockerignore
# Dependencies
vendor/
composer.phar
composer.lock

# Testing
tests/
phpunit.xml
.phpunit.result.cache

# Build
build/

# Laravel specific
storage/
bootstrap/cache/
.env*
!.env.example

# Logs
*.log

# Editor
.vscode
.idea
*.swp

# Git
.git
.gitignore

# Documentation
README.md
docs/
*.md

# CI/CD
.github
.gitlab-ci.yml

# PHP
*.cache
```

---

## 🎨 Framework-Specific Templates

### React / Next.js

```dockerignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
__tests__/
**/*.test.js
**/*.test.jsx
**/*.test.tsx

# Next.js
.next/
out/

# Build
build/
dist/

# Environment
.env*
!.env.example

# Vercel
.vercel

# Editor
.vscode
.idea

# Git
.git
.gitignore

# Documentation
README.md
*.md

# Config files
.eslintrc.json
.prettierrc
tsconfig.json
next.config.js

# Logs
*.log
npm-debug.log*
```

### Vue.js

```dockerignore
# Dependencies
node_modules/

# Build
dist/
dist-ssr/

# Testing
tests/
coverage/

# Environment
.env*
!.env.example

# Editor
.vscode
.idea

# Git
.git
.gitignore

# Documentation
README.md

# Config
vite.config.js
vue.config.js
tsconfig.json
```

### Django

```dockerignore
# Python
__pycache__/
*.py[cod]
*.pyc

# Virtual environment
venv/
env/
.venv/

# Database
*.sqlite3
db.sqlite3

# Media files (if not needed in image)
media/

# Static files (if collecting in container)
staticfiles/

# Testing
.pytest_cache/
.coverage

# Environment
.env*
!.env.example
local_settings.py

# Editor
.vscode
.idea

# Git
.git
.gitignore

# Documentation
README.md
docs/
```

---

## 🔒 Security-Focused .dockerignore

For maximum security, use this template:

```dockerignore
# CRITICAL: Secrets and credentials
.env*
!.env.example
secrets/
*.key
*.pem
*.p12
*.pfx
*.crt
*.cert
credentials.json
service-account.json
auth.json
.aws/
.gcloud/
.azure/
.kube/
.ssh/

# CRITICAL: Environment files
.env
.env.local
.env.development
.env.production
.env.test
.env.*.local

# Development tools (potential attack surface)
node_modules/
venv/
.git/

# Testing (not needed in production)
test/
tests/
__tests__/
spec/
*.test.*
*.spec.*
coverage/

# CI/CD (may contain sensitive info)
.github/
.gitlab-ci.yml
.travis.yml
.circleci/
azure-pipelines.yml
Jenkinsfile

# Editor (may contain sensitive settings)
.vscode/
.idea/
*.swp

# Documentation (info disclosure)
README.md
CHANGELOG.md
docs/
*.md

# Source control
.git/
.gitignore
.gitattributes

# Logs (may contain sensitive data)
*.log
logs/
npm-debug.log*
```

---

## 📝 Best Practices

### 1. Start Broad, Then Exclude

```dockerignore
# Ignore everything
**

# Then allow what's needed
!src/
!package.json
!package-lock.json
!tsconfig.json
```

### 2. Use Comments

```dockerignore
# Dependencies - These will be installed via npm ci
node_modules/

# Testing - Not needed in production
test/
coverage/

# Build artifacts - Will be generated during build
dist/
```

### 3. Exclude Build Context vs Image Content

```dockerfile
# .dockerignore - Exclude from build context
tests/
docs/
.git/

# Dockerfile - Control what goes in image
COPY package*.json ./
RUN npm ci --only=production  # Only prod dependencies
COPY src/ ./src/              # Only source code
# Don't copy tests, docs, etc.
```

### 4. Test Your .dockerignore

```bash
# See what's in build context
docker build --no-cache -t test . 2>&1 | grep "Sending build context"

# Should see reduced size with .dockerignore
```

### 5. Use .dockerignore for Multi-Stage Builds

```dockerignore
# Exclude heavy items from build stage
node_modules/

# But keep source code for building
!src/
!package*.json
```

---

## 🚀 Template Generator

Use this decision tree to choose a template:

```
What language are you using?
├── JavaScript/TypeScript
│   ├── Framework?
│   │   ├── React → Use React template
│   │   ├── Next.js → Use Next.js template
│   │   ├── Vue → Use Vue template
│   │   └── Other → Use Node.js template
│   └── No framework → Use Node.js template
│
├── Python
│   ├── Framework?
│   │   ├── Django → Use Django template
│   │   ├── Flask → Use Python template + Flask specifics
│   │   └── Other → Use Python template
│   └── No framework → Use Python template
│
├── Go → Use Go template
├── Java → Use Java/Spring Boot template
├── .NET/C# → Use .NET template
├── PHP → Use PHP template
└── Other → Use Universal template
```

---

## ✅ Verification Checklist

After creating .dockerignore:

- [ ] **File is in the correct location** (same dir as Dockerfile)
- [ ] **Excludes secrets** (.env, *.key, *.pem)
- [ ] **Excludes development dependencies** (node_modules, venv)
- [ ] **Excludes testing files** (test/, coverage/)
- [ ] **Excludes documentation** (README.md, docs/)
- [ ] **Excludes version control** (.git/)
- [ ] **Excludes editor files** (.vscode, .idea)
- [ ] **Build context size reduced** (verify with build output)

```bash
# Verify build context size
docker build --no-cache -t myapp:latest . 2>&1 | grep "Sending build context"

# Before .dockerignore:
# Sending build context to Docker daemon  2.5GB

# After .dockerignore:
# Sending build context to Docker daemon  50MB  ✅
```

---

## 🔍 Common Mistakes

### ❌ Mistake 1: Excluding Required Files

```dockerignore
# ❌ BAD - Excludes package.json needed for npm install!
*.json

# ✅ GOOD - Be specific
tsconfig.json
jest.config.json
# Keep package.json and package-lock.json
```

### ❌ Mistake 2: Wrong File Location

```bash
# ❌ WRONG
src/.dockerignore    # Won't work here!

# ✅ CORRECT
.dockerignore        # Same level as Dockerfile
Dockerfile
```

### ❌ Mistake 3: Forgetting Wildcards

```dockerignore
# ❌ BAD - Only ignores root .env
.env

# ✅ GOOD - Ignores all .env files
.env*
**/.env*
```

### ❌ Mistake 4: Not Excluding Secrets

```dockerignore
# ❌ MISSING CRITICAL EXCLUSIONS
# No .env
# No *.key
# No secrets/

# ✅ GOOD
.env*
*.key
*.pem
secrets/
```

---

## 📖 Examples from Real Projects

### Minimal Microservice (Node.js)

```dockerignore
node_modules
npm-debug.log
.env*
!.env.example
README.md
.git
.vscode
test
coverage
```

### Full-Stack Application

```dockerignore
# Frontend
frontend/node_modules
frontend/dist
frontend/.next

# Backend
backend/node_modules
backend/dist

# Shared
.env*
!.env.example
.git
.vscode
.idea
*.log
README.md
docker-compose.yml
```

### Python Data Science Project

```dockerignore
__pycache__
*.pyc
venv/
.venv/
.env*
notebooks/
data/raw/
data/processed/
models/experiments/
.git
.vscode
README.md
```

---

## 📚 Additional Resources

- [Official Docker Documentation](https://docs.docker.com/engine/reference/builder/#dockerignore-file)
- [.dockerignore Pattern Reference](https://docs.docker.com/engine/reference/builder/#dockerignore-file)
- [GitHub .dockerignore Examples](https://github.com/search?q=filename:.dockerignore)

---

## 🎓 Quick Reference Card

```
.dockerignore QUICK REFERENCE

SYNTAX:
# Comment
*           Match everything
**          Match zero or more directories
?           Match single character
!pattern    Negate pattern (include)

MUST EXCLUDE:
✅ .env* (secrets)
✅ *.key, *.pem (credentials)
✅ node_modules/ (dependencies)
✅ .git/ (version control)
✅ test/, coverage/ (testing)
✅ README.md, docs/ (documentation)
✅ .vscode/, .idea/ (editor)

LOCATION:
.dockerignore must be in same directory as Dockerfile

VERIFY:
docker build . 2>&1 | grep "Sending build context"
```

---

**Version:** 1.0 | **Last Updated:** October 2025
**Maintained by:** Docker Course Team

**Always create a .dockerignore before building images!**
