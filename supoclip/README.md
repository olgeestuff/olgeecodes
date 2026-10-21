# SupoClip connector

Turns long-form videos (YouTube links or direct video URLs) into short vertical clips with the [SupoClip](https://supoclip.com) API.

You only need Python 3.8 or newer. There is nothing to install.

## 1. Add your API key (one time)

1. Create a key at https://www.supoclip.com/settings/api-keys. Your email must be verified first.
2. In this folder, copy `.env.example` to `.env`.
3. Paste the key after `SUPOCLIP_API_KEY=` and save.

`.env` is git-ignored, so the key never gets committed. Don't put the key in `supoclip.py` or in any other committed file.

## 2. Check the connection

```bash
python supoclip/supoclip.py check
```

If it works, you see `Connected.` followed by your plan and remaining quota.

## 3. Clip a video

```bash
# Create clips, wait for them to finish, list them, then download every clip
python supoclip/supoclip.py clip "https://www.youtube.com/watch?v=VIDEO_ID" --download

# With options
python supoclip/supoclip.py clip "https://youtu.be/VIDEO_ID" \
  --mode quality --captions hormozi --format vertical --download
```

| Option | Values | Default |
|---|---|---|
| `--mode` | `fast`, `balanced`, `quality` | `fast` |
| `--format` | `vertical`, `vertical_pan`, `vertical_split`, `original` | `vertical` |
| `--captions` | caption template, e.g. `default`, `hormozi`, `mrbeast` | `default` |
| `--no-subtitles` | turn burned-in subtitles off | subtitles on |
| `--broll` | add B-roll overlays | off |
| `--no-wait` | print the `task_id` and exit without waiting | waits |
| `--download` | save every clip to `./supoclip-downloads/` | off |

## Other commands

```bash
python supoclip/supoclip.py status   <task_id>              # progress
python supoclip/supoclip.py clips    <task_id>              # list clips + virality scores
python supoclip/supoclip.py download <task_id>              # download all clips
python supoclip/supoclip.py download <task_id> <clip_id>    # download one clip
```

## Errors

| Error | Meaning |
|---|---|
| `HTTP 401` | The key is wrong or was revoked. Create a new one. |
| `HTTP 402` | You hit your plan or quota limit. Run `check`. |
| `HTTP 403` | Verify your email on SupoClip. |
| `Cannot reach ...` | Network or firewall problem (see the note below). |

## Running in a Claude Code cloud session

The cloud sandbox blocks unknown hosts. In the environment settings (cloud environment menu in the title bar, then **Edit**):

- **Network access:** add `api.supoclip.com` under Allowed domains, or pick a broader access level.
- **Environment variables:** add `SUPOCLIP_API_KEY` with your key.

The settings take effect in a new session.

API reference: https://github.com/FujiwaraChoki/supoclip/blob/main/docs/api-reference.md
