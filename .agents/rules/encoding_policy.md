# Repository Encoding Policy

This policy defines the default text encoding and line-ending rules for
repositories coordinated by the agent OS.

## Decision

- Text files should use UTF-8 without BOM.
- C# source and .NET project files should use CRLF line endings.
- Markdown, JSON, YAML, and Unity serialized text assets should use LF line
  endings.
- Use both `.gitattributes` and `.editorconfig`.
- Do not add a pre-commit hook for encoding enforcement by default. Add one only
  if BOM or EOL churn continues after `.gitattributes` and `.editorconfig` are
  in place.

## Rationale

- `charset = utf-8` in `.editorconfig` means UTF-8 without BOM.
- CRLF for C# and .NET project files matches common Windows, Visual Studio, and
  Unity editor behavior and reduces repeated `LF will be replaced by CRLF`
  warnings when editors comply.
- LF for Markdown, JSON, YAML, and Unity serialized assets keeps generated
  metadata and data files stable across tools.
- `.gitattributes` controls how Git normalizes files. `.editorconfig` guides
  editors before files reach Git. Both are needed.

## Standard `.gitattributes` Baseline

Use this as the baseline for non-Unity repositories:

```gitattributes
* text=auto

*.cs text eol=crlf
*.csproj text eol=crlf
*.props text eol=crlf
*.targets text eol=crlf
*.sln text eol=crlf

*.json text eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
```

For Unity repositories, preserve existing Unity and Git LFS attribute entries.
Merge the following text rules instead of replacing the Unity template:

```gitattributes
*.cs text eol=crlf
*.csproj text eol=crlf
*.props text eol=crlf
*.targets text eol=crlf
*.sln text eol=crlf

*.json text eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf

*.asmdef text eol=lf
*.asmref text eol=lf
*.meta text eol=lf
*.asset text eol=lf
*.prefab text eol=lf
*.unity text eol=lf
*.mat text eol=lf
*.controller text eol=lf
*.anim text eol=lf
```

## Standard `.editorconfig` Baseline

```editorconfig
root = true

[*]
charset = utf-8
insert_final_newline = true
trim_trailing_whitespace = true

[*.{md,markdown}]
trim_trailing_whitespace = false

[*.{cs,csproj,props,targets,sln}]
end_of_line = crlf

[*.{json,yml,yaml,md,markdown,asmdef,asmref,meta,asset,prefab,unity,mat,controller,anim}]
end_of_line = lf
```

## Existing File Normalization

Do not perform broad file normalization in the same change that introduces this
policy. Apply configuration first, then handle existing BOM or EOL drift in a
separate targeted cleanup after reviewing diffs.

When normalizing existing files:

- Keep the diff narrow.
- Do not change file content beyond encoding or EOL normalization.
- Avoid mass rewriting generated Unity assets unless the change is intentional.
- Re-run build, test, or fixture validation affected by byte-level changes.

## Fixtures And Byte-Sensitive Data

For golden files, fixtures, snapshots, or test data that may be hashed or
compared byte-for-byte:

- Treat encoding and EOL changes as behavioral test input changes.
- Re-run the owning validation suite.
- If hashes or expected byte outputs exist, update them only in the same
  migration that intentionally changes the file bytes.

## Worker Requirements

Workers applying this policy must:

- Edit only `.gitattributes` and `.editorconfig` unless explicitly authorized.
- Preserve existing Unity, Git LFS, and binary attribute rules.
- Not run `git add --renormalize` unless explicitly requested.
- Report detected BOM files instead of normalizing them by default.
- Report any fixture or golden-file byte changes as a validation risk.
