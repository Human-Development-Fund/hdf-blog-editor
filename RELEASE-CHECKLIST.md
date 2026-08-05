# Production release checklist

## Repository setup — once

- [ ] Confirm the GitHub owner and repository name.
- [ ] Choose public or private visibility deliberately.
- [ ] Add the approved licence.
- [ ] Enable a `main` branch ruleset requiring the **Validate and build** check.
- [ ] Require at least one CODEOWNERS review for changes to the canonical skill.
- [ ] Enable secret scanning and dependency alerts where the GitHub plan permits.
- [ ] Give at least two HDF maintainers permission to issue or roll back releases.
- [ ] Publish releases from tags; do not distribute unversioned ZIPs from chat or email.

## Every release

- [ ] Confirm `VERSION` and `RELEASE_DATE`.
- [ ] Update `CHANGELOG.md`.
- [ ] Recheck current platform installation steps and model guidance.
- [ ] Run `python3 tools/release.py check`.
- [ ] Run `python3 -m unittest discover -s tests -v`.
- [ ] Run `python3 tools/release.py build`.
- [ ] Complete [ACCEPTANCE-TESTS.md](ACCEPTANCE-TESTS.md).
- [ ] Obtain HDF editorial-owner approval.
- [ ] Merge the approved commit to `main`.
- [ ] Create and push a signed or protected tag matching `VERSION`, such as `v1.0.0`.
- [ ] Confirm that GitHub Releases contains all three ZIPs, `SHA256SUMS` and `release-manifest.json`.
- [ ] Download one published artifact and verify its checksum.
- [ ] Announce the version and material changes to users.

## Rollback

- [ ] Mark a defective release clearly; do not silently replace its assets.
- [ ] Direct users to the previous known-good release.
- [ ] Fix forward with a new patch version and regression test.
