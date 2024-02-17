import bibtexparser
import hydra
from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero


def get_doi(zot):
    zot.add_parameters(format="bibtex")
    x = zot.item("C46JTY9H")
    doi = x.entries[0]["doi"]
    # x is a BibDatabase object.
    # Look up BibDatabase methods from bibtextparser documentation
    return doi


@hydra.main(
    version_base=None, config_path=osp.join(os.getcwd(), "conf"), config_name="config"
)
def main(cfg: DictConfig):
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type  # or 'user'
    zot = zotero.Zotero(library_id, library_type, api_key)
    doi = get_doi(zot)
    print(f"retrieved DOI from journalArticle... What is it like to be a Bat?: {doi}")


if __name__ == "__main__":
    main()
