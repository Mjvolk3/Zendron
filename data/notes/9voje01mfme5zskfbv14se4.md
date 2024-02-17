## Zendron Ideas

- We can now add images by getting the local paths to the image annotations out of the cache.
- We can also create a two way sync for projects by writing the "comments" note to the data in Zotero. This way any new project can read this file and write on it to update it.

## Zendron Roadmap

- Solid bold lines have been completed.
- Dashed lines are loose plans.
- Brainstorming ideas to prevent fatal sync.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': "#E69F00", 'edgeLabelBackground':"#F0E442", 'tertiaryColor': '#fff0f0'}}}%%
flowchart TB
User((User))--oRun_Task{Run_Task}
User((User)) -.User_Input.->Make_Path_Change_Func([Make_Path_Change_Func])
  subgraph .vscode task
    Run_Task{Run_Task}==>Zendron:Sync{Zendron:Sync}
    Zendron:Sync{Zendron:Sync}==>Sync_Zotero.sh
    Sync_Zotero.sh==>resync.py
    Sync_Zotero.sh==>Pod-Import-Markdown
    Run_Task{Run_Task}-.->Zendron:Doctor_Fix_Path{Zendron:Doctor_Fix_Path}
    Run_Task{Run_Task}-.->Zendron:Delete_zotero_pod{Zendron:Delete_zotero_pod}
    Zendron:Delete_zotero_pod{Zendron:Delete_zotero_pod} -.-> Delete.sh
    Zendron:Doctor_Fix_Path{Zendron:Doctor_Fix_Path} -.-> Doctor.sh
    Delete.sh -.-> delete_pod.py
    Doctor.sh-.->doctor.py
  end
  subgraph resync.py
    Data_Class==Compile_Metadata_Func==>Metadata_Lines
    Metadata_Lines==Write_Metadata_Func==>Metadata.md_files
    Conf/Metadata.format-. Main_Func .->Data_Class
    Data_Class==Compile_Annotations_Func==>Annotations_Lines
    Annotations_Lines==Write_Annotations_Func==>Annotations.md_files
    Conf/Annotations.format-. Main_Func .->Data_Class
  end
  subgraph database.py
    Metadata_Date_Modified-.Database_Metadata_Func.-> Metadata_Database
    Metadata_Database-.Database_Metadata_Diff_Func.-> Metadata_Database_Diff
    Metadata_Annotations_Modified-.Database_Annotations_Func.-> Annotations_Database
    Annotations_Database-.Database_Annotations_Diff_Func.-> Annotations_Database_Diff
    Metadata_Database_Diff-.Init.-> Data_Class
    Annotations_Database_Diff-.Init.-> Data_Class
    Metadata_Database -.Clear_Database_Func.-> Metadata_Database
    Annotations_Database -.Clear_Database_Func.-> Annotations_Database
    Linked_Notes_Database -.Clear_Database_Func.-> Linked_Notes_Database
    Metadata_Database -.Load_Database_Func .-> Database_Obj
    Annotations_Database -.Load_Database_Func .-> Database_Obj
    Linked_Notes_Database -.Load_Database_Func .-> Database_Obj
  end
  subgraph Pod-Import-Markdown
    Metadata.md_files==>Dendron:Import_Pod
    Annotations.md_files==>Dendron:Import_Pod
    config.import.yml==>Dendron:Import_Pod
  end
  subgraph Dendron_Vault
    Dendron:Import_Pod==>Zendron.Import.*.md
    Zendron.Import.*.md==>Vault
    Zendron.Import.*.md-.wiki_link.->Zendron.Local.*.md
  end
  subgraph scan_import.py
    Zendron.Import.*.md-.extract-links.->Out_Linked_Notes
    Out_Linked_Notes-.database-links.->Linked_Notes_Database
  end
  subgraph delete_pod.py
    Zendron.Import.*.md-.Collect_Paths_Func.->Zotero_Limb_Paths
    Linked_Notes_Database-.Collect_Paths_Func.->Zotero_Link_Paths
    Zotero_Limb_Paths-.->Delete_zotero_pod_Func
    Zotero_Link_Paths-.->Delete_zotero_pod_Func
  end
  subgraph doctor.py
    *Zendron.Import.*.md -. fix_path .-> Local_Import_Path_Diff
    Zendron.Local.*.md -. fix_path .-> Local_Import_Path_Diff
    Local_Import_Path_Diff -.-> Make_Path_Change_Func([Make_Path_Change_Func])
    Make_Path_Change_Func([Make_Path_Change_Func])  -.-> Corrected_Paths
    Corrected_Paths-.Overwrite_Local_Path_Func  .->Zendron.Local.*.md
  end

  subgraph Ideas
    sync_backward.py-.->tags-and-comments
    refactor_before_import.py-.->stop-fatal-mistake
  end
  ```

## Issues

- Annotations are sorted by date modified [[sync|zendron/resync.py]]
  - `['data']['AnnotationSortIndex']` returns a number liked '00000|001873|00467'
  - Looks like the first number is index of item, the middle one changes the most maybe every character or word, and the last number changes medium maybe page wise.
- If `Dendron: Doctor` is used to `createMissingLinkedNotes` then notes will be created that cannot be easily deleted or overwritten by removing the import branch

## Itemized-Annotation-Collection

- [ ] Build database with this data.
![](/assets/images/delete-itemized-annotation-collection.png)
- [ ] BetterBibTex export is finnicky... pyzotero has a way to generate bibtex.
