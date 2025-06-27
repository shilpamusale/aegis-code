# Main entrypoint for the Aegis Code application that uses Hydra for configuration.

import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(config_path="config", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    """
    Main funstion orchstrated by HYdra.

    This function will load the configuration and eventually start
    FastAPI server or other application workflows.

    Args:
        cfg: A dictionary-like object holding the configuration
        from YAML files.

    """

    print("Configuration loaded successfully!")
    print(OmegaConf.to_yaml)

    # Start the FastAPI server and padd the configuration to it.


if __name__ == "__main__":
    main()
