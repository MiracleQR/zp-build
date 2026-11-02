"""Patch ZPill for building with the official Flutter SDK.

`lib/platform/video_player.dart` references `OhosView`, which only exists in
the OpenHarmony-SIG flutter_flutter fork. The branch is never taken on iOS
(`Platform.operatingSystem` is "ios"), so replacing it with a comment keeps
the runtime behaviour identical for an iOS build.
"""

import sys
from pathlib import Path

TARGET = "lib/platform/video_player.dart"

OLD = """  if (Platform.operatingSystem == 'ohos') {
    return OhosView(
      viewType: 'zpill/video-view',
      onPlatformViewCreated: onCreated,
    );
  }
"""

NEW = "  // OhosView exists only in the OpenHarmony Flutter fork.\n"


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    path = root / TARGET
    if not path.is_file():
        print(f"missing {path}", file=sys.stderr)
        return 1

    source = path.read_text()
    if OLD not in source:
        print(f"patch target not found in {path}", file=sys.stderr)
        return 1

    patched = source.replace(OLD, NEW)
    path.write_text(patched)
    print(f"patched {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
