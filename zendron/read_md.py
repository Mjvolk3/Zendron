from markdown import markdown

with open("notes/zendron.import.variational-graph-auto-encoders.comments.md", "r") as f:
    text = f.read()
    html = markdown(text)
    print("end")

# # Update the attachment
# zot.attachment_simple(
#     ["notes/zendron.import.variational-graph-auto-encoders.comments.md"], "ITY7GKUZ"
# )
# with open("result.json", "w") as fp:
#     json.dump(zot.children("UIVEMQEC"), fp, indent=4)

# with open("result.json") as f:
#     data = json.load(f)
# print("end")

# zot.attachment_simple(["result.json"], "ITY7GKUZ")

# zot.upload_attachments(
#     data,
#     "ITY7GKUZ",
#     "notes",
# )


# with open("Picnic.html", "w") as f:
#     f.write(html)
