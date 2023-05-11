---
id: kot1u7ake6ay29lm3g6gewl
title: Ffmpeg
desc: ''
updated: 1683783515160
created: 1683782502997
---
```bash
ffmpeg -i notes/assets/videos/screencast/zendron-test_1.mov -vf "fps=4,scale=800:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 - -loop 0 -layers optimize notes/assets/videos/gif/zendron-test_1.gif
```

- `scale=800` is a nice default for github README.
- `fps=4` is nice default, but still a little fast.
