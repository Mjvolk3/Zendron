import logging
import os
import os.path as osp
from concurrent.futures import ThreadPoolExecutor, as_completed
from omegaconf import DictConfig
from pyzotero import zotero
from tqdm import tqdm
from zendron.annotations import AnnotationsCompiler
from zendron.cache import Cache, cache_difference
from zendron.comments import Comment, CommentCompiler
from zendron.items import get_annotated_attachments, get_attachments, get_metadatas
from zendron.metadata import Metadata, MetadataCompiler
from zendron.user_citation_key import UserCitationKey, UserCitationKeyCompiler
import hydra
from zendron import load

log = logging.getLogger(__name__)

def process_metadata_and_attachments(metadata_key, zot, cfg, cache):
    """Process a single piece of metadata and its attachments."""
    metadata = zot.item(metadata_key)
    attachments = get_attachments(zot, metadata["key"])
    metadata_obj = Metadata(metadata, attachments, cfg.dendron_limb)
    meta_compiler = MetadataCompiler(metadata_obj, cfg.pod_path)
    meta_compiler.compile()
    meta_compiler.write()
    user_citation_key = UserCitationKey(metadata_obj, cfg.pod_path)
    user_citation_key_compiler = UserCitationKeyCompiler(user_citation_key)
    user_citation_key_compiler.compile()
    user_citation_key_compiler.write()
    cache.add_metadata(metadata_obj.metadata)
    # Process annotated attachments
    annotated_attachments = get_annotated_attachments(zot, metadata_obj.key)
    for annot_attach in annotated_attachments:
        annotations = zot.children(annot_attach["key"])
        cache.add_annotations(annot_attach, annotations)
        # Compile annotations here if needed, or defer to later processing

def process_annotations(annot_attach_key, zot, cfg):
    """Process annotations for a given attachment."""
    metadata_key = metadata_key_from_annotated_attachment(annot_attach_key, zot)
    title_dendron = get_title_dendron(metadata_key, zot)
    annotations = zot.children(annot_attach_key)
    annot_compiler = AnnotationsCompiler(
        annot_attach_key,  # Adjust based on actual title field
        title_dendron,
        cfg.local_image_path,
        cfg.dendron_limb,
        cfg.pod_path,
    )
    annot_compiler.compile(annotations)
    annot_compiler.write()

def metadata_key_from_annotated_attachment(annotated_attachment, zot):
    """Extract metadata key from annotated attachment."""
    key = annotated_attachment['attachment_key']
    return zot.item(key)['links']['up']['href'].split('/')[-1]

def get_title_dendron(metadata_key, zot):
    """Generate a title dendron from metadata."""
    title = zot.item(metadata_key)["data"]["title"]
    title = title.replace(":", "-")
    return "-".join(title.split(" "))

@hydra.main(version_base=None, config_path=osp.join(os.getcwd(), "conf", "zendron"), config_name="config")
def main(cfg: DictConfig):
    if not osp.exists(".zendron.cache.json"):
        load.main(cfg)
        return

    zot = zotero.Zotero(cfg.library_id, cfg.library_type, cfg.api_key)
    new_cache = Cache(zot)
    old_cache = Cache(zot)
    old_cache.load()
    cache_diff = cache_difference(old_cache, new_cache)

    with ThreadPoolExecutor(max_workers=10) as executor:
        # Process new metadata and attachments
        futures_metadata = [executor.submit(process_metadata_and_attachments, metadata_key, zot, cfg, new_cache) for metadata_key in cache_diff["new_metadata"]]
        # Wait for all metadata processing to complete
        tqdm(as_completed(futures_metadata), total=len(futures_metadata), desc="Processing metadata and attachments")
        
        # Process new annotations
        futures_annotations = [executor.submit(process_annotations, annot_attach_key, zot, cfg) for annot_attach_key in cache_diff["new_annotations"]]
        # Wait for all annotation processing to complete
        tqdm(as_completed(futures_annotations), total=len(futures_annotations), desc="Processing annotations")

    new_cache.write()
    log.info("Cache update complete.")

if __name__ == "__main__":
    main()
