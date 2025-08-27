# Recommended setup for libraries in KiCAD repo

Source: Chat GPT

## 1) Keep **project-local libraries** in the repo

- Create folders like:

  ```
  /hardware/
    /libs/
      /symbols/         # .kicad_sym files
      /footprints/      # .pretty dir with .kicad_mod files
      /3d/              # STEP/WRL models (often large)
  ```

- Typical names:

  - `libs/symbols/<project>_symbols.kicad_sym`
  - `libs/footprints/<project>_footprints.pretty/…`

- Benefits: everything needed to open, edit, and build the design travels with the repo.

## 2) Use **project library tables** with **relative paths**

- In KiCad’s *Library Manager*, define **Project Specific** libraries, pointing to paths under `${KIPRJMOD}` (project root), e.g.
  - Symbols: `${KIPRJMOD}/hardware/libs/symbols/<project>_symbols.kicad_sym`
  - Footprints: `${KIPRJMOD}/hardware/libs/footprints/<project>_footprints.pretty`
- Ensure `sym-lib-table` and `fp-lib-table` exist in the project root. Commit them.
- Avoid global-only libs; they break on other machines.

## 3) External/shared libs → **submodules** (or vendored snapshots)

- If you rely on a company/open-source library:

  - Add as a **git submodule** pinned to a tag/commit under `hardware/ext-libs/...`

    ```
    git submodule add <git-url> hardware/ext-libs/kicad-footprints
    ```

  - Reference them in the project library tables using **relative paths**.

- If submodules feel heavy, vendor a snapshot into `ext-libs/` and update manually when needed.

## 4) 3D models: prefer **relative paths** and consider **Git LFS**

- Point models to `${KIPRJMOD}/hardware/libs/3d/...`

- Large binaries (STEP/WRL) → track with **Git LFS**:

  ```
  git lfs track "*.step"
  git lfs track "*.stp"
  git lfs track "*.wrl"
  git add .gitattributes
  ```

- Keep names and directories stable to avoid breakage.

## 5) Versioning & change control

- Treat libs like source code:
  - One change per commit (e.g., “Add SOT-223 footprint variant”).
  - Use tags/releases for tape-out milestones.
  - For shared libs (submodules), bump submodule commits via PRs to keep history clear.

## 6) CI/automation (nice to have)

- Add a simple CI job to:
  - Run `kicad-cli sch check` and `kicad-cli pcb check` (KiCad 7+).
  - Validate footprints exist and 3D model references resolve (scripted checks).
- This catches missing library entries early.

# Example repo layout

```
your-project/
├─ hardware/
│  ├─ project.kicad_pro
│  ├─ project.kicad_sch
│  ├─ project.kicad_pcb
│  ├─ sym-lib-table
│  ├─ fp-lib-table
│  └─ libs/
│     ├─ symbols/
│     │  └─ project_symbols.kicad_sym
│     ├─ footprints/
│     │  └─ project_footprints.pretty/
│     │     ├─ SOT-223.kicad_mod
│     │     └─ …
│     └─ 3d/
│        ├─ SOT-223.step
│        └─ …
└─ README.md
```

# `.gitignore` suggestions for KiCad

Keep the libraries and tables tracked; ignore generated/temporary files.

```
# KiCad autosaves & user settings
*.kicad_prl
*.kicad_pro-bak
*-bak
*.bak
*.tmp
*.autosave
*.lck

# Cache & metadata
fp-info-cache
sym-lib-table-bak
fp-lib-table-bak

# Plot/outputs (if generated)
*.gbr
*.drl
*.pos
*.rpt
*.zip

# OS junk
.DS_Store
Thumbs.db
```

# Migration tips (if you started with global libs)

1. Create the `libs/symbols` and `libs/footprints` folders in your project.
2. In *Library Manager*:
   - Add your symbol/footprint libs under **Project Specific**, pointing to the new local paths.
   - Remove project dependency on Global entries where possible.
3. Save to write `sym-lib-table` / `fp-lib-table` into the project.
4. Commit the new files and tables.

# Quick checklist

- [x]  Project has local symbol & footprint libs committed.
- [x]  All library paths are relative via `${KIPRJMOD}`.
- [x]  Project `sym-lib-table` & `fp-lib-table` committed.
- [ ]  3D models use relative paths; big ones tracked with Git LFS.
- [ ]  External libs come in via submodules (or vendored snapshots).
- [x]  `.gitignore` ignores only junk, not your libraries.
- [ ]  Optional CI runs KiCad checks.