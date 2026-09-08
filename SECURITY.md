# Security and Data Handling

LazyBuilder is publicly accessible but is not an appropriate storage location for private project/client production data.

## Do not commit

Do not commit or publish:

- credentials, API keys, tokens, passwords, or private configuration;
- private client/reference images, drawings, or source files without explicit public-visibility approval;
- generated project GLBs, Blender work files, schematics, or Minecraft-world data containing non-public project information;
- personally identifying or confidential data not required by the public system repository;
- temporary transfer payloads, encoded stand-ins, or upload-only helper artifacts.

## Project packages

`workspace/active/<project>/` and `workspace/archive/<project>/` are local/external mount conventions. Project subdirectories are ignored by Git. Keep actual project data in an authorized local/private repository or other approved storage location.

If a build must become a public example, create a deliberately sanitized example rather than publishing the live production package by default.

## Existing Git history

Deleting a file from the current tree or adding it to `.gitignore` does not remove copies already present in Git history.

If sensitive material is discovered in history:

1. stop adding new copies;
2. determine whether credentials need rotation;
3. treat history rewriting, visibility changes, and secret rotation as explicit security operations;
4. do not rewrite shared history as ordinary cleanup.

## Reporting

For a suspected exposure, contact the repository owner directly rather than opening a public issue containing sensitive material.

## Scope

Third-party tools, models, game content, assets, and libraries remain subject to their own licenses and permissions.
