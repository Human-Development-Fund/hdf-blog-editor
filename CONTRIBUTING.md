# Updating and releasing the skill

## Source of truth

Edit only:

```text
skill/hdf-blog-editor/
adapters/
tests/
documentation files
```

Never hand-edit files in `dist/`. They are generated release artifacts.

## Change process

1. Create a branch from the default branch.
2. Update the canonical skill or relevant documentation.
3. Add or update a realistic fixture when behavior changes.
4. Run:

   ```bash
   python3 tools/release.py check
   python3 tools/release.py build
   ```

5. Inspect the generated archives and `dist/release-manifest.json`.
6. Update `CHANGELOG.md` and `VERSION` using semantic versioning.
7. Recheck the platform model guidance and update the review date in `USAGE.md` for every minor or major release.
8. Request review from the HDF editorial owner.
9. Merge only after automated checks pass.
10. Tag the approved commit, for example `v1.0.1`.
11. Publish the generated files from `dist/` as release assets.

## Versioning

- **Patch:** clarification, typo or validation improvement without changing the expected handoff.
- **Minor:** new mode, new platform support or backward-compatible output improvement.
- **Major:** a change that materially alters activation, factual policy or the Full Retrofit contract.

## Review requirements

Every behavioral change should be reviewed for:

- Factual integrity and attribution.
- HDF voice and audience.
- WordPress practicality.
- Accessibility.
- Platform compatibility.
- Privacy and security.
- Whether it improves a repeated problem rather than one isolated preference.

## Release ownership

Assign one HDF owner to approve production releases and at least one backup reviewer. The owner should verify the changelog, test results and example outputs before a release is published.

## Rollback

Do not overwrite or delete previous release assets. If a release causes regressions, reinstall the prior known-good ZIP and issue a corrected patch release.
