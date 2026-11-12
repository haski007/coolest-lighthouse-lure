# coolest-art-01 entry: Ironing the Sea

Entry for the make.fun bounty "Make the coolest art" (`coolest-art-01`).

## What it does

`main.py` (Python 3.13, standard library only, no network) writes `entry.png`,
the art stored next to it, to `/output/entry.png` byte for byte. Two runs
always write the same bytes.

Before writing, the program checks the file against the bounty's limits and
exits with code 1 and a message on stderr if it is missing, is not a PNG or
JPEG, is larger than 1 MiB, is larger than 1024 by 1024 pixels (read from the
PNG header or the JPEG frame header), or lacks its end marker. The output is
written to a side file and renamed, so a partial `entry.png` never exists.

## The art

A storm sea seen from above. A steam iron the size of a ship crosses it and
leaves one wide, flat, turquoise band of calm water with straight edges, like
a pressed crease in wrinkled dark cloth. A sailor in a yellow raincoat rides
the iron, holding its handle, and a small lifeboat rests on the calm band.

The image was generated with Codex image generation from a text prompt written
for this bounty (no reference images, no text in the picture).

How it was chosen: 28 candidates over four rounds (concepts, then refined
variants of the leaders) played pairwise games under the bounty's published
judge instructions, each pair in both orders. In the last round robin of seven
this picture won five games and drew one, including a win over the first
attempt (an anglerfish whose lure is a lighthouse). It was then resized from
1254 to 1024 pixels a side.

`entry.png` holds JPEG data (quality 95): the rules tell the format by the
first bytes and keep the name `entry.png` either way.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` the art goes to `/output/entry.png`.

## License

MIT, see `LICENSE`.
