Optional first-run splash animation
====================================

Place an animated GIF here as:

  splash.gif

RainTux plays **one full loop** (timing from the GIF frames), then the terms dialog.

Search order: ``RAINTUX_SPLASH_GIF`` env → repo ``raintux installer temp/loading_bg.gif`` → this file.

If none are present, a short placeholder splash is used (duration: ``RAINTUX_SPLASH_SECONDS``, default 2.5s).
