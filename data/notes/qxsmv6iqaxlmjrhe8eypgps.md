## Config Location

- [stack overflow](https://stackoverflow.com/questions/70890187/referring-to-hydras-conf-directory-from-a-python-sub-sub-sub-directory-module)
  - Using the first option of putting the `__init__.py` in the conf directory... This is awkward because then any potential user would have to access `site-packages` to change their config. It would be better if the config can live at the root of the current project.
