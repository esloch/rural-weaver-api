# Backend Release Checklist

## Before release

- [ ] `git status` clean or reviewed.
- [ ] Migration exists for model changes.
- [ ] `alembic upgrade head` passes.
- [ ] API container builds.
- [ ] Relevant curl validations pass.
- [ ] Phase docs updated.
- [ ] API contract updated if endpoints changed.

## After release

- [ ] Active campaign endpoint works.
- [ ] Admin campaign endpoint works.
- [ ] Payment summary works.
- [ ] Financial summary works.
- [ ] CSV exports work if changed.
