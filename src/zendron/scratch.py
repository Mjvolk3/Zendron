# %%

from zendron import sync

# # %%

# # https://github.com/urschrei/pyzotero/issues/148

# group_id = 4761702
# library_type = "group" #or 'user'
# group_name = "parameter_estimation"
# # From Key generation: Your new API key has been created and is displayed below. Please save it now as it will not be accessible again after this point.
# api_key = "jzPvsy3TRlC8blUsbBZRMUMK"

# zot = zotero.Zotero(group_id, library_type, api_key)
# items = zot.top(limit=5)

# %%
# all_annotations = zot.everything(zot.items(itemType="annotation"))
# %%
# TODO implement tag update in vscode
# zot.add_tags(all_annotations[0], "test-tag")
# # adding tags
# all_annotations[0]['data']['tags']
# zot.update_item(all_annotations[0])
# %%
# all_annotations[0]
# %%
# TODO update only recently modified
# modified_dates = [i['data']['dateModified'] for i in all_annotations]
# modified_dates_parsed = [utc_parse(i) for i in modified_dates]
# LAST_MODIFIED_DATE = max(modified_dates_parsed)
# LAST_MODIFIED_DATE = max(modified_dates)
