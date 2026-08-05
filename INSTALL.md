# Installation

Choose your platform below. In every case, download the matching ZIP from the repository's **Releases** page rather than copying individual files.

## ChatGPT

Download:

`hdf-blog-editor-chatgpt-v1.0.0.zip`

Then:

1. Open ChatGPT.
2. In the sidebar, open **Plugins**, then the **Skills** tab.
3. Select **Create**, then **Upload from your computer**.
4. Upload the ZIP without extracting it.
5. Install or enable **HDF Blog Editor** when the scan completes.
6. Start a new conversation and type: **“I would like to review the next blog.”**

If Skills are unavailable in a managed workspace, ask the workspace administrator to enable skill creation, uploading and installation for your role.

## Claude

Download:

`hdf-blog-editor-claude-v1.0.0.zip`

Then:

1. Open Claude.
2. Go to **Customize → Skills**.
3. Select **+**, then **Create skill**.
4. Choose **Upload a skill** and upload the ZIP without extracting it.
5. Enable **HDF Blog Editor**.
6. Confirm that **Code execution and file creation** is enabled; the structural HTML checker depends on it.
7. Start a new conversation and type: **“I would like to review the next blog.”**

Team and Enterprise administrators can provision the skill organization-wide instead of asking each person to upload it.

## Google Antigravity

Download:

`hdf-blog-editor-antigravity-v1.0.0.zip`

Then:

1. Create or open the workspace where HDF blog work will be done.
2. Extract the ZIP into the workspace root. Keep the included `.agent` and `.agents` directories intact.
3. Restart or refresh Antigravity so it discovers the workspace skill and workflow.
4. Start naturally with **“I would like to review the next blog.”** or invoke the saved `/review-hdf-blog` workflow.

The package installs:

```text
.agent/skills/hdf-blog-editor/
.agents/workflows/review-hdf-blog.md
```

If your Antigravity version uses its Skills interface, you may instead import the skill folder from `.agent/skills/hdf-blog-editor/`.

## Updating

Download the newest release and replace the old installation:

- ChatGPT: upload or install the new skill release through Skills.
- Claude: upload the new ZIP with the same skill name; organization-managed deployments should be updated by an owner.
- Antigravity: replace the existing `.agent/skills/hdf-blog-editor/` folder and workflow with the files from the new ZIP.

Start a fresh conversation after updating so the new instructions are loaded cleanly.

## Optional download verification

Each release includes `SHA256SUMS`. This lets a maintainer confirm that a downloaded ZIP is byte-for-byte identical to the published artifact.

On macOS or Linux, place the ZIP and `SHA256SUMS` in the same folder and run:

```bash
shasum -a 256 -c SHA256SUMS
```

On Windows PowerShell, run `Get-FileHash <zip-name> -Algorithm SHA256` and compare the result with the matching line in `SHA256SUMS`.

## Verifying the installation

Try these prompts in a fresh conversation:

1. `I would like to review the next blog.`
2. `Help me fix these Yoast warnings.`
3. `Nothing to change in the content; write alt text for these images.`

The assistant should request only the next necessary material and should not demand a long technical prompt.
