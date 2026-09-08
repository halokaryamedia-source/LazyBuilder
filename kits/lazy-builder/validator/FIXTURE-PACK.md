# Acceptance Fixture Pack

The first local acceptance session uses **one bounded object/build concept** across all three input paths so differences can be attributed to the input mode rather than a different design.

## Required package

```text
case.json
inputs/text/prompt.txt
inputs/single/front.png
inputs/multiview/front.png
inputs/multiview/right.png
inputs/multiview/back.png
inputs/multiview/left.png
```

Use `prepare_case.py` to create the directories/manifest only. It does not start a runtime test.

## Selection criteria

Choose an object/build that is:

- geometrically clear from front/right/back/left;
- asymmetric enough that orientation mistakes are obvious;
- large enough to contain roof/slope and depth changes;
- simple enough that a V0 full-block result is still judgeable;
- free of vegetation, people, cables, smoke, glass-only shells, or other thin/noisy details;
- shown completely in frame with consistent proportions/crop between views.

A compact building, station, house, kiosk, or pavilion is preferable to an organic character for the first acceptance case.

## Image guidance

Prefer near-orthographic or mild-perspective views, neutral/simple background, consistent lighting, full silhouette visible, and the same exact design in every image.

Do not independently invent four different views from text for the first multiview acceptance pack. I2 should come from a genuinely consistent source set.

## Scale

`target_width_blocks` is explicit in `case.json`. The default template uses 64 only as a starting point. Change it before runtime if the selected fixture needs another intentional Minecraft width.

## Authority

T1 text, I1 single image, and I2 multiview are test inputs. They do not redefine one another. The user-selected reference package remains authority when judging generated geometry.
